from sqlmodel import Session, select
from datetime import datetime

from src.models.complaints import Complaints, ComplaintStatus
from src.models.complaint_history import ComplaintHistory
from src.models.orders import Orders, OrderStatus
from src.models.linkings import Linkings
from src.models.users import Users, UserRole
from src.schemas.complaint import CreateComplaint


def create_complaint(
    session: Session,
    order_id: int,
    consumer_staff_id: int,
    complaint_data: CreateComplaint
):
    """Create a new complaint for an order"""
    from src.cruds.chat import create_system_message
    from src.models.messages import MessageType

    # Get the order to find the assigned salesman
    order = session.get(Orders, order_id)
    if not order:
        raise ValueError("Order not found")
    
    # Get the linking to find assigned salesman
    linking = session.get(Linkings, order.linking_id)
    if not linking or not linking.assigned_salesman_user_id:
        raise ValueError("No salesman assigned to this linking")
    
    # Create the complaint
    complaint = Complaints(
        order_id=order_id,
        assigned_to_salesman_id=linking.assigned_salesman_user_id,
        status=ComplaintStatus.open,
        description=complaint_data.description,
        created_at=str(datetime.now()),
        updated_at=str(datetime.now())
    )
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    
    # Create initial history entry
    history = ComplaintHistory(
        complaint_id=complaint.complaint_id,
        changed_by_user_id=consumer_staff_id,
        new_status=ComplaintStatus.open,
        notes="Complaint created",
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    
    # Create system message
    message = create_system_message(
        session,
        order_id,
        consumer_staff_id,
        MessageType.complaint,
        {
            "event": "status_change",
            "entity": "complaint",
            "id": complaint.complaint_id,
            "old_status": None,
            "new_status": ComplaintStatus.open
        }
    )
    
    return complaint, message


def escalate_complaint(
    session: Session,
    complaint_id: int,
    salesman_id: int,
    notes: str | None = None
):
    """Escalate a complaint from salesman to manager"""
    from src.cruds.chat import create_system_message
    from src.models.messages import MessageType

    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status != ComplaintStatus.open:
        raise ValueError("Only open complaints can be escalated")
    
    old_status = complaint.status
    complaint.status = ComplaintStatus.escalated
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=salesman_id,
        new_status=ComplaintStatus.escalated,
        notes=notes or "Escalated to manager",
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    # Create system message
    message = create_system_message(
        session,
        complaint.order_id,
        salesman_id,
        MessageType.complaint,
        {
            "event": "status_change",
            "entity": "complaint",
            "id": complaint_id,
            "old_status": old_status,
            "new_status": ComplaintStatus.escalated
        }
    )
    
    return complaint, message


def claim_complaint(
    session: Session,
    complaint_id: int,
    manager_id: int
):
    """Manager claims an escalated complaint"""
    from src.cruds.chat import create_system_message
    from src.models.messages import MessageType

    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status != ComplaintStatus.escalated:
        raise ValueError("Only escalated complaints can be claimed")
    
    if complaint.escalated_to_manager_id is not None:
        raise ValueError("Complaint already claimed by another manager")
    
    old_status = complaint.status
    complaint.status = ComplaintStatus.in_progress
    complaint.escalated_to_manager_id = manager_id
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=manager_id,
        new_status=ComplaintStatus.in_progress,
        notes="Manager claimed complaint",
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    # Create system message
    message = create_system_message(
        session,
        complaint.order_id,
        manager_id,
        MessageType.complaint,
        {
            "event": "status_change",
            "entity": "complaint",
            "id": complaint_id,
            "old_status": old_status,
            "new_status": ComplaintStatus.in_progress
        }
    )
    
    return complaint, message


def resolve_complaint(
    session: Session,
    complaint_id: int,
    user_id: int,
    resolution_notes: str,
    cancel_order: bool = False
):
    """Resolve a complaint (by salesman or manager)"""
    from src.cruds.chat import create_system_message
    from src.models.messages import MessageType

    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status not in [ComplaintStatus.open, ComplaintStatus.in_progress]:
        raise ValueError("Only open or in-progress complaints can be resolved")
    
    old_status = complaint.status
    complaint.status = ComplaintStatus.resolved
    complaint.resolution_notes = resolution_notes
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # If manager wants to cancel the order
    if cancel_order:
        order = session.get(Orders, complaint.order_id)
        if order:
            order.status = OrderStatus.rejected
            order.updated_at = str(datetime.now())
            session.add(order)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=user_id,
        new_status=ComplaintStatus.resolved,
        notes=f"Resolved: {resolution_notes}" + (" (Order cancelled)" if cancel_order else ""),
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    # Create system message
    message = create_system_message(
        session,
        complaint.order_id,
        user_id,
        MessageType.complaint,
        {
            "event": "status_change",
            "entity": "complaint",
            "id": complaint_id,
            "old_status": old_status,
            "new_status": ComplaintStatus.resolved
        }
    )
    
    return complaint, message


def close_complaint(
    session: Session,
    complaint_id: int,
    manager_id: int,
    notes: str | None = None,
    cancel_order: bool = False
):
    """Close a complaint (reject it) - manager only"""
    from src.cruds.chat import create_system_message
    from src.models.messages import MessageType

    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status != ComplaintStatus.in_progress:
        raise ValueError("Only in-progress complaints can be closed")
    
    old_status = complaint.status
    complaint.status = ComplaintStatus.closed
    complaint.resolution_notes = notes or "Complaint closed"
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # If manager wants to cancel the order
    if cancel_order:
        order = session.get(Orders, complaint.order_id)
        if order:
            order.status = OrderStatus.rejected
            order.updated_at = str(datetime.now())
            session.add(order)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=manager_id,
        new_status=ComplaintStatus.closed,
        notes=notes or "Complaint closed" + (" (Order cancelled)" if cancel_order else ""),
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    # Create system message
    message = create_system_message(
        session,
        complaint.order_id,
        manager_id,
        MessageType.complaint,
        {
            "event": "status_change",
            "entity": "complaint",
            "id": complaint_id,
            "old_status": old_status,
            "new_status": ComplaintStatus.closed
        }
    )
    
    return complaint, message


def get_complaint_by_id(session: Session, complaint_id: int) -> Complaints | None:
    """Get a complaint by ID"""
    return session.get(Complaints, complaint_id)


def get_complaints_for_consumer(session: Session, user_id: int):
    """Get all complaints created by a consumer"""
    statement = (
        select(Complaints)
        .join(Orders)
        .where(Orders.consumer_staff_id == user_id)
        .order_by(Complaints.created_at.desc())
    )
    return session.exec(statement).all()


def get_complaints_for_salesman(session: Session, salesman_id: int):
    """Get all complaints assigned to a salesman"""
    statement = (
        select(Complaints)
        .where(Complaints.assigned_to_salesman_id == salesman_id)
        .where(Complaints.status.in_([ComplaintStatus.open]))
        .order_by(Complaints.created_at.desc())
    )
    return session.exec(statement).all()


def get_escalated_complaints(session: Session):
    """Get all escalated complaints that haven't been claimed by a manager"""
    statement = (
        select(Complaints)
        .where(Complaints.status == ComplaintStatus.escalated)
        .where(Complaints.escalated_to_manager_id.is_(None))
        .order_by(Complaints.created_at.desc())
    )
    return session.exec(statement).all()


def get_complaints_for_manager(session: Session, manager_id: int):
    """Get all complaints assigned to a specific manager"""
    statement = (
        select(Complaints)
        .where(Complaints.escalated_to_manager_id == manager_id)
        .where(Complaints.status == ComplaintStatus.in_progress)
        .order_by(Complaints.created_at.desc())
    )
    return session.exec(statement).all()


def get_all_complaints_for_company(session: Session, company_id: int):
    """Get all complaints for a company (for owners)"""
    statement = (
        select(Complaints)
        .join(Orders)
        .join(Linkings)
        .where(
            (Linkings.supplier_company_id == company_id) |
            (Linkings.consumer_company_id == company_id)
        )
        .order_by(Complaints.created_at.desc())
    )
    return session.exec(statement).all()


def escalate_complaint(
    session: Session,
    complaint_id: int,
    salesman_id: int,
    notes: str | None = None
) -> Complaints:
    """Escalate a complaint from salesman to manager"""
    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status != ComplaintStatus.open:
        raise ValueError("Only open complaints can be escalated")
    
    complaint.status = ComplaintStatus.escalated
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=salesman_id,
        new_status=ComplaintStatus.escalated,
        notes=notes or "Escalated to manager",
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    return complaint


def claim_complaint(
    session: Session,
    complaint_id: int,
    manager_id: int
) -> Complaints:
    """Manager claims an escalated complaint"""
    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status != ComplaintStatus.escalated:
        raise ValueError("Only escalated complaints can be claimed")
    
    if complaint.escalated_to_manager_id is not None:
        raise ValueError("Complaint already claimed by another manager")
    
    complaint.status = ComplaintStatus.in_progress
    complaint.escalated_to_manager_id = manager_id
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=manager_id,
        new_status=ComplaintStatus.in_progress,
        notes="Manager claimed complaint",
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    return complaint


def resolve_complaint(
    session: Session,
    complaint_id: int,
    user_id: int,
    resolution_notes: str,
    cancel_order: bool = False
) -> Complaints:
    """Resolve a complaint (by salesman or manager)"""
    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status not in [ComplaintStatus.open, ComplaintStatus.in_progress]:
        raise ValueError("Only open or in-progress complaints can be resolved")
    
    complaint.status = ComplaintStatus.resolved
    complaint.resolution_notes = resolution_notes
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # If manager wants to cancel the order
    if cancel_order:
        order = session.get(Orders, complaint.order_id)
        if order:
            order.status = OrderStatus.rejected
            order.updated_at = str(datetime.now())
            session.add(order)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=user_id,
        new_status=ComplaintStatus.resolved,
        notes=f"Resolved: {resolution_notes}" + (" (Order cancelled)" if cancel_order else ""),
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    return complaint


def close_complaint(
    session: Session,
    complaint_id: int,
    manager_id: int,
    notes: str | None = None,
    cancel_order: bool = False
) -> Complaints:
    """Close a complaint (reject it) - manager only"""
    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        raise ValueError("Complaint not found")
    
    if complaint.status != ComplaintStatus.in_progress:
        raise ValueError("Only in-progress complaints can be closed")
    
    complaint.status = ComplaintStatus.closed
    complaint.resolution_notes = notes or "Complaint closed"
    complaint.updated_at = str(datetime.now())
    session.add(complaint)
    
    # If manager wants to cancel the order
    if cancel_order:
        order = session.get(Orders, complaint.order_id)
        if order:
            order.status = OrderStatus.rejected
            order.updated_at = str(datetime.now())
            session.add(order)
    
    # Add history entry
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by_user_id=manager_id,
        new_status=ComplaintStatus.closed,
        notes=notes or "Complaint closed" + (" (Order cancelled)" if cancel_order else ""),
        updated_at=str(datetime.now())
    )
    session.add(history)
    session.commit()
    session.refresh(complaint)
    
    return complaint


