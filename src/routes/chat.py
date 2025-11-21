from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlmodel import Session
from typing import Dict
import json

from src.core.database import get_session
from src.core.jwt import decode_token
from src.core.security import check_access_token
from src.cruds.user import get_user_by_email
from src.cruds.chat import (
    get_or_create_chat_for_linking,
    create_message,
    check_user_can_chat
)
from src.models.messages import MessageType

router = APIRouter(prefix="/chat", tags=["Chat"])

# Store active WebSocket connections: {linking_id: {user_id: websocket}}
active_connections: Dict[int, Dict[int, WebSocket]] = {}


def verify_websocket_token(token: str) -> dict:
    try:
        decoded_token = decode_token(token, refresh=False)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


async def connect_websocket(websocket: WebSocket, linking_id: int, user_id: int):
    if linking_id not in active_connections:
        active_connections[linking_id] = {}
    active_connections[linking_id][user_id] = websocket


async def disconnect_websocket(linking_id: int, user_id: int):
    if linking_id in active_connections:
        active_connections[linking_id].pop(user_id, None)
        if not active_connections[linking_id]:
            del active_connections[linking_id]


async def broadcast_message(linking_id: int, message_data: dict, exclude_user_id: int = None):
    if linking_id not in active_connections:
        return
    
    message_json = json.dumps(message_data)
    disconnected_users = []
    
    for user_id, connection in active_connections[linking_id].items():
        if user_id != exclude_user_id:
            try:
                await connection.send_text(message_json)
            except Exception:
                disconnected_users.append(user_id)
    
    for user_id in disconnected_users:
        await disconnect_websocket(linking_id, user_id)


@router.websocket("/ws/{linking_id}")
async def websocket_chat(websocket: WebSocket, linking_id: int):
    try:
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008, reason="Token required")
            return

        decoded_token = verify_websocket_token(token)
        email = decoded_token.get("sub")
        
        if not email:
            await websocket.close(code=1008, reason="Invalid token")
            return

        from src.core.database import engine
        with Session(engine) as session:
            user = get_user_by_email(session, email)
            
            if not user:
                await websocket.close(code=1008, reason="User not found")
                return
            

            if not check_user_can_chat(session, user.user_id, linking_id):
                await websocket.close(code=1008, reason="Access denied: You are not authorized to chat in this linking")
                return
            
            chat = get_or_create_chat_for_linking(session, linking_id)
            
            await websocket.accept()
            
            await connect_websocket(websocket, linking_id, user.user_id)
            
            await websocket.send_json({
                "type": "connection",
                "message": "Connected to chat",
                "chat_id": chat.chat_id,
                "linking_id": linking_id
            })
            
            try:
                while True:

                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    
                    body = message_data.get("body", "").strip()
                    if not body:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Message body cannot be empty"
                        })
                        continue
                    
                    message_type_str = message_data.get("type", "text")
                    try:
                        message_type = MessageType(message_type_str)
                    except ValueError:
                        message_type = MessageType.text
                    
                    with Session(engine) as msg_session:
                        message = create_message(
                            msg_session,
                            chat.chat_id,
                            user.user_id,
                            body,
                            message_type
                        )
                        
                        broadcast_data = {
                            "type": "message",
                            "message_id": message.message_id,
                            "chat_id": message.chat_id,
                            "sender_id": message.sender_id,
                            "sender_name": f"{user.first_name} {user.last_name}",
                            "body": message.body,
                            "message_type": message.type,
                            "sent_at": message.sent_at
                        }
                        
                        await broadcast_message(linking_id, broadcast_data, exclude_user_id=user.user_id)
                        
                        await websocket.send_json({
                            "type": "message_sent",
                            "message_id": message.message_id,
                            "sent_at": message.sent_at
                        })
                    
            except WebSocketDisconnect:
                await disconnect_websocket(linking_id, user.user_id)
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error processing message: {str(e)}"
                })
                await disconnect_websocket(linking_id, user.user_id)
                
    except HTTPException as e:
        await websocket.close(code=1008, reason=str(e.detail))
    except Exception as e:
        await websocket.close(code=1011, reason=f"Server error: {str(e)}")


