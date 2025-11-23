# Models and Diagrams

## Context Diagram

The system context diagram shows the SCP platform interacting with external entities and systems.

**External Entities:**
- **Consumers** (Restaurants/Hotels) - Use mobile and web applications
- **Suppliers** - Use web application for management, mobile for sales representatives
- **AWS S3** - External file storage service for images and documents
- **PostgreSQL Database** - Data persistence layer

**System Boundary:**
- **SCP Backend API** - Core platform providing REST API and WebSocket services

**Interactions:**
- Consumers and Suppliers interact with the platform via HTTP/WebSocket
- Platform stores files in AWS S3
- Platform persists data in PostgreSQL database

*Note: A detailed context diagram should be created using PlantUML or similar tool. Reference: `docs/diagrams/src/component-diagram.puml`*

---

## Use Case Diagram

The use case diagram illustrates all system functionalities organized by user roles.

**Key Use Cases:**

### Consumer Use Cases
- Request Link to Supplier
- Browse Catalog
- Place Order
- Track Order
- Submit Complaint
- Chat with Supplier
- Create Manager Account (Owner)
- Create Staff Account (Manager/Owner)
- Delete Accounts (Owner)

### Supplier Use Cases
- Approve/Deny Link Request (Sales Rep)
- Handle First-Line Complaint (Sales Rep)
- Escalate Complaint (Sales Rep)
- Chat with Consumer (Sales Rep)
- Manage Catalog (Manager)
- Manage Inventory (Manager)
- Accept/Reject Order (Manager)
- Resolve Escalated Complaint (Manager)
- Create Manager Account (Owner)
- Create Staff Account (Owner)
- Delete Accounts (Owner)

**Diagram Location:** `docs/diagrams/src/use-case.puml`  
**Generated PDF:** `docs/diagrams/out/use-case.pdf`

---

## Activity Diagrams (Key Flows)

### Flow 1: Order Creation and Processing

**Actors:** Consumer Staff, Supplier Manager

**Steps:**
1. Consumer Staff browses supplier catalog (after linking approval)
2. Consumer Staff selects products and quantities
3. Consumer Staff creates order
4. Order status: "created"
5. Supplier Manager receives order notification
6. Supplier Manager reviews order
7. Supplier Manager accepts or rejects order
8. If accepted: Order status → "processing"
9. Supplier Manager updates order status: "processing" → "shipping" → "completed"
10. Consumer Staff tracks order status

**Diagram Location:** `docs/diagrams/src/main-activity-diagram.puml`  
**Generated PDF:** `docs/diagrams/out/main-activity-diagram.pdf`

### Flow 2: Complaint Escalation

**Actors:** Consumer Staff, Sales Representative, Manager, Owner

**Steps:**
1. Consumer Staff creates complaint for an order
2. Complaint status: "open", assigned to Sales Representative
3. Sales Representative attempts resolution
4. If unresolved: Sales Representative escalates to Manager
5. Complaint status: "escalated"
6. Manager claims complaint from pool
7. Complaint status: "in_progress", assigned to Manager
8. Manager resolves complaint
9. Complaint status: "resolved"
10. Optionally: Manager can cancel order if complaint is severe

**Diagram Location:** `docs/diagrams/src/activity-sequence-diagrams.tex`  
**Generated PDF:** `docs/diagrams/out/activity-sequence-diagrams.pdf`

### Flow 3: Linking Request Workflow

**Actors:** Consumer Staff, Supplier Staff/Manager

**Steps:**
1. Consumer Staff requests link to supplier
2. Linking status: "pending"
3. Supplier Staff/Manager reviews request
4. Supplier approves or rejects
5. If approved:
   - Linking status: "accepted"
   - Sales Representative assigned (optional)
   - Chat channel created
6. Consumer can now browse catalog and place orders

---

## ERD (Entity Relationship Diagram) + Data Dictionary

### Entity Relationship Diagram

The ERD shows all database entities and their relationships.

**Core Entities:**

1. **Users** - User accounts with roles (Owner, Manager, Staff)
2. **Companies** - Supplier or Consumer companies
3. **Products** - Products in supplier catalogs
4. **Linkings** - Relationships between consumers and suppliers
5. **Orders** - Purchase orders from consumers
6. **OrderProducts** - Association table for order items
7. **Chats** - Chat channels (linking-based or order-based)
8. **Messages** - Chat messages
9. **Complaints** - Complaints raised on orders
10. **ComplaintHistory** - History of complaint status changes
11. **Cities** - City data with multi-language support

**Key Relationships:**
- Company 1:N Users (one company has many users)
- Company 1:N Products (one supplier has many products)
- Company 1:N Linkings (as consumer or supplier)
- Linking 1:N Orders (one linking has many orders)
- Order 1:N OrderProducts (one order has many order products)
- Product 1:N OrderProducts (one product in many orders)
- Linking 1:N Chats (one linking has chat)
- Order 0:1 Chat (one order may have chat)
- Chat 1:N Messages (one chat has many messages)
- Order 0:1 Complaint (one order may have complaint)
- Complaint 1:N ComplaintHistory (one complaint has history)

**Diagram Location:** `docs/diagrams/src/class-diagram.puml` (class diagram represents ERD)  
**Generated PDF:** `docs/diagrams/out/class-diagram.pdf`

### Data Dictionary

#### Users Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| user_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| company_id | INTEGER | FOREIGN KEY → companies.company_id, NOT NULL | Company the user belongs to |
| status | ENUM | NOT NULL, DEFAULT 'active' | User status: active, suspended |
| first_name | VARCHAR | NOT NULL | User's first name |
| last_name | VARCHAR | NOT NULL | User's last name |
| phone_number | VARCHAR | NOT NULL, UNIQUE, INDEXED | User's phone number |
| email | VARCHAR | NOT NULL, UNIQUE, INDEXED | User's email address |
| hashed_password | VARCHAR | NOT NULL | Argon2-hashed password |
| role | ENUM | NOT NULL | User role: owner, manager, staff |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| locale | ENUM | NOT NULL, DEFAULT 'en' | User locale: en, ru, kz |

#### Companies Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| company_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique company identifier |
| status | ENUM | NOT NULL, DEFAULT 'active' | Company status: active, suspended |
| name | VARCHAR | NOT NULL | Company name |
| description | TEXT | NULLABLE | Company description |
| logo_url | VARCHAR | NULLABLE | URL to company logo (S3) |
| location | VARCHAR | NOT NULL | Company location |
| company_type | ENUM | NOT NULL | Company type: supplier, consumer |

#### Products Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| product_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique product identifier |
| company_id | INTEGER | FOREIGN KEY → companies.company_id, NULLABLE | Supplier company ID |
| name | VARCHAR | NOT NULL | Product name |
| description | TEXT | NULLABLE | Product description |
| picture_url | JSON | NULLABLE | Array of image URLs |
| stock_quantity | INTEGER | NOT NULL, DEFAULT 0 | Available stock quantity |
| retail_price | INTEGER | NOT NULL | Retail price (in smallest currency unit) |
| threshold | INTEGER | NULLABLE | Quantity threshold for bulk pricing |
| bulk_price | INTEGER | NULLABLE | Bulk price (in smallest currency unit) |
| minimum_order | INTEGER | NOT NULL, DEFAULT 1 | Minimum order quantity |
| unit | VARCHAR | NOT NULL | Product unit (kg, piece, etc.) |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | Product availability flag |

#### Linkings Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| linking_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique linking identifier |
| consumer_company_id | INTEGER | FOREIGN KEY → companies.company_id, NOT NULL | Consumer company ID |
| supplier_company_id | INTEGER | FOREIGN KEY → companies.company_id, NOT NULL | Supplier company ID |
| requested_by_user_id | INTEGER | FOREIGN KEY → users.user_id, NOT NULL | User who requested link |
| responded_by_user_id | INTEGER | FOREIGN KEY → users.user_id, NULLABLE | User who responded |
| assigned_salesman_user_id | INTEGER | FOREIGN KEY → users.user_id, NULLABLE | Assigned sales representative |
| status | ENUM | NOT NULL, DEFAULT 'pending' | Linking status: pending, accepted, rejected, unlinked |
| message | TEXT | NULLABLE | Optional message with request/response |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Request creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

#### Orders Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| order_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique order identifier |
| linking_id | INTEGER | FOREIGN KEY → linkings.linking_id, NOT NULL | Associated linking |
| consumer_staff_id | INTEGER | FOREIGN KEY → users.user_id, NOT NULL | User who created order |
| total_price | INTEGER | NOT NULL | Total order price (in smallest currency unit) |
| status | ENUM | NOT NULL, DEFAULT 'created' | Order status: created, processing, shipping, completed, rejected |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Order creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

#### OrderProducts Table (Association)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| order_product_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| order_id | INTEGER | FOREIGN KEY → orders.order_id, NOT NULL | Associated order |
| product_id | INTEGER | FOREIGN KEY → products.product_id, NOT NULL | Associated product |
| product_quantity | INTEGER | NOT NULL | Quantity ordered |
| product_price | INTEGER | NOT NULL | Price at time of order (in smallest currency unit) |

#### Chats Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| chat_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique chat identifier |
| linking_id | INTEGER | FOREIGN KEY → linkings.linking_id, NULLABLE | Associated linking (for general chat) |
| order_id | INTEGER | FOREIGN KEY → orders.order_id, NULLABLE | Associated order (for order-specific chat) |

#### Messages Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| message_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique message identifier |
| chat_id | INTEGER | FOREIGN KEY → chats.chat_id, NOT NULL | Associated chat |
| sender_id | INTEGER | FOREIGN KEY → users.user_id, NOT NULL | Message sender |
| type | ENUM | NOT NULL, DEFAULT 'text' | Message type: text, system |
| body | TEXT | NOT NULL | Message content |
| sent_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

