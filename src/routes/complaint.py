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
    **Create a complaint for a specific order.**

    This endpoint allows the consumer staff member who created the order to file a complaint.
    
    **Permissions:**
    - Only the **consumer staff member** who created the order can create a complaint for it.

    **Arguments:**
    - `order_id`: The ID of the order to complain about.
    - `complaint_data`:
        - `description`: A detailed description of the issue.

    **Returns:**
    - The created complaint object.

    **Raises:**
    - `404 Not Found`: If the order or user does not exist.
    - `403 Forbidden`: If the user is not the creator of the order.
    - `400 Bad Request`: If there is a validation error (e.g., order not found, no salesman assigned).
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
    **Get all complaints created by the current user.**

    Retrieves a list of all complaints filed by the authenticated consumer staff member.

    **Permissions:**
    - Any authenticated user (typically consumer staff).

    **Returns:**
    - A list of complaint objects created by the user.

    **Raises:**
    - `404 Not Found`: If the user does not exist.
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
    **Get complaints assigned to the current salesman.**

    Retrieves a list of open complaints assigned to the authenticated salesman.

    **Permissions:**
    - **Staff**, **Manager**, or **Owner** roles.
    - The user must be the assigned salesman for the complaints.

    **Returns:**
    - A list of open complaints assigned to the user.

    **Raises:**
    - `404 Not Found`: If the user does not exist.
    - `403 Forbidden`: If the user does not have the required role.
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
    **Get a list of escalated complaints (Manager Pool).**

    Retrieves all complaints with status `escalated` that have not yet been claimed by any manager.

    **Permissions:**
    - **Manager** or **Owner** roles only.

    **Returns:**
    - A list of unclaimed escalated complaints.

    **Raises:**
    - `404 Not Found`: If the user does not exist.
    - `403 Forbidden`: If the user is not a manager or owner.
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
    **Get complaints managed by the current manager.**

    Retrieves all complaints with status `in_progress` that have been claimed by the authenticated manager.

    **Permissions:**
    - **Manager** or **Owner** roles only.

    **Returns:**
    - A list of complaints currently being managed by the user.

    **Raises:**
    - `404 Not Found`: If the user does not exist.
    - `403 Forbidden`: If the user is not a manager or owner.
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
    **Get all complaints related to the user's company.**

    Retrieves all complaints where the user's company is either the supplier or the consumer.

    **Permissions:**
    - **Owner** role only.

    **Returns:**
    - A list of all complaints related to the company.

    **Raises:**
    - `404 Not Found`: If the user does not exist.
    - `403 Forbidden`: If the user is not an owner.
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
    **Get details of a specific complaint.**

    Retrieves full details of a complaint by its ID.

    **Permissions:**
    - **Consumer**: If they created the order.
    - **Salesman**: If assigned to the complaint.
    - **Manager**: If assigned to the complaint or if it's escalated (and they are from the supplier company).
    - **Owner**: If they own the supplier or consumer company.

    **Arguments:**
    - `complaint_id`: The ID of the complaint.

    **Returns:**
    - The complaint object.

    **Raises:**
    - `404 Not Found`: If the user or complaint does not exist.
    - `403 Forbidden`: If the user does not have permission to view the complaint.
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
    **Get the history of a complaint.**

    Retrieves the timeline of status changes and notes for a specific complaint.

    **Permissions:**
    - Same as `get_complaint_details` (Consumer, Assigned Salesman, Assigned/Eligible Manager, Owner).

    **Arguments:**
    - `complaint_id`: The ID of the complaint.

    **Returns:**
    - A list of history entries for the complaint.

    **Raises:**
    - `404 Not Found`: If the user does not exist.
    - `403 Forbidden`: If the user does not have permission to view the complaint.
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
    **Escalate a complaint to a manager.**

    Changes the complaint status from `open` to `escalated`.

    **Permissions:**
    - Only the **assigned salesman** can escalate the complaint.

    **Arguments:**
    - `complaint_id`: The ID of the complaint.
    - `update_data`:
        - `notes`: Optional notes explaining the reason for escalation.

    **Returns:**
    - The updated complaint object with status `escalated`.

    **Raises:**
    - `404 Not Found`: If the user or complaint does not exist.
    - `403 Forbidden`: If the user is not the assigned salesman.
    - `400 Bad Request`: If the complaint is not in `open` status or other validation errors.
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
    **Claim an escalated complaint.**

    Allows a manager to take ownership of an escalated complaint. Changes status from `escalated` to `in_progress`.

    **Permissions:**
    - **Manager** or **Owner** roles only.

    **Arguments:**
    - `complaint_id`: The ID of the complaint.

    **Returns:**
    - The updated complaint object with status `in_progress` and assigned manager.

    **Raises:**
    - `404 Not Found`: If the user does not exist.
    - `403 Forbidden`: If the user is not a manager or owner.
    - `400 Bad Request`: If the complaint is not in `escalated` status or already claimed.
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
    **Resolve a complaint.**

    Marks a complaint as `resolved`.

    **Permissions:**
    - **Salesman**: Can resolve `open` complaints assigned to them.
    - **Manager**: Can resolve `in_progress` complaints assigned to them.
    - **Note**: Only **Managers** and **Owners** can choose to cancel the order (`cancel_order=True`).

    **Arguments:**
    - `complaint_id`: The ID of the complaint.
    - `resolve_data`:
        - `resolution_notes`: Notes describing how the issue was resolved.
        - `cancel_order`: Boolean (default False). If True, the associated order status is set to `rejected`.

    **Returns:**
    - The updated complaint object with status `resolved`.

    **Raises:**
    - `404 Not Found`: If the user or complaint does not exist.
    - `403 Forbidden`: If the user is not assigned or lacks permission to cancel orders.
    - `400 Bad Request`: If the complaint status is invalid for resolution.
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
    **Close (Reject) a complaint.**

    Marks a complaint as `closed`, typically meaning it was rejected or could not be resolved to the consumer's satisfaction.

    **Permissions:**
    - **Manager** or **Owner** roles only.
    - Must be the assigned manager for the complaint.

    **Arguments:**
    - `complaint_id`: The ID of the complaint.
    - `resolve_data`:
        - `resolution_notes`: Notes explaining why the complaint is being closed.
        - `cancel_order`: Boolean (default False). If True, the associated order status is set to `rejected`.

    **Returns:**
    - The updated complaint object with status `closed`.

    **Raises:**
    - `404 Not Found`: If the user or complaint does not exist.
    - `403 Forbidden`: If the user is not the assigned manager or lacks required role.
    - `400 Bad Request`: If the complaint is not in `in_progress` status.
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
