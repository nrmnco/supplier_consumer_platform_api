# API Section

## OpenAPI Summary

The SCP Backend API is built using FastAPI, which automatically generates OpenAPI (Swagger) documentation. The API follows RESTful principles and uses JWT-based authentication.

**Base URL:** `http://localhost:8000` (development)  
**API Documentation:** Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)  
**OpenAPI Schema:** Available at `/openapi.json`

---

## Endpoints Overview

### Authentication Endpoints (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register company with owner account | No |
| POST | `/auth/login` | User login | No |
| POST | `/auth/refresh` | Refresh access token | No (refresh token) |

### User Management Endpoints (`/user`)

| Method | Endpoint | Description | Auth Required | RBAC |
|--------|----------|-------------|---------------|------|
| GET | `/user/me` | Get current user profile | Yes | All |
| GET | `/user/get-user` | Get user by ID | Yes | All |
| GET | `/user/` | Get all users in company | Yes | Owner, Manager |
| POST | `/user/` | Create new user | Yes | Owner, Manager |
| PUT | `/user/{user_id}` | Update user profile | Yes | Owner (or self) |
| DELETE | `/user/{user_id}` | Delete user | Yes | Owner, Manager |

### Company Management Endpoints (`/company`)

| Method | Endpoint | Description | Auth Required | RBAC |
|--------|----------|-------------|---------------|------|
| GET | `/company/get-company` | Get company by ID | Yes | All |
| GET | `/company/` | Get all companies (consumers only) | Yes | Consumer |
| PUT | `/company/{company_id}` | Update company profile | Yes | Owner |

### Linking Endpoints (`/linkings`)

| Method | Endpoint | Description | Auth Required | RBAC |
|--------|----------|-------------|---------------|------|
| POST | `/linkings/` | Create link request | Yes | Consumer |
| GET | `/linkings/` | Get all linkings for company | Yes | All |
| GET | `/linkings/status/{other_company_id}` | Get linking status | Yes | All |
| PATCH | `/linkings/supplier_response/{linking_id}` | Approve/reject link | Yes | Supplier |

### Product Catalog Endpoints (`/products`)

| Method | Endpoint | Description | Auth Required | RBAC |
|--------|----------|-------------|---------------|------|
| GET | `/products/` | Get products for company | Yes | All |
| GET | `/products/{product_id}` | Get product by ID | Yes | All |
| POST | `/products/` | Create product | Yes | Owner, Manager (Supplier) |
| PUT | `/products/{product_id}` | Update product | Yes | Owner, Manager (Supplier) |
| DELETE | `/products/{product_id}` | Delete product | Yes | Owner, Manager (Supplier) |

### Order Management Endpoints (`/orders`)

| Method | Endpoint | Description | Auth Required | RBAC |
|--------|----------|-------------|---------------|------|
| POST | `/orders/` | Create order | Yes | Consumer Staff |
| GET | `/orders/` | Get all orders for company | Yes | All |
| GET | `/orders/{order_id}` | Get order by ID | Yes | All (linked companies) |
| PATCH | `/orders/{order_id}/status` | Update order status | Yes | Supplier |
| GET | `/orders/linking/{linking_id}` | Get orders by linking | Yes | All (linked companies) |

### Chat Endpoints (`/chat`)

| Method | Endpoint | Description | Auth Required | Protocol |
|--------|----------|-------------|---------------|----------|
| WebSocket | `/chat/ws/{linking_id}` | WebSocket chat for linking | Yes (token in query) | WebSocket |
| GET | `/chat/messages/{linking_id}` | Get chat history | Yes | HTTP |
| WebSocket | `/chat/ws/order/{order_id}` | WebSocket chat for order | Yes (token in query) | WebSocket |
| GET | `/chat/messages/order/{order_id}` | Get order chat history | Yes | HTTP |

### Complaint Management Endpoints (`/complaints`)

