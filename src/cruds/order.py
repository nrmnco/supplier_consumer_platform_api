from sqlmodel import Session, select
from datetime import datetime

from src.models.linkings import Linkings
from src.models.orders import Orders, OrderStatus
from src.models.order_products import OrderProducts
from src.models.products import Products
from src.models.chats import Chats
from src.schemas.order import OrderCreate


def create_order(order_data: OrderCreate, linking_id: int, user_id: int, session: Session):
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
        
        if product.threshold <= item.quantity:
            total_price += product.bulk_price * item.quantity
        else:
            total_price += product.retail_price * item.quantity

    # create order
    order = Orders(
        linking_id=linking_id,
        consumer_staff_id=user_id,
        total_price=total_price,
        status=OrderStatus.created
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    # create order chat automatically
    order_chat = Chats(
        linking_id=linking_id,
        order_id=order.order_id,
        created_at=str(datetime.now())
    )
    session.add(order_chat)
    session.commit()

    # add order products
    for item in order_data.products:
        product = session.exec(
            select(Products).where(Products.product_id == item.product_id)
        ).one()

        if product.threshold <= item.quantity:
            price = product.bulk_price
        else:
            price = product.retail_price

        op = OrderProducts(
            order_id=order.order_id,
            product_id=item.product_id,
            product_quantity=item.quantity,
            product_price=price
        )
        session.add(op)

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


def get_ordered_products_for_company(company_id: int, session: Session):
    # Get all orders for the company
    orders = get_orders_for_company(company_id, session)
    order_ids = [order.order_id for order in orders]
    
    if not order_ids:
        return []
    
    # Create a dictionary for quick order lookup
    orders_dict = {order.order_id: order for order in orders}
    
    # Get all order products for these orders
    statement = (
        select(OrderProducts)
        .where(OrderProducts.order_id.in_(order_ids))
    )
    
    order_products = session.exec(statement).all()
    
    # Get all product IDs and fetch products in one query
    product_ids = [op.product_id for op in order_products]
    if not product_ids:
        return []
    
    products_statement = (
        select(Products)
        .where(Products.product_id.in_(product_ids))
    )
    products = session.exec(products_statement).all()
    products_dict = {product.product_id: product for product in products}
    
    # Format the results to return products with order information
    products_list = []
    for order_product in order_products:
        # Get the product details
        product = products_dict.get(order_product.product_id)
        if not product:
            continue
            
        # Get the order for this order_product
        order = orders_dict.get(order_product.order_id)
        if order:
            products_list.append({
                "order_id": order.order_id,
                'linking_id': order.linking_id,
                "product_id": product.product_id,
                "product_name": product.name,
                "product_description": product.description,
                "product_picture_url": product.picture_url,
                "quantity": order_product.product_quantity,
                "price": order_product.product_price,
                "unit": product.unit,
                "order_status": order.status,
                "order_total_price": order.total_price,
                "order_created_at": order.created_at,
                "order_updated_at": order.updated_at
            })
    
    return products_list


def get_products_for_order(order_id: int, session: Session):
    # Get all order products for this order
    statement = (
        select(OrderProducts)
        .where(OrderProducts.order_id == order_id)
    )
    
    order_products = session.exec(statement).all()
    
    if not order_products:
        return []
    
    # Get all product IDs and fetch products in one query
    product_ids = [op.product_id for op in order_products]
    
    products_statement = (
        select(Products)
        .where(Products.product_id.in_(product_ids))
    )
    products = session.exec(products_statement).all()
    products_dict = {product.product_id: product for product in products}
    
    # Format the results to return products with order product information
    products_list = []
    for order_product in order_products:
        # Get the product details
        product = products_dict.get(order_product.product_id)
        if not product:
            continue
            
        products_list.append({
            "product_id": product.product_id,
            "product_name": product.name,
            "product_description": product.description,
            "product_picture_url": product.picture_url,
            "quantity": order_product.product_quantity,
            "price": order_product.product_price,
            "unit": product.unit
        })
    
    return products_list


def update_order_status(order_id: int, new_status: OrderStatus, user_id: int, session: Session):
    from src.cruds.chat import create_system_message
    from src.models.messages import MessageType

    order = get_order_by_id(order_id, session)
    if not order:
        raise ValueError("Order not found")

    old_status = order.status
    order.status = new_status
    order.updated_at = str(datetime.now())
    session.commit()
    session.refresh(order)
    
    # Create system message
    message = create_system_message(
        session,
        order_id,
        user_id,
        MessageType.order,
        {
            "event": "status_change",
            "entity": "order",
            "id": order_id,
            "old_status": old_status,
            "new_status": new_status
        }
    )
    
    return order, message


def get_orders_by_linking_id(linking_id: int, session: Session):
    return session.exec(
        select(Orders).where(Orders.linking_id == linking_id)
    ).all()
