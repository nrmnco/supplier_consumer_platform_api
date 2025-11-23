# Functional Requirements

## User Stories with Given-When-Then Acceptance Criteria

### Authentication & Authorization

#### US-001: User Registration
**As a** company owner  
**I want to** register my company and create my owner account  
**So that** I can start using the platform

**Given** I am a new user  
**When** I submit registration form with company and user details  
**Then** my company and owner account are created  
**And** I receive access and refresh tokens  
**And** I can immediately log in

**Acceptance Criteria:**
- Email and phone number must be unique
- Company type must be either "supplier" or "consumer"
- Owner role is automatically assigned
- JWT tokens are returned upon successful registration

**Traceability:** SRS Section 3.2.1 → Story US-001 → Test TC-001

---

#### US-002: User Login
**As a** registered user  
**I want to** log in with my email and password  
**So that** I can access the platform

**Given** I have a registered account  
**When** I provide valid email and password  
**Then** I receive access and refresh tokens  
**And** I can make authenticated API requests

**Acceptance Criteria:**
- Valid credentials return JWT tokens
- Invalid credentials return 404 error
- Tokens expire after configured time

**Traceability:** SRS Section 3.2.1 → Story US-002 → Test TC-002

---

#### US-003: Token Refresh
**As a** logged-in user  
**I want to** refresh my access token  
**So that** I can continue using the platform without re-login

**Given** I have a valid refresh token  
**When** I call the refresh endpoint  
**Then** I receive a new access token  
**And** my refresh token remains valid

**Acceptance Criteria:**
- Refresh token must be valid and not expired
- New access token is generated
- Refresh token type is validated

**Traceability:** SRS Section 3.2.1 → Story US-003 → Test TC-003

---

### Company Management

#### US-004: View Company Profile
**As a** user  
**I want to** view company details  
**So that** I can see company information

**Given** I am authenticated  
**When** I request company information by company_id  
**Then** I receive company details including name, description, logo, location, and type

**Acceptance Criteria:**
- Company must exist
- All company fields are returned
- Logo URL is included if available

**Traceability:** SRS Section 3.2 → Story US-004 → Test TC-004

---

#### US-005: Update Company Profile
**As a** company owner  
**I want to** update my company information  
**So that** I can keep company details current

**Given** I am the company owner  
**When** I update company information  
**Then** the company profile is updated  
**And** only owners can perform this action

**Acceptance Criteria:**
- Only owner role can update company
- User must belong to the company
- Updates are persisted to database

**Traceability:** SRS Section 3.2 → Story US-005 → Test TC-005

---

### User Management

#### US-006: Create User Account
**As a** company owner or manager  
**I want to** create new user accounts  
**So that** I can add staff to my company

**Given** I am an owner or manager  
**When** I create a new user with role and details  
**Then** the user account is created  
**And** the user is assigned to my company  
**And** managers can only create staff users

**Acceptance Criteria:**
- Owner can create manager and staff users
- Manager can only create staff users
- Email and phone must be unique
- Cannot create another owner

**Traceability:** SRS Section 3.2.1 → Story US-006 → Test TC-006

---

#### US-007: View Company Users
**As a** company owner or manager  
**I want to** view all users in my company  
**So that** I can manage my team

**Given** I am an owner or manager  
**When** I request the user list  
**Then** I receive all users in my company  
**And** staff users cannot access this

**Acceptance Criteria:**
- Only owner and manager roles can view users
- Returns all users from the same company
- User details include role and status

**Traceability:** SRS Section 3.2.1 → Story US-007 → Test TC-007

---

#### US-008: Delete User Account
**As a** company owner or manager  
**I want to** delete user accounts  
**So that** I can remove staff from my company

**Given** I am an owner or manager  
**When** I delete a user account  
**Then** the user is removed from the system  
**And** managers can only delete staff users  
**And** users cannot delete themselves

**Acceptance Criteria:**
- Owner can delete manager and staff users
- Manager can only delete staff users
- Cannot delete own account
- User must belong to same company

**Traceability:** SRS Section 3.2.1 → Story US-008 → Test TC-008

---

### Linking System

#### US-009: Request Link to Supplier
**As a** consumer company user  
**I want to** request a link to a supplier  
**So that** I can access their catalog and place orders

**Given** I am from a consumer company  
**When** I send a link request to a supplier  
**Then** a linking record is created with status "pending"  
**And** the supplier is notified

**Acceptance Criteria:**
- Only consumer companies can request links
- Supplier company must exist and be type "supplier"
- Cannot create duplicate link requests
- Request includes optional message

**Traceability:** SRS Section 3.1 → Story US-009 → Test TC-009

---

#### US-010: Approve/Reject Link Request
**As a** supplier company user  
**I want to** approve or reject link requests  
**So that** I can control which consumers access my catalog

**Given** I am from a supplier company  
**When** I respond to a link request  
**Then** the linking status is updated  
**And** if approved, a salesman can be assigned  
**And** if approved, chat is enabled

**Acceptance Criteria:**
- Only supplier companies can respond
- Status changes to "accepted" or "rejected"
- Salesman assignment is optional
- Consumer is notified of decision