| Method | Endpoint | Description | Auth Required | RBAC |
|--------|----------|-------------|---------------|------|
| POST | `/complaints/order/{order_id}` | Create complaint | Yes | Consumer (order creator) |
| GET | `/complaints/my-complaints` | Get user's complaints | Yes | Consumer |
| GET | `/complaints/assigned-to-me` | Get assigned complaints | Yes | Staff, Manager, Owner |
| GET | `/complaints/escalated` | Get escalated complaints | Yes | Manager, Owner |
| GET | `/complaints/my-managed-complaints` | Get managed complaints | Yes | Manager, Owner |
| GET | `/complaints/company` | Get all company complaints | Yes | Owner |
| GET | `/complaints/{complaint_id}` | Get complaint details | Yes | Authorized users |
| GET | `/complaints/{complaint_id}/history` | Get complaint history | Yes | Authorized users |
| PUT | `/complaints/{complaint_id}/escalate` | Escalate complaint | Yes | Assigned Salesman |
| PUT | `/complaints/{complaint_id}/claim` | Claim escalated complaint | Yes | Manager, Owner |
| PUT | `/complaints/{complaint_id}/resolve` | Resolve complaint | Yes | Assigned user |
| PUT | `/complaints/{complaint_id}/close` | Close complaint | Yes | Assigned Manager |
| GET | `/complaints/order/{order_id}` | Get complaint by order | Yes | Authorized users |
| GET | `/complaints/order/{order_id}/exists` | Check if complaint exists | Yes | Authorized users |

### File Upload Endpoints (`/uploads`)

| Method | Endpoint | Description | Auth Required | RBAC |
|--------|----------|-------------|---------------|------|
| GET | `/uploads/upload-url` | Get presigned S3 upload URL | Yes | All |
| POST | `/uploads/companies/{company_id}/photo` | Store company logo URL | Yes | Owner |
| DELETE | `/uploads/delete-file` | Delete file from S3 | Yes | All |

### City Endpoints (`/cities`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/cities/get-all-cities` | Get all cities | No |

---

## Request/Response Examples

### Authentication

#### Register
**Request:**
```http
POST /auth/register
Content-Type: application/json

{
  "user": {
    "email": "owner@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+77001234567",
    "role": "owner"
  },
  "company": {
    "name": "Example Supplier Co",
    "description": "Food supplier",
    "location": "Almaty",
    "company_type": "supplier"
  }
}
```

**Response:**
```json
{
  "company_id": 1,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Login
**Request:**
```http
POST /auth/login
Content-Type: application/json