def get_complaint_history(session: Session, complaint_id: int):
    """Get history for a complaint"""
    statement = (
        select(ComplaintHistory)
        .where(ComplaintHistory.complaint_id == complaint_id)
        .order_by(ComplaintHistory.updated_at.asc())
    )
    return session.exec(statement).all()


def check_user_can_access_complaint(
    session: Session,
    user_id: int,
    complaint_id: int
) -> bool:
    """Check if a user can access a complaint"""
    complaint = session.get(Complaints, complaint_id)
    if not complaint:
        return False
    
    user = session.get(Users, user_id)
    if not user:
        return False
    
    order = session.get(Orders, complaint.order_id)
    if not order:
        return False
    
    linking = session.get(Linkings, order.linking_id)
    if not linking:
        return False
    
    # Consumer who created the order
    if order.consumer_staff_id == user_id:
        return True
    
    # Assigned salesman
    if complaint.assigned_to_salesman_id == user_id:
        return True
    
    # Assigned manager
    if complaint.escalated_to_manager_id == user_id:
        return True
    
    # Owner of either company
    if user.role == UserRole.owner:
        if user.company_id == linking.supplier_company_id or user.company_id == linking.consumer_company_id:
            return True
    
    # Manager can see escalated complaints
    if user.role == UserRole.manager and complaint.status == ComplaintStatus.escalated:
        if user.company_id == linking.supplier_company_id:
            return True
    
    return False