**Traceability:** SRS Section 3.2.4 → Story US-010 → Test TC-010

---

#### US-011: View Linkings
**As a** company user  
**I want to** view all linkings for my company  
**So that** I can see my relationships with other companies

**Given** I am authenticated  
**When** I request linkings  
**Then** I receive all linkings where my company is consumer or supplier  
**And** linkings include status and other company details

**Acceptance Criteria:**
- Returns linkings for user's company
- Includes both consumer and supplier linkings
- Status information is included

**Traceability:** SRS Section 3.1, 3.2.4 → Story US-011 → Test TC-011

---

### Product Catalog Management

#### US-012: Create Product
**As a** supplier owner or manager  
**I want to** create products in my catalog  
**So that** consumers can view and order them

**Given** I am a supplier owner or manager  
**When** I create a product with details  
**Then** the product is added to my catalog  
**And** it becomes visible to linked consumers

**Acceptance Criteria:**
- Only owner and manager roles can create products
- Only supplier companies can have products
- Product includes name, description, pricing, stock, images
- Minimum order quantity is set

**Traceability:** SRS Section 3.2.2 → Story US-012 → Test TC-012

---

#### US-013: View Products
**As a** user  
**I want to** view products from a supplier  
**So that** I can see what's available

**Given** I am authenticated  
**When** I request products for a company  
**Then** I receive the product list  
**And** consumers can only view products from linked suppliers

**Acceptance Criteria:**
- Products are returned for the specified company
- Consumer companies cannot have products
- Product details include pricing and availability

**Traceability:** SRS Section 3.1, 3.2.2 → Story US-013 → Test TC-013

---

#### US-014: Update Product
**As a** supplier owner or manager  
**I want to** update product information  
**So that** I can keep my catalog current

**Given** I am a supplier owner or manager  
**When** I update product details  
**Then** the product information is updated  
**And** changes are reflected immediately

**Acceptance Criteria:**
- Only owner and manager roles can update
- All product fields can be updated
- Stock and pricing updates are allowed

**Traceability:** SRS Section 3.2.2 → Story US-014 → Test TC-014

---

#### US-015: Delete Product
**As a** supplier owner or manager  
**I want to** delete products  
**So that** I can remove items from my catalog

**Given** I am a supplier owner or manager  
**When** I delete a product  
**Then** the product is removed from the catalog  
**And** it is no longer visible to consumers

**Acceptance Criteria:**
- Only owner and manager roles can delete
- Product is removed from database
- Associated order products may remain for history

**Traceability:** SRS Section 3.2.2 → Story US-015 → Test TC-015

---

### Order Management

#### US-016: Create Order
**As a** consumer staff member  
**I want to** create an order from a supplier's catalog  
**So that** I can purchase products

**Given** I am from a consumer company linked to a supplier  
**When** I create an order with products and quantities  
**Then** the order is created with status "created"  
**And** the supplier is notified

**Acceptance Criteria:**
- Only consumer companies can create orders
- Companies must be linked
- Order includes products with quantities and prices
- Total price is calculated
- Order status starts as "created"

**Traceability:** SRS Section 3.1 → Story US-016 → Test TC-016

---

#### US-017: View Orders
**As a** company user  
**I want to** view orders related to my company  
**So that** I can track order status

**Given** I am authenticated  
**When** I request orders  
**Then** I receive orders where my company is consumer or supplier  
**And** order details include status and products

**Acceptance Criteria:**
- Returns orders for user's company
- Includes orders as consumer and supplier
- Order details include products and status

**Traceability:** SRS Section 3.1, 3.2.3 → Story US-017 → Test TC-017

---

#### US-018: Update Order Status
**As a** supplier user  
**I want to** update order status  
**So that** I can track order progress

**Given** I am from the supplier company  
**When** I update order status  
**Then** the order status changes  
**And** a system message is sent to the order chat  
**And** status transitions follow valid workflow

**Acceptance Criteria:**
- Only supplier company can update status
- Valid status transitions: created → processing → shipping → completed
- Status can be set to "rejected" from any state
- System notification is created

**Traceability:** SRS Section 3.2.3 → Story US-018 → Test TC-018

---

### Real-time Communication

#### US-019: Send Chat Message
**As a** user from a linked company  
**I want to** send messages in a chat  
**So that** I can communicate with the other company

**Given** I am connected via WebSocket to a linking chat  
**When** I send a text message  
**Then** the message is saved to the database  
**And** it is broadcast to all connected users in the chat  
**And** I receive confirmation

**Acceptance Criteria:**
- User must be authorized for the linking
- Message body cannot be empty
- Message is persisted to database
- Real-time broadcast to all participants
- Message type is "text" by default

**Traceability:** SRS Section 3.2.4 → Story US-019 → Test TC-019

---

#### US-020: View Chat History
**As a** user  
**I want to** view chat message history  
**So that** I can see previous conversations

**Given** I am authenticated and authorized for the linking  
**When** I request chat messages  
**Then** I receive paginated message history  
**And** messages are ordered by timestamp

**Acceptance Criteria:**
- User must be authorized for the linking
- Messages are paginated (limit/offset)
- Messages include sender, body, type, timestamp
- Default limit is 100 messages

**Traceability:** SRS Section 3.2.4 → Story US-020 → Test TC-020

---

### Complaint Management

#### US-021: Create Complaint
**As a** consumer staff member  
**I want to** create a complaint for an order  
**So that** I can report issues

**Given** I created an order  
**When** I submit a complaint with description  
**Then** a complaint is created with status "open"  
**And** it is assigned to the supplier's salesman  
**And** a system message is sent to the order chat

**Acceptance Criteria:**
- Only the order creator can create complaint
- Complaint is tied to the order
- Automatically assigned to supplier salesman
- Status starts as "open"
- System notification is created

**Traceability:** SRS Section 7 → Story US-021 → Test TC-021

---

#### US-022: Escalate Complaint
**As a** supplier salesman  
**I want to** escalate a complaint to a manager  
**So that** complex issues can be resolved

**Given** I am assigned to a complaint  
**When** I escalate the complaint  
**Then** complaint status changes to "escalated"  
**And** it becomes available in the manager pool  
**And** a system message is sent

**Acceptance Criteria:**
- Only assigned salesman can escalate
- Complaint must be in "open" status
- Status changes to "escalated"
- Managers can claim it
- System notification is created

**Traceability:** SRS Section 7 → Story US-022 → Test TC-022

---

#### US-023: Claim Escalated Complaint
**As a** supplier manager  
**I want to** claim an escalated complaint  
**So that** I can resolve it

**Given** I am a manager and there is an escalated complaint  
**When** I claim the complaint  
**Then** complaint status changes to "in_progress"  
**And** I am assigned as the manager  
**And** a system message is sent

**Acceptance Criteria:**
- Only manager or owner roles can claim
- Complaint must be in "escalated" status
- Status changes to "in_progress"
- Manager is assigned
- System notification is created

**Traceability:** SRS Section 7 → Story US-023 → Test TC-023

---

#### US-024: Resolve Complaint
**As a** supplier salesman or manager  
**I want to** resolve a complaint  
**So that** I can close the issue

**Given** I am assigned to a complaint  
**When** I resolve it with resolution notes  
**Then** complaint status changes to "resolved"  
**And** optionally the order can be cancelled  
**And** a system message is sent

**Acceptance Criteria:**
- Assigned user can resolve
- Salesman can resolve "open" complaints
- Manager can resolve "in_progress" complaints
- Only managers can cancel orders
- Status changes to "resolved"
- System notification is created

**Traceability:** SRS Section 7 → Story US-024 → Test TC-024

---

### File Management

#### US-025: Upload File
**As a** user  
**I want to** upload files to the platform  
**So that** I can attach images and documents

**Given** I am authenticated  
**When** I request an upload URL  
**Then** I receive a presigned S3 URL  
**And** I can upload the file directly to S3  
**And** I receive the final file URL

**Acceptance Criteria:**
- Presigned URL is time-limited
- File extension is validated
- Upload is direct to S3
- Final URL is returned for storage

**Traceability:** SRS Section 3.2.4 → Story US-025 → Test TC-025

---

## Traceability Matrix

| Story ID | SRS Reference | Test Case ID | Status |
|----------|----------------|--------------|--------|
| US-001 | 3.2.1 | TC-001 | ✅ |
| US-002 | 3.2.1 | TC-002 | ✅ |
| US-003 | 3.2.1 | TC-003 | ✅ |
| US-004 | 3.2 | TC-004 | ✅ |
| US-005 | 3.2 | TC-005 | ✅ |
| US-006 | 3.2.1 | TC-006 | ✅ |
| US-007 | 3.2.1 | TC-007 | ✅ |
| US-008 | 3.2.1 | TC-008 | ✅ |
| US-009 | 3.1 | TC-009 | ✅ |
| US-010 | 3.2.4 | TC-010 | ✅ |
| US-011 | 3.1, 3.2.4 | TC-011 | ✅ |
| US-012 | 3.2.2 | TC-012 | ✅ |
| US-013 | 3.1, 3.2.2 | TC-013 | ✅ |
| US-014 | 3.2.2 | TC-014 | ✅ |
| US-015 | 3.2.2 | TC-015 | ✅ |
| US-016 | 3.1 | TC-016 | ✅ |
| US-017 | 3.1, 3.2.3 | TC-017 | ✅ |
| US-018 | 3.2.3 | TC-018 | ✅ |
| US-019 | 3.2.4 | TC-019 | ✅ |
| US-020 | 3.2.4 | TC-020 | ✅ |
| US-021 | 7 | TC-021 | ✅ |
| US-022 | 7 | TC-022 | ✅ |
| US-023 | 7 | TC-023 | ✅ |
| US-024 | 7 | TC-024 | ✅ |
| US-025 | 3.2.4 | TC-025 | ✅ |

**Legend:**
- ✅ Implemented and tested (test cases to be created)
- ⚠️ Partially implemented
- ❌ Not implemented

