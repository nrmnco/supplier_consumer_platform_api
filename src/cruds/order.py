from sqlmodel import Session, select
from datetime import datetime

from src.models.linkings import Linkings
from src.models.orders import Orders, OrderStatus
from src.models.order_products import OrderProducts
from src.models.products import Products
from src.schemas.order import OrderCreate


def create_order(order_data: OrderCreate, session: Session):
    total_price = 0

    # check products and calculate price
    for item in order_data.products:
        product = session.exec(
            select(Products).where(Products.product_id == item.product_id)
        ).first()

        if not product:
            raise ValueError(f"Product {item.product_id} not found")

        if product.stock_quantity < item.quantity:
            raise ValueError(f"Product {product.name} does not have enough stock")

        total_price += product.retail_price * item.quantity

    # create order
    order = Orders(
        linking_id=order_data.linking_id,
        consumer_staff_id=order_data.consumer_staff_id,
        total_proce=total_price,
        status=OrderStatus.created,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    # add order products
    for item in order_data.products:
        product = session.exec(
            select(Products).where(Products.product_id == item.product_id)
        ).one()

        op = OrderProducts(
            order_id=order.order_id,
            product_id=item.product_id,
            product_quantity=item.quantity,
            product_price=product.retail_price
        )
        session.add(op)

        # decrease stock
        product.stock_quantity -= item.quantity

    session.commit()
    return order


def get_order_by_id(order_id: int, session: Session):
    return session.exec(
        select(Orders).where(Orders.order_id == order_id)
    ).first()


def get_orders_for_company(company_id: int, session: Session):
    statement = (
        select(Orders)
        .join(Linkings)
        .where(
            (Linkings.supplier_company_id == company_id)
            | (Linkings.consumer_company_id == company_id)
        )
    )
    return session.exec(statement).all()


def update_order_status(order_id: int, new_status: OrderStatus, session: Session):
    order = get_order_by_id(order_id, session)
    if not order:
        raise ValueError("Order not found")

    order.status = new_status
    order.updated_at = datetime.now()
    session.commit()
    return order