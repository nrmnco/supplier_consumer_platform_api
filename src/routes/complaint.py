from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.user import get_user_by_email
from src.cruds.complaint import (
    create_complaint,
    get_complaint_by_id,
    get_complaints_for_consumer,
    get_complaints_for_salesman,
    get_escalated_complaints,
    get_complaints_for_manager,
    get_all_complaints_for_company,
    escalate_complaint,
    claim_complaint,
    resolve_complaint,
    close_complaint,
    get_complaint_history,
    check_user_can_access_complaint
)
from src.cruds.order import get_order_by_id
from src.schemas.complaint import CreateComplaint, UpdateComplaintStatus, ResolveComplaint
from src.models.users import UserRole
from src.models.complaints import ComplaintStatus

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.post("/order/{order_id}")
async def create_complaint_for_order(
    order_id: int,
    complaint_data: CreateComplaint,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Create a complaint for an order. Only the consumer who created the order can create a complaint.
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if order exists
    order = get_order_by_id(order_id, session)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user is the consumer who created the order
    if order.consumer_staff_id != user_obj.user_id:
        raise HTTPException(
            status_code=403,
            detail="Only the consumer who created the order can create a complaint"
        )
    
    try:
        complaint = create_complaint(session, order_id, user_obj.user_id, complaint_data)
        return {
            "message": "Complaint created successfully",
            "complaint": complaint
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-complaints")
async def get_my_complaints(
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Get all complaints created by the current user (consumer).
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    complaints = get_complaints_for_consumer(session, user_obj.user_id)
    
    return {
        "complaints": complaints
    }


@router.get("/assigned-to-me")
async def get_assigned_complaints(
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Get all complaints assigned to the current user (salesman).
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_obj.role not in [UserRole.staff, UserRole.manager, UserRole.owner]:
        raise HTTPException(
            status_code=403,
            detail="Only staff members can view assigned complaints"
        )
    
    complaints = get_complaints_for_salesman(session, user_obj.user_id)
    
    return {
        "complaints": complaints
    }


@router.get("/escalated")
async def get_escalated_complaints_list(
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Get all escalated complaints that haven't been claimed (manager only).
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_obj.role not in [UserRole.manager, UserRole.owner]:
        raise HTTPException(
            status_code=403,
            detail="Only managers can view escalated complaints"
        )
    
    complaints = get_escalated_complaints(session)
    
    return {
        "complaints": complaints
    }


@router.get("/my-managed-complaints")
async def get_my_managed_complaints(
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Get all complaints currently managed by the current user (manager).
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_obj.role not in [UserRole.manager, UserRole.owner]:
        raise HTTPException(
            status_code=403,
            detail="Only managers can view managed complaints"
        )
    
    complaints = get_complaints_for_manager(session, user_obj.user_id)
    
    return {
        "complaints": complaints
    }


@router.get("/company")
async def get_company_complaints(
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Get all complaints for the company (owner only).
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_obj.role != UserRole.owner:
        raise HTTPException(
            status_code=403,
            detail="Only owners can view all company complaints"
        )
    
    complaints = get_all_complaints_for_company(session, user_obj.company_id)
    
    return {
        "complaints": complaints
    }


@router.get("/{complaint_id}")
async def get_complaint_details(
    complaint_id: int,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Get details of a specific complaint.
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user can access this complaint
    if not check_user_can_access_complaint(session, user_obj.user_id, complaint_id):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this complaint"
        )
    
    complaint = get_complaint_by_id(session, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    return {
        "complaint": complaint
    }


@router.get("/{complaint_id}/history")
async def get_complaint_history_route(
    complaint_id: int,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Get history of a complaint.
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user can access this complaint
    if not check_user_can_access_complaint(session, user_obj.user_id, complaint_id):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this complaint"
        )
    
    history = get_complaint_history(session, complaint_id)
    
    return {
        "complaint_id": complaint_id,
        "history": history
    }


@router.put("/{complaint_id}/escalate")
async def escalate_complaint_route(
    complaint_id: int,
    update_data: UpdateComplaintStatus,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Escalate a complaint to manager (salesman only).
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    complaint = get_complaint_by_id(session, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Check if user is the assigned salesman
    if complaint.assigned_to_salesman_id != user_obj.user_id:
        raise HTTPException(
            status_code=403,
            detail="Only the assigned salesman can escalate this complaint"
        )
    
    try:
        updated_complaint = escalate_complaint(
            session,
            complaint_id,
            user_obj.user_id,
            update_data.notes
        )
        return {
            "message": "Complaint escalated successfully",
            "complaint": updated_complaint
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{complaint_id}/claim")
async def claim_complaint_route(
    complaint_id: int,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Claim an escalated complaint (manager only).
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_obj.role not in [UserRole.manager, UserRole.owner]:
        raise HTTPException(
            status_code=403,
            detail="Only managers can claim complaints"
        )
    
    try:
        updated_complaint = claim_complaint(session, complaint_id, user_obj.user_id)
        return {
            "message": "Complaint claimed successfully",
            "complaint": updated_complaint
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{complaint_id}/resolve")
async def resolve_complaint_route(
    complaint_id: int,
    resolve_data: ResolveComplaint,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Resolve a complaint. Salesman can resolve open complaints, manager can resolve in-progress complaints.
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    complaint = get_complaint_by_id(session, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Check permissions based on complaint status
    if complaint.status == ComplaintStatus.open:
        # Salesman can resolve open complaints
        if complaint.assigned_to_salesman_id != user_obj.user_id:
            raise HTTPException(
                status_code=403,
                detail="Only the assigned salesman can resolve this complaint"
            )
    elif complaint.status == ComplaintStatus.in_progress:
        # Manager can resolve in-progress complaints
        if complaint.escalated_to_manager_id != user_obj.user_id:
            raise HTTPException(
                status_code=403,
                detail="Only the assigned manager can resolve this complaint"
            )
        # Only managers can cancel orders
        if resolve_data.cancel_order and user_obj.role not in [UserRole.manager, UserRole.owner]:
            raise HTTPException(
                status_code=403,
                detail="Only managers can cancel orders"
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Complaint cannot be resolved in its current status"
        )
    
    try:
        updated_complaint = resolve_complaint(
            session,
            complaint_id,
            user_obj.user_id,
            resolve_data.resolution_notes,
            resolve_data.cancel_order
        )
        return {
            "message": "Complaint resolved successfully",
            "complaint": updated_complaint,
            "order_cancelled": resolve_data.cancel_order
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{complaint_id}/close")
async def close_complaint_route(
    complaint_id: int,
    resolve_data: ResolveComplaint,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Close a complaint (reject it) - manager only.
    """
    user_obj = get_user_by_email(session, user['sub'])
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_obj.role not in [UserRole.manager, UserRole.owner]:
        raise HTTPException(
            status_code=403,
            detail="Only managers can close complaints"
        )
    
    complaint = get_complaint_by_id(session, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Check if manager is assigned to this complaint
    if complaint.escalated_to_manager_id != user_obj.user_id:
        raise HTTPException(
            status_code=403,
            detail="Only the assigned manager can close this complaint"
        )
    
    try:
        updated_complaint = close_complaint(
            session,
            complaint_id,
            user_obj.user_id,
            resolve_data.resolution_notes,
            resolve_data.cancel_order
        )
        return {
            "message": "Complaint closed successfully",
            "complaint": updated_complaint,
            "order_cancelled": resolve_data.cancel_order
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