#### Complaints Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| complaint_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique complaint identifier |
| order_id | INTEGER | FOREIGN KEY → orders.order_id, NOT NULL | Associated order |
| assigned_to_salesman_id | INTEGER | FOREIGN KEY → users.user_id, NOT NULL | Assigned sales representative |
| escalated_to_manager_id | INTEGER | FOREIGN KEY → users.user_id, NULLABLE | Assigned manager (if escalated) |
| escalated_to_owner_id | INTEGER | FOREIGN KEY → users.user_id, NULLABLE | Assigned owner (if further escalated) |
| status | ENUM | NOT NULL, DEFAULT 'open' | Complaint status: open, in_progress, escalated, resolved, closed |
| description | TEXT | NOT NULL | Complaint description |
| resolution_notes | TEXT | NULLABLE | Resolution notes |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Complaint creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

#### ComplaintHistory Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| history_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique history entry identifier |
| complaint_id | INTEGER | FOREIGN KEY → complaints.complaint_id, NOT NULL | Associated complaint |
| changed_by_user_id | INTEGER | FOREIGN KEY → users.user_id, NOT NULL | User who made the change |
| new_status | ENUM | NOT NULL | New status after change |
| notes | TEXT | NULLABLE | Optional notes about the change |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Change timestamp |

#### Cities Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| city_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique city identifier |
| city_name | VARCHAR | NOT NULL | City name in English |
| city_name_ru | VARCHAR | NOT NULL | City name in Russian |
| city_name_kz | VARCHAR | NOT NULL | City name in Kazakh |

---

## Sequence Diagrams

### Sequence Diagram 1: Order Creation Flow

**Actors:** Consumer Staff, Supplier Manager  
**Components:** Mobile/Web App, Backend API, Order Service, Database

**Sequence:**
1. Consumer Staff → App: Browse catalog, select products
2. App → API: POST /orders/ (order data)
3. API → Order Service: create_order()
4. Order Service → Database: Insert order and order_products
5. Database → Order Service: Return order_id
6. Order Service → API: Return order object
7. API → App: Return order confirmation
8. App → Consumer Staff: Display order created
9. API → Supplier Manager: Notify new order (via WebSocket/system message)

**Diagram Location:** `docs/diagrams/src/sequence-diagram.puml`  
**Generated PDF:** `docs/diagrams/out/sequence-diagram.pdf`

### Sequence Diagram 2: Complaint Escalation Flow

**Actors:** Consumer Staff, Sales Representative, Manager  
**Components:** Mobile/Web App, Backend API, Complaint Service, Chat Service, Database

**Sequence:**
1. Consumer Staff → App: Create complaint for order
2. App → API: POST /complaints/order/{order_id}
3. API → Complaint Service: create_complaint()
4. Complaint Service → Database: Insert complaint (status: "open")
5. Complaint Service → Chat Service: Create system message
6. Chat Service → Database: Insert message
7. Database → Complaint Service: Return complaint
8. Complaint Service → API: Return complaint
9. API → App: Return complaint confirmation
10. App → Sales Representative: Notify new complaint
11. Sales Representative → App: Attempt resolution
12. Sales Representative → App: Escalate complaint
13. App → API: PUT /complaints/{id}/escalate
14. API → Complaint Service: escalate_complaint()
15. Complaint Service → Database: Update complaint (status: "escalated")
16. Complaint Service → Chat Service: Create system message
17. API → Manager: Notify escalated complaint (available in pool)
18. Manager → App: Claim complaint
19. App → API: PUT /complaints/{id}/claim
20. API → Complaint Service: claim_complaint()
21. Complaint Service → Database: Update complaint (status: "in_progress", assign manager)
22. API → App: Return updated complaint
23. App → Manager: Display complaint for resolution

**Diagram Location:** `docs/diagrams/src/sequence-diagram.puml`  
**Generated PDF:** `docs/diagrams/out/sequence-diagram.pdf`

---

## Component Diagram

The component diagram shows the system architecture and component interactions.

**Components:**
- **Frontend Components:**
  - Web Frontend (Supplier) - Catalogs, Orders, Complaints, Auth, Link Management, Chat
  - Mobile App (Supplier & Consumer) - Same features as web

- **Backend Components:**
  - Catalogs API / Service
  - Orders API / Service
  - Complaint API / Service
  - Auth API / Service
  - Link API / Service
  - Chat API / Service
  - Database (PostgreSQL)

**Diagram Location:** `docs/diagrams/src/component-diagram.puml`  
**Generated PDF:** `docs/diagrams/out/component-diagram.pdf`

---

## Information Engineering Diagram

The information engineering diagram shows data flow and relationships.

**Diagram Location:** `docs/diagrams/src/information-engineering.puml`  
**Generated PDF:** `docs/diagrams/out/information-engineering.pdf`

---

## Diagram Generation

All diagrams are created using PlantUML and can be regenerated using:

```bash
./export-diagrams.sh
```

Or manually using:

```bash
java -jar plantuml.jar docs/diagrams/src/*.puml -o ../out
```

**Note:** All generated PDFs are available in `docs/diagrams/out/` directory.

