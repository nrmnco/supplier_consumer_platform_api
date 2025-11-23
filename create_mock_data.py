import random
import httpx
import json
import time

BASE_URL = "http://localhost:8000"

def get_random_phone():
    return f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

class MockDataCreator:
    def __init__(self):
        self.companies = {}  # name -> {id, token, type, owner_email, users: []}
        self.products = {}   # company_name -> [product_ids]
        
        self.first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Jessica", "William", "Ashley", "James", "Linda", "Richard", "Patricia", "Thomas", "Elizabeth"]
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
        
        self.supplier_names = ["TechParts Inc.", "Global Foods", "BuildIt Materials", "Office Supplies Co.", "ChemWorks"]
        self.consumer_names = ["Gadget Store", "Restaurant Chain", "Construction Corp", "Corporate Office", "Lab Solutions"]
        
        self.logo_urls = [
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/1a37b342-ca35-4ef5-bbf7-9ab93548ac0f.jpg",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/058c400d-a105-41ab-94da-340ed4389348.png",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/448653f7-077a-4e8f-b1cb-bab74a2cf760.jpg",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/0095eb9e-1c3d-4669-8d8a-9c981f19524b.jpg",
            "https://csci361bucket.s3.eu-north-1.amazonaws.com/uploads/5f758e52-a038-433a-a563-9dded62271b6.jpg"
        ]

    def login(self, email, password):
        try:
            response = httpx.post(f"{BASE_URL}/auth/login", json={
                "email": email,
                "password": password
            })
            if response.status_code == 200:
                return response.json()["access_token"]
        except Exception as e:
            print(f"Login failed for {email}: {e}")
        return None

    def register_company(self, name, company_type, index):
        company_slug = name.replace(' ', '').replace('.', '').lower()
        owner_email = f"owner@{company_slug}.com"
        password = "password123"
        
        payload = {
            "company": {
                "name": name,
                "description": f"{company_type.capitalize()} of {name}",
                "logo_url": self.logo_urls[index % len(self.logo_urls)],
                "location": f"Location {index if company_type == 'supplier' else index + 5}",
                "company_type": company_type
            },
            "user": {
                "first_name": random.choice(self.first_names),
                "last_name": random.choice(self.last_names),
                "phone_number": get_random_phone(),
                "email": owner_email,
                "password": password,
                "role": "owner",
                "locale": "en"
            }
        }

        print(f"Creating {company_type} company: {name}...")
        response = httpx.post(f"{BASE_URL}/auth/register", json=payload)
        
        token = None
        company_id = None

        if response.status_code == 200:
            data = response.json()
            company_id = data["company_id"]
            token = data["access_token"]
            print(f"  -> Created successfully (ID: {company_id})")
        elif response.status_code == 409:
            print(f"  -> Company/User already exists, logging in...")
            token = self.login(owner_email, password)
            if token:
                # Fetch company ID
                headers = {"Authorization": f"Bearer {token}"}
                user_resp = httpx.get(f"{BASE_URL}/user/me", headers=headers)
                if user_resp.status_code == 200:
                    company_id = user_resp.json()["company_id"]
                    print(f"  -> Logged in successfully (ID: {company_id})")
        else:
            print(f"  -> Failed: {response.text}")

        if company_id and token:
            self.companies[name] = {
                "id": company_id,
                "token": token,
                "type": company_type,
                "owner_email": owner_email,
                "users": []
            }

    def create_users(self):
        print("\nCreating users...")
        for name, info in self.companies.items():
            company_slug = name.replace(' ', '').replace('.', '').lower()
            headers = {"Authorization": f"Bearer {info['token']}"}
            
            roles = []
            if info['type'] == 'supplier':
                roles.append("manager")
            roles.append("staff")
            
            for role in roles:
                email = f"{role}@{company_slug}.com"
                payload = {
                    "first_name": random.choice(self.first_names),
                    "last_name": random.choice(self.last_names),
                    "phone_number": get_random_phone(),
                    "email": email,
                    "password": "password123",
                    "role": role,
                    "locale": "en"
                }
                
                print(f"  -> Creating {role} for {name} ({email})...")
                response = httpx.post(f"{BASE_URL}/user/", json=payload, headers=headers)
                
                if response.status_code == 200:
                    print("    -> Created")
                elif response.status_code == 400 and "already exists" in response.text:
                    print("    -> Already exists")
                else:
                    print(f"    -> Failed: {response.text}")

    def create_products(self):
        print("\nCreating products...")
        for name, info in self.companies.items():
            if info['type'] != 'supplier':
                continue
                
            headers = {"Authorization": f"Bearer {info['token']}"}
            
            # Check existing products
            resp = httpx.get(f"{BASE_URL}/products/?company_id={info['id']}", headers=headers)
            current_count = 0
            if resp.status_code == 200:
                current_count = len(resp.json().get("products", []))
            
            if current_count >= 5:
                print(f"  -> {name} already has {current_count} products, skipping...")
                # Store product IDs for later
                self.products[name] = [p['product_id'] for p in resp.json().get("products", [])]
                continue

            self.products[name] = []
            for j in range(5):
                payload = {
                    "name": f"Product {j} of {name}",
                    "description": f"Description for product {j}",
                    "picture_url": [self.logo_urls[j % len(self.logo_urls)]],
                    "stock_quantity": 100,
                    "retail_price": 100 + j * 10,
                    "threshold": 10,
                    "bulk_price": 90 + j * 10,
                    "minimum_order": 1,
                    "unit": "pcs"
                }
                
                print(f"  -> Creating product {j} for {name}...")
                response = httpx.post(f"{BASE_URL}/products/", json=payload, headers=headers)
                
                if response.status_code == 200:
                    prod_data = response.json().get("product")
                    if prod_data:
                        self.products[name].append(prod_data['product_id'])
                    print("    -> Created")
                else:
                    print(f"    -> Failed: {response.text}")

    def create_linkings(self):
        print("\nLinking companies...")
        # Link i-th consumer to i-th supplier
        for i in range(min(len(self.consumer_names), len(self.supplier_names))):
            consumer_name = self.consumer_names[i]
            supplier_name = self.supplier_names[i]
            
            if consumer_name not in self.companies or supplier_name not in self.companies:
                continue
                
            consumer = self.companies[consumer_name]
            supplier = self.companies[supplier_name]
            
            print(f"  -> Linking {consumer_name} -> {supplier_name}...")
            
            # 1. Consumer requests link
            headers_consumer = {"Authorization": f"Bearer {consumer['token']}"}
            payload = {"message": "We would like to connect."}
            
            resp = httpx.post(f"{BASE_URL}/linkings/?company_id={supplier['id']}", json=payload, headers=headers_consumer)
            
            linking_id = None
            if resp.status_code == 200:
                linking_id = resp.json()["linking"]["linking_id"]
                print("    -> Request sent")
            elif resp.status_code == 400 and "Already sent" in resp.text:
                print("    -> Request already sent")
                # Try to find existing linking ID
                # This is a bit tricky without a direct "get linking by pair" endpoint that returns ID easily
                # But we can list linkings for consumer
                l_resp = httpx.get(f"{BASE_URL}/linkings/", headers=headers_consumer)
                if l_resp.status_code == 200:
                    for l in l_resp.json().get("linkings", []):
                        if l["supplier_company_id"] == supplier["id"]:
                            linking_id = l["linking_id"]
                            break
            else:
                print(f"    -> Failed to request: {resp.text}")
                continue

            if linking_id:
                # 2. Supplier accepts link
                headers_supplier = {"Authorization": f"Bearer {supplier['token']}"}
                resp = httpx.patch(f"{BASE_URL}/linkings/supplier_response/{linking_id}?status=accepted", headers=headers_supplier)
                if resp.status_code == 200:
                    print("    -> Accepted by supplier")
                else:
                    print(f"    -> Failed to accept: {resp.text}")

    def create_orders(self):
        print("\nCreating orders...")
        for i in range(min(len(self.consumer_names), len(self.supplier_names))):
            consumer_name = self.consumer_names[i]
            supplier_name = self.supplier_names[i]
            
            if consumer_name not in self.companies or supplier_name not in self.companies:
                continue
                
            consumer = self.companies[consumer_name]
            supplier = self.companies[supplier_name]
            
            supplier_prod_ids = self.products.get(supplier_name, [])
            if not supplier_prod_ids:
                continue
                
            headers_consumer = {"Authorization": f"Bearer {consumer['token']}"}
            
            # Check if order already exists (simple check: get all orders for consumer)
            # This might be too broad but matches the original script's intent roughly
            resp = httpx.get(f"{BASE_URL}/orders/", headers=headers_consumer)
            has_orders = False
            if resp.status_code == 200:
                # The endpoint returns list of orders
                orders = resp.json()
                # We can't easily filter by supplier here without fetching details, 
                # but let's just create one if the list is empty or small
                if len(orders) > 0:
                    # Check if any order is with this supplier? 
                    # For simplicity, let's just create one if we haven't tracked it yet
                    pass 
            
            print(f"  -> Creating order from {consumer_name} to {supplier_name}...")
            
            products_payload = []
            for pid in supplier_prod_ids[:2]:
                products_payload.append({
                    "product_id": pid,
                    "quantity": 5
                })
            
            payload = {"products": products_payload}
            
            resp = httpx.post(f"{BASE_URL}/orders/?supplier_company_id={supplier['id']}", json=payload, headers=headers_consumer)
            
            if resp.status_code == 200:
                print("    -> Order created")
            else:
                print(f"    -> Failed to create order: {resp.text}")

    def run(self):
        # 1. Create Suppliers
        for i, name in enumerate(self.supplier_names):
            self.register_company(name, "supplier", i)
            
        # 2. Create Consumers
        for i, name in enumerate(self.consumer_names):
            self.register_company(name, "consumer", i)
            
        # 3. Create Users
        self.create_users()
        
        # 4. Create Products
        self.create_products()
        
        # 5. Link Companies
        self.create_linkings()
        
        # 6. Create Orders
        self.create_orders()
        
        print("\nMock data creation complete!")

if __name__ == "__main__":
    creator = MockDataCreator()
    creator.run()
