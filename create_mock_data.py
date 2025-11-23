import random
from sqlmodel import Session, select
from src.core.database import engine
from src.models.companies import Companies, CompanyType, CompanyStatus
from src.models.users import Users, UserRole, UserStatus
from src.models.products import Products
from src.models.linkings import Linkings, LinkingStatus
from src.models.orders import Orders, OrderStatus
from src.models.order_products import OrderProducts
from src.core.security import hash_password

def create_mock_data():
    with Session(engine) as session:
        print("Creating companies...")
        
        first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Jessica", "William", "Ashley", "James", "Linda", "Richard", "Patricia", "Thomas", "Elizabeth"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]

        suppliers = []
        consumers = []
        
        supplier_names = ["TechParts Inc.", "Global Foods", "BuildIt Materials", "Office Supplies Co.", "ChemWorks"]
        consumer_names = ["Gadget Store", "Restaurant Chain", "Construction Corp", "Corporate Office", "Lab Solutions"]
        
        logo_urls = [
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/1a37b342-ca35-4ef5-bbf7-9ab93548ac0f.jpg",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/058c400d-a105-41ab-94da-340ed4389348.png",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/448653f7-077a-4e8f-b1cb-bab74a2cf760.jpg",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/0095eb9e-1c3d-4669-8d8a-9c981f19524b.jpg",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/5f758e52-a038-433a-a563-9dded62271b6.jpg"
        ]
        
        for i, name in enumerate(supplier_names):
            existing = session.exec(select(Companies).where(Companies.name == name)).first()
            if existing:
                existing.logo_url = logo_urls[i % len(logo_urls)]
                session.add(existing)
                suppliers.append(existing)
                continue

            company = Companies(
                name=name,
                location=f"Location {i}",
                company_type=CompanyType.supplier,
                status=CompanyStatus.active,
                description=f"Supplier of {name}",
                logo_url=logo_urls[i % len(logo_urls)]
            )
            session.add(company)
            suppliers.append(company)
            
        for i, name in enumerate(consumer_names):
            existing = session.exec(select(Companies).where(Companies.name == name)).first()
            if existing:
                existing.logo_url = logo_urls[i % len(logo_urls)]
                session.add(existing)
                consumers.append(existing)
                continue

            company = Companies(
                name=name,
                location=f"Location {i+5}",
                company_type=CompanyType.consumer,
                status=CompanyStatus.active,
                description=f"Consumer {name}",
                logo_url=logo_urls[i % len(logo_urls)]
            )
            session.add(company)
            consumers.append(company)
            
        session.commit()
        
        for c in suppliers + consumers:
            session.refresh(c)
            
        print("Creating users...")
        users = []
        for company in suppliers + consumers:
            company_slug = company.name.replace(' ', '').replace('.', '').lower()
            
            if company.company_type == CompanyType.supplier:
                manager_email = f"manager@{company_slug}.com"
                existing_manager = session.exec(select(Users).where(Users.email == manager_email)).first()
                
                f_name = random.choice(first_names)
                l_name = random.choice(last_names)
                
                if existing_manager:
                    existing_manager.first_name = f_name
                    existing_manager.last_name = l_name
                    session.add(existing_manager)
                    users.append(existing_manager)
                else:
                    manager = Users(
                        company_id=company.company_id,
                        first_name=f_name,
                        last_name=l_name,
                        email=manager_email,
                        phone_number=f"555-000-{company.company_id}",
                        hashed_password=hash_password("password123"),
                        role=UserRole.manager,
                        status=UserStatus.active
                    )
                    session.add(manager)
                    users.append(manager)

            owner_email = f"owner@{company_slug}.com"
            existing_owner = session.exec(select(Users).where(Users.email == owner_email)).first()
            
            f_name = random.choice(first_names)
            l_name = random.choice(last_names)
            
            if existing_owner:
                existing_owner.first_name = f_name
                existing_owner.last_name = l_name
                session.add(existing_owner)
                users.append(existing_owner)
            else:
                owner = Users(
                    company_id=company.company_id,
                    first_name=f_name,
                    last_name=l_name,
                    email=owner_email,
                    phone_number=f"555-111-{company.company_id}",
                    hashed_password=hash_password("password123"),
                    role=UserRole.owner,
                    status=UserStatus.active
                )
                session.add(owner)
                users.append(owner)

            staff_email = f"staff@{company_slug}.com"
            existing_staff = session.exec(select(Users).where(Users.email == staff_email)).first()
            
            f_name = random.choice(first_names)
            l_name = random.choice(last_names)
            
            if existing_staff:
                existing_staff.first_name = f_name
                existing_staff.last_name = l_name
                session.add(existing_staff)
                users.append(existing_staff)
            else:
                staff = Users(
                    company_id=company.company_id,
                    first_name=f_name,
                    last_name=l_name,
                    email=staff_email,
                    phone_number=f"555-222-{company.company_id}",
                    hashed_password=hash_password("password123"),
                    role=UserRole.staff,
                    status=UserStatus.active
                )
                session.add(staff)
                users.append(staff)
            
        session.commit()
        
        for u in users:
            session.refresh(u)
            
        print("Creating products...")
        all_products = []
        for supplier in suppliers:
            existing_products = session.exec(select(Products).where(Products.company_id == supplier.company_id)).all()
            if len(existing_products) >= 5:
                all_products.extend(existing_products)
                continue

            for j in range(5):
                product = Products(
                    company_id=supplier.company_id,
                    name=f"Product {j} of {supplier.name}",
                    description=f"Description for product {j}",
                    stock_quantity=100,
                    retail_price=100 + j * 10,
                    minimum_order=1,
                    unit="pcs",
                    is_available=True
                )
                session.add(product)
                all_products.append(product)
                
        session.commit()
        
        for p in all_products:
            session.refresh(p)

        print("Linking companies...")
        linkings = []
        for i in range(min(len(consumers), len(suppliers))):
            consumer = consumers[i]
            supplier = suppliers[i]
            
            existing = session.exec(select(Linkings).where(
                Linkings.consumer_company_id == consumer.company_id,
                Linkings.supplier_company_id == supplier.company_id
            )).first()
            
            if existing:
                linkings.append(existing)
                continue

            consumer_user = next(u for u in users if u.company_id == consumer.company_id)
            supplier_user = next(u for u in users if u.company_id == supplier.company_id)
            
            linking = Linkings(
                consumer_company_id=consumer.company_id,
                supplier_company_id=supplier.company_id,
                requested_by_user_id=consumer_user.user_id,
                responded_by_user_id=supplier_user.user_id,
                status=LinkingStatus.accepted
            )
            session.add(linking)
            linkings.append(linking)
            
        session.commit()
        
        for l in linkings:
            session.refresh(l)
            
        print("Creating orders...")
        for linking in linkings:
            existing_order = session.exec(select(Orders).where(Orders.linking_id == linking.linking_id)).first()
            if existing_order:
                continue

            consumer_user = next(u for u in users if u.company_id == linking.consumer_company_id)
            
            supplier_products = [p for p in all_products if p.company_id == linking.supplier_company_id]
            
            if not supplier_products:
                continue
                
            order = Orders(
                linking_id=linking.linking_id,
                consumer_staff_id=consumer_user.user_id,
                total_price=0,
                status=OrderStatus.created
            )
            session.add(order)
            session.commit()
            session.refresh(order)
            
            total_price = 0
            for product in supplier_products[:2]:
                qty = 5
                price = product.retail_price
                op = OrderProducts(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    product_quantity=qty,
                    product_price=price
                )
                session.add(op)
                total_price += qty * price
                
            order.total_price = total_price
            session.add(order)
            
        session.commit()
        print("Mock data created successfully!")

if __name__ == "__main__":
    create_mock_data()