{
  "email": "owner@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create Order
**Request:**
```http
POST /orders/?supplier_company_id=1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "products": [
    {
      "product_id": 1,
      "quantity": 10,
      "price": 5000
    },
    {
      "product_id": 2,
      "quantity": 5,
      "price": 3000
    }
  ]
}
```

**Response:**
```json
{
  "order": {
    "order_id": 1,
    "linking_id": 1,
    "consumer_staff_id": 2,
    "total_price": 65000,
    "status": "created",
    "created_at": "2025-01-15T10:30:00",
    "updated_at": "2025-01-15T10:30:00"
  }
}
```

### Create Complaint
**Request:**
```http
POST /complaints/order/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "description": "Products received were damaged"
}
```

**Response:**
```json
{
  "message": "Complaint created successfully",
  "complaint": {
    "complaint_id": 1,
    "order_id": 1,
    "assigned_to_salesman_id": 3,
    "status": "open",
    "description": "Products received were damaged",
    "created_at": "2025-01-15T11:00:00",
    "updated_at": "2025-01-15T11:00:00"
  }
}
```

---

## Role-Based Access Control (RBAC)

### Role Hierarchy

1. **Owner** - Full company control
   - Can create/delete managers and staff
   - Can update company profile
   - Can delete company account
   - Can access all company data

2. **Manager** - Management capabilities
   - Can create/delete staff (not managers)
   - Can manage catalog (products)
   - Can handle orders
   - Can resolve escalated complaints

3. **Staff** - Limited permissions
   - Consumer Staff: Can place orders, create complaints
   - Supplier Staff (Sales Rep): Can handle communications, first-line complaints

### Permission Matrix

| Action | Owner | Manager | Staff (Consumer) | Staff (Supplier) |
|--------|-------|---------|-----------------|------------------|
| Create User (Manager) | ✅ | ❌ | ❌ | ❌ |
| Create User (Staff) | ✅ | ✅ | ❌ | ❌ |
| Delete User | ✅ | ✅ (Staff only) | ❌ | ❌ |
| Update Company | ✅ | ❌ | ❌ | ❌ |
| Create Product | ✅ | ✅ | ❌ | ❌ |
| Update Product | ✅ | ✅ | ❌ | ❌ |
| Delete Product | ✅ | ✅ | ❌ | ❌ |
| Create Order | ❌ | ❌ | ✅ | ❌ |
| Update Order Status | ✅ | ✅ | ❌ | ✅ |
| Create Complaint | ❌ | ❌ | ✅ | ❌ |
| Escalate Complaint | ✅ | ❌ | ❌ | ✅ |
| Claim Complaint | ✅ | ✅ | ❌ | ❌ |
| Resolve Complaint | ✅ | ✅ | ✅ (own) | ✅ (assigned) |
| Approve/Reject Link | ✅ | ✅ | ✅ | ✅ |
| Request Link | ❌ | ❌ | ✅ | ❌ |

---

## Error Model

The API uses standard HTTP status codes and returns error details in JSON format.

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH requests |
| 201 | Created | Successful POST requests (if resource created) |
| 400 | Bad Request | Invalid request data, validation errors |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Insufficient permissions for the action |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists (duplicate email, etc.) |
| 500 | Internal Server Error | Server-side errors |

### Error Examples

#### 400 Bad Request
```json
{
  "detail": "Invalid status value. Must be one of: created, processing, shipping, completed, rejected"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Token has expired"
}
```

#### 403 Forbidden
```json
{
  "detail": "Insufficient permissions to create product"
}
```

#### 404 Not Found
```json
{
  "detail": "User not found"
}
```

#### 409 Conflict
```json
{
  "detail": "User with this email already exists"
}
```

---

## Authentication

### JWT Token Structure

**Access Token:**
- Expires: 15 minutes (configurable)
- Contains: `sub` (email), `exp`, `type: "access"`

**Refresh Token:**
- Expires: 7 days (configurable)
- Contains: `sub` (email), `exp`, `type: "refresh"`

### Token Usage

1. Include access token in Authorization header:
   ```http
   Authorization: Bearer {access_token}
   ```

2. For WebSocket connections, include token as query parameter:
   ```
   ws://localhost:8000/chat/ws/{linking_id}?token={access_token}
   ```

3. Refresh expired access token:
   ```http
   POST /auth/refresh
   Content-Type: application/json
   
   { "refresh_token": "{refresh_token}" }
   ```

---

## WebSocket API

### Connection

**Endpoint:** `ws://localhost:8000/chat/ws/{linking_id}?token={access_token}`

**Connection Flow:**
1. Client connects with token in query parameter
2. Server validates token
3. Server checks user authorization for linking
4. Server accepts connection and sends confirmation
5. Client can send/receive messages

### Message Format

**Client → Server:**
```json
{
  "body": "Hello, this is a message",
  "type": "text"
}
```

**Server → Client:**
```json
{
  "type": "message",
  "message_id": 1,
  "chat_id": 1,
  "sender_id": 2,
  "sender_name": "John Doe",
  "body": "Hello, this is a message",
  "message_type": "text",
  "sent_at": "2025-01-15T10:30:00"
}
```

**Connection Confirmation:**
```json
{
  "type": "connection",
  "message": "Connected to chat",
  "chat_id": 1,
  "linking_id": 1
}
```

---

## API Versioning

Currently, the API does not implement versioning. Future versions may use:
- URL versioning: `/api/v1/...`
- Header versioning: `Accept: application/vnd.scp.v1+json`

---

## Rate Limiting

**Status:** ⚠️ Not implemented (TODO)

Future implementation should include:
- Rate limiting per user/IP
- Different limits for authenticated vs unauthenticated requests
- Protection against DDoS attacks

---

## OpenAPI Documentation

FastAPI automatically generates OpenAPI 3.0 specification:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

The OpenAPI specification includes:
- All endpoints with methods
- Request/response schemas
- Authentication requirements
- Example requests and responses
- Error responses

