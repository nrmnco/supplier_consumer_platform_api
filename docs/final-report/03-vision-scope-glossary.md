# Vision & Scope

## Vision Statement

The Supplier Consumer Platform (SCP) aims to revolutionize B2B food supply chain management by providing a secure, efficient, and user-friendly digital platform that connects food suppliers with institutional consumers (restaurants and hotels). The platform eliminates traditional communication barriers, streamlines ordering processes, and ensures transparent, accountable business relationships through integrated order tracking, real-time communication, and comprehensive complaint resolution mechanisms.

## Scope

### In Scope (MVP)

The current implementation focuses on the core MVP functionality:

1. **Authentication & Authorization**
   - User registration with company creation
   - JWT-based authentication (access and refresh tokens)
   - Role-based access control (Owner, Manager, Staff)
   - Multi-company support (Supplier and Consumer types)

2. **Company Management**
   - Company registration and profile management
   - Company logo upload via AWS S3
   - Company status management (active/suspended)

3. **User Management**
   - User creation with role assignment
   - User profile updates
   - User deletion (with role-based restrictions)
   - User status management (active/suspended)

4. **Linking System**
   - Consumer-initiated link requests to suppliers
   - Supplier approval/rejection of link requests
   - Sales representative assignment
   - Link status tracking (pending, accepted, rejected, unlinked)

5. **Product Catalog Management**
   - Product creation, update, and deletion (Supplier only)
   - Product details: name, description, images, stock, pricing
   - Retail and bulk pricing with thresholds
   - Minimum order quantities
   - Product availability management

6. **Order Management**
   - Order creation by consumer staff
   - Order status tracking (created, processing, shipping, completed, rejected)
   - Order status updates by supplier
   - Order history and retrieval

7. **Real-time Communication**
   - WebSocket-based chat for linking conversations
   - Order-specific chat channels
   - Message types: text, system notifications
   - Real-time message broadcasting

8. **Complaint Management**
   - Complaint creation by consumer staff
   - Multi-level escalation: Sales → Manager → Owner
   - Complaint status tracking (open, in_progress, escalated, resolved, closed)
   - Complaint history logging
   - Order cancellation capability

9. **File Management**
   - AWS S3 integration for file uploads
   - Presigned URL generation for secure uploads
   - File deletion support

10. **Internationalization**
    - Multi-language support (English, Russian, Kazakh)
    - City names in multiple languages
    - User locale preferences

### Out of Scope (Future Enhancements)

- Platform Admin dashboard and features
- Analytics and reporting dashboards
- Payment processing integration
- Logistics and shipping management
- Ratings and reviews system
- Subscription management
- Advanced search and filtering
- Email notifications
- SMS notifications
- Mobile push notifications
- Advanced inventory management
- Multi-currency support (currently KZT only)

---

# Glossary

## Core Terms

**SCP** - Supplier Consumer Platform

**B2B** - Business-to-Business

**MVP** - Minimum Viable Product

**RBAC** - Role-Based Access Control

**JWT** - JSON Web Token

**API** - Application Programming Interface

**REST** - Representational State Transfer

**WebSocket** - Full-duplex communication protocol

## User Roles

**Owner** - Company owner with full administrative control, including user management and company deletion

**Manager** - Company manager with catalog management, order handling, and escalation resolution capabilities (cannot manage other managers or delete company)

**Staff** - Regular staff member with limited permissions (consumer staff can place orders; supplier staff can handle communications and first-line complaints)

**Sales Representative** - Supplier staff member assigned to handle consumer relationships and communications

## Company Types

**Supplier** - Company that provides food products to consumers

**Consumer** - Company (restaurant or hotel) that purchases products from suppliers

## System Concepts

**Linking** - A relationship between a consumer company and a supplier company that enables ordering and communication

**Link Request** - A request initiated by a consumer to establish a relationship with a supplier

**Order** - A purchase request created by consumer staff containing one or more products

**Complaint** - An issue raised by consumer staff regarding an order, with escalation capabilities

**Chat** - Real-time messaging channel associated with either a linking or a specific order

**Catalog** - Collection of products offered by a supplier company

**Product** - An item in a supplier's catalog with pricing, stock, and availability information

## Technical Terms

**CRUD** - Create, Read, Update, Delete operations

**ORM** - Object-Relational Mapping

**SQLModel** - Python library combining SQLAlchemy and Pydantic

**FastAPI** - Modern Python web framework for building APIs

**PostgreSQL** - Open-source relational database management system

**Docker** - Containerization platform

**AWS S3** - Amazon Simple Storage Service for file storage

**Presigned URL** - Time-limited URL for secure file uploads

**i18n** - Internationalization (support for multiple languages)

**KZT** - Kazakhstani Tenge (currency)