@router.get("/messages/{linking_id}")
async def get_chat_messages(
    linking_id: int,
    limit: int = 100,
    offset: int = 0,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    from src.cruds.chat import get_messages_for_chat, get_or_create_chat_for_linking, check_user_can_chat
    from fastapi import HTTPException
    
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not check_user_can_chat(session, user_obj.user_id, linking_id):
        raise HTTPException(status_code=403, detail="Access denied: You are not authorized to access this chat")
    
    chat = get_or_create_chat_for_linking(session, linking_id)
    
    messages = get_messages_for_chat(session, chat.chat_id, limit, offset)
    
    return {
        "chat_id": chat.chat_id,
        "linking_id": linking_id,
        "messages": [
            {
                "message_id": msg.message_id,
                "sender_id": msg.sender_id,
                "body": msg.body,
                "type": msg.type,
                "sent_at": msg.sent_at
            }
            for msg in messages
        ],
        "limit": limit,
        "offset": offset
    }


# Order chat endpoints
# Store active WebSocket connections for order chats: {order_id: {user_id: websocket}}
active_order_connections: Dict[int, Dict[int, WebSocket]] = {}


async def connect_order_websocket(websocket: WebSocket, order_id: int, user_id: int):
    if order_id not in active_order_connections:
        active_order_connections[order_id] = {}
    active_order_connections[order_id][user_id] = websocket


async def disconnect_order_websocket(order_id: int, user_id: int):
    if order_id in active_order_connections:
        active_order_connections[order_id].pop(user_id, None)
        if not active_order_connections[order_id]:
            del active_order_connections[order_id]


async def broadcast_order_message(order_id: int, message_data: dict, exclude_user_id: int = None):
    if order_id not in active_order_connections:
        return
    
    message_json = json.dumps(message_data)
    disconnected_users = []
    
    for user_id, connection in active_order_connections[order_id].items():
        if user_id != exclude_user_id:
            try:
                await connection.send_text(message_json)
            except Exception:
                disconnected_users.append(user_id)
    
    for user_id in disconnected_users:
        await disconnect_order_websocket(order_id, user_id)


@router.websocket("/ws/order/{order_id}")
async def websocket_order_chat(websocket: WebSocket, order_id: int):
    try:
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008, reason="Token required")
            return

        decoded_token = verify_websocket_token(token)
        email = decoded_token.get("sub")
        
        if not email:
            await websocket.close(code=1008, reason="Invalid token")
            return

        from src.core.database import engine
        from src.cruds.chat import get_chat_for_order, check_user_can_access_order_chat
        
        with Session(engine) as session:
            user = get_user_by_email(session, email)
            
            if not user:
                await websocket.close(code=1008, reason="User not found")
                return
            
            if not check_user_can_access_order_chat(session, user.user_id, order_id):
                await websocket.close(code=1008, reason="Access denied: You are not authorized to chat in this order")
                return
            
            chat = get_chat_for_order(session, order_id)
            if not chat:
                await websocket.close(code=1008, reason="Order chat not found")
                return
            
            await websocket.accept()
            
            await connect_order_websocket(websocket, order_id, user.user_id)
            
            await websocket.send_json({
                "type": "connection",
                "message": "Connected to order chat",
                "chat_id": chat.chat_id,
                "order_id": order_id
            })
            
            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    
                    body = message_data.get("body", "").strip()
                    if not body:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Message body cannot be empty"
                        })
                        continue
                    
                    message_type_str = message_data.get("type", "text")
                    try:
                        message_type = MessageType(message_type_str)
                    except ValueError:
                        message_type = MessageType.text
                    
                    with Session(engine) as msg_session:
                        message = create_message(
                            msg_session,
                            chat.chat_id,
                            user.user_id,
                            body,
                            message_type
                        )
                        
                        broadcast_data = {
                            "type": "message",
                            "message_id": message.message_id,
                            "chat_id": message.chat_id,
                            "sender_id": message.sender_id,
                            "sender_name": f"{user.first_name} {user.last_name}",
                            "body": message.body,
                            "message_type": message.type,
                            "sent_at": message.sent_at
                        }
                        
                        await broadcast_order_message(order_id, broadcast_data, exclude_user_id=user.user_id)
                        
                        await websocket.send_json({
                            "type": "message_sent",
                            "message_id": message.message_id,
                            "sent_at": message.sent_at
                        })
                    
            except WebSocketDisconnect:
                await disconnect_order_websocket(order_id, user.user_id)
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error processing message: {str(e)}"
                })
                await disconnect_order_websocket(order_id, user.user_id)
                
    except HTTPException as e:
        await websocket.close(code=1008, reason=str(e.detail))
    except Exception as e:
        await websocket.close(code=1011, reason=f"Server error: {str(e)}")


@router.get("/messages/order/{order_id}")
async def get_order_chat_messages(
    order_id: int,
    limit: int = 100,
    offset: int = 0,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    from src.cruds.chat import get_messages_for_chat, get_chat_for_order, check_user_can_access_order_chat
    from fastapi import HTTPException
    
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not check_user_can_access_order_chat(session, user_obj.user_id, order_id):
        raise HTTPException(status_code=403, detail="Access denied: You are not authorized to access this order chat")
    
    chat = get_chat_for_order(session, order_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Order chat not found")
    
    messages = get_messages_for_chat(session, chat.chat_id, limit, offset)
    
    return {
        "chat_id": chat.chat_id,
        "order_id": order_id,
        "messages": [
            {
                "message_id": msg.message_id,
                "sender_id": msg.sender_id,
                "body": msg.body,
                "type": msg.type,
                "sent_at": msg.sent_at
            }
            for msg in messages
        ],
        "limit": limit,
        "offset": offset
    }
