# Software Requirements Specification (SRS)

## **Supplier Consumer Platform (SCP)**

Version: 2.0

Date: September 17, 2025 Author: Marat Isteleyev

**B2B platform - Core MVP**

**Supplier ↔ Consumer workflows only**

## <span id="page-1-0"></span>**Table of Contents**

| Table of Contents                            | 2  |
|----------------------------------------------|----|
| 1. Introduction                              | 3  |
| 1.1 Purpose                                  | 3  |
| 1.2 Scope                                    | 3  |
| 1.3 Definitions, Acronyms, and Abbreviations | 3  |
| 2. Overall Description                       | 4  |
| 2.1 Product Perspective                      | 4  |
| 2.2 Product Functions (High-Level)           | 4  |
| 2.3 User Classes and Characteristics         | 4  |
| 2.4 Operating Environment                    | 4  |
| 2.5 Constraints                              | 5  |
| 2.6 Documentation                            | 5  |
| 2.7 Assumptions and Dependencies             | 5  |
| 3. System Features and Requirements          | 5  |
| 3.1 Consumer Functionality                   | 5  |
| 3.2 Supplier Functionality                   | 5  |
| 3.2.1 Roles & Permissions                    | 5  |
| 3.2.2 Catalog & Storefront                   | 6  |
| 3.2.3 Order Management                       | 6  |
| 3.2.4 Communication                          | 6  |
| 3.3 Platform Admin Functionality (OPTIONAL)  | 6  |
| 4. Technology Stack                          |    |
| 5. Example Use Cases                         |    |
| ' 6. Role-Based Responsibility Matrix        |    |
| 7. Incident Management                       |    |
| 8. Data Retention                            |    |
| 9. MVP Scope & Launch                        |    |
| 10. Pacammandad Tools                        | 10 |

## <span id="page-2-0"></span>**1. Introduction**

## <span id="page-2-1"></span>**1.1 Purpose**

The purpose of this document is to outline the detailed software requirements for the Supplier Consumer Platform (SCP), a B2B mobile and web-based application that facilitates direct collaboration between suppliers and institutional consumers (restaurants/hotels). This document provides a clear set of requirements to guide development and implementation, ensuring the platform meets the needs of suppliers, consumers, and platform administrators (optional).

## <span id="page-2-2"></span>**1.2 Scope**

The Supplier Consumer Platform (SCP) is a B2B digital platform designed to enable structured collaboration between food suppliers and institutional consumers such as restaurants and hotels. The platform is not a public marketplace; instead, it supports direct, pre-approved relationships between suppliers and their linked consumers.

Suppliers can create and manage catalogs, assign managers and sales representatives, and handle consumer relationships. Consumers may only view and order goods after a link request is approved by a supplier. Managers oversee catalog integrity and escalations inside supplier companies. Platform Admins (optional, SCP staff) may manage verification, moderation, and analytics in future phases.

The main stakeholders of the Supplier Consumer Platform (SCP) are:

- Consumers (restaurants, hotels) who use the system to order food products.
- Suppliers (producers, distributors) who list products and manage relationships.
- Supplier Staff (Owners, Managers, Sales Representatives) who operate the supplier accounts.
- Platform Admins (OPTIONAL, SCP staff) who may oversee compliance, catalog moderation, and analytics in future phases.
- Development Team (engineers, designers, QA testers) responsible for building and maintaining the platform.
- Business Stakeholders (project sponsors, investors, management) ensuring alignment with strategic goals.

## <span id="page-2-3"></span>**1.3 Definitions, Acronyms, and Abbreviations**

SCP – Supplier Consumer Platform

B2B – Business-to-Business

Supplier – Company providing food products

Consumer – Restaurant or hotel purchasing goods

Owner (Supplier-side) – Has full account control, including creating/removing managers and deleting the supplier account.

Manager (Supplier-side) – Handles catalog, inventory, orders, and escalations but cannot remove the

supplier account or manage Owners/Managers.

Sales Representative – Handles direct communication with consumers and escalates issues when necessary.

Platform Admin (OPTIONAL) – SCP staff for compliance, moderation, and analytics (not part of MVP).

## <span id="page-3-0"></span>**2. Overall Description**

## <span id="page-3-1"></span>**2.1 Product Perspective**

The platform consists of:

- Mobile application (for consumers and supplier Sales Representatives)
- Web application (for suppliers and optional platform admins)
- Backend services (REST API with Django/FastAPI/Spring/Go, PostgreSQL database)

## <span id="page-3-2"></span>**2.2 Product Functions (High-Level)**

- Supplier onboarding (KYB)
- Controlled catalog management (products, availability, minimum order quantities)
- Link-based access (consumers must be approved/linked)
- Order creation, acceptance/rejection, tracking
- Complaint and return handling
- Messaging and notifications
- Incident logging and escalation
- Ratings & reviews (OPTIONAL)
- Platform Admin dashboard for verification, moderation, analytics (OPTIONAL)
- Analytics dashboards (OPTIONAL)

## <span id="page-3-3"></span>**2.3 User Classes and Characteristics**

- Consumers: Restaurants and hotels
- Suppliers: Owners, Managers, Sales Representatives
- Platform Admins (OPTIONAL): SCP staff responsible for compliance and platform-wide oversight

## <span id="page-3-4"></span>**2.4 Operating Environment**

Mobile: Flutter or React Native, iOS/Android

Web: React (Next.js), VueJS, Angular, Tailwind, or Svelte

Backend: Cloud-deployed (Docker containers)

Backend and the entire platform can also be hosted on **localhost** for development, testing, and demo

#### purposes.

Design: Usage of Figma for UI/UX design is highly advised.

Containerization: Usage of Docker for service deployment is also advised.

## <span id="page-4-0"></span>**2.5 Constraints**

Mobile app must use Flutter/React Native

Initial rollout: Kazakhstan market Languages: Kazakh, Russian, English

Accessibility: WCAG 2.1 AA Performance SLAs: TBD

## <span id="page-4-1"></span>**2.6 Documentation**

In-app guides, FAQs, and supplier onboarding checklists

## <span id="page-4-2"></span>**2.7 Assumptions and Dependencies**

Flutter stack supported for iOS/Android distribution (React Native too) Third-party map provider (Google/Apple Maps)

## <span id="page-4-3"></span>**3. System Features and Requirements**

## <span id="page-4-4"></span>**3.1 Consumer Functionality**

- Link requests required before accessing supplier catalogs
- Manage links: pending, accepted, removed, blocked
- View catalog and place orders once approved
- Track orders and reorder (optional)
- Log complaints tied to order details

## <span id="page-4-5"></span>**3.2 Supplier Functionality**

#### <span id="page-4-6"></span>**3.2.1 Roles & Permissions**

#### Owner:

- Full control over supplier account
- Can create/remove Managers and Sales
- Can delete/deactivate supplier account

#### Manager:

- Same as Owner except cannot create/remove Managers or delete account
- Handles catalog, inventory, and escalations

#### Sales Representative:

- Handles consumer communication
- Manages first-line complaints
- Escalates issues to Manager/Owner

#### <span id="page-5-0"></span>**3.2.2 Catalog & Storefront**

- Create/edit products with units, pricing, discounts, stock levels
- Configure delivery/pickup options, lead times

#### <span id="page-5-1"></span>**3.2.3 Order Management**

- Receive, accept, reject bulk orders
- Update stock in real time
- Complaints: Sales (first-line) → Manager (escalation) → Owner (oversight)

#### <span id="page-5-2"></span>**3.2.4 Communication**

- Integrated chat post link approval
- Features: receipts, attachments, product links, canned replies
- Escalation: Sales → Manager
- Controls: Approve/deny links, block/unlink consumers

## <span id="page-5-3"></span>**3.3 Platform Admin Functionality (OPTIONAL)**

- Manage supplier onboarding and verification
- Moderate product categories
- Monitor disputes
- Access platform-wide analytics dashboards

## <span id="page-6-0"></span>**4. Technology Stack**

The following technology stack is recommended for implementation of the SCP system:

#### Database (DB):

- PostgreSQL

#### Backend:

- Python (Django or FastAPI), or
- Java (Spring), or
- Go

#### Frontend (Web):

- React (or Next.js), or
- Vue.js, or
- Angular, or
- Svelte
- Tailwind CSS (for styling)

### Mobile:

- Flutter, or
- React Native

Backend and the entire platform can also be hosted on **localhost** for development, testing, and demo purposes.

## <span id="page-6-1"></span>**5. Example Use Cases**

UC1: Consumer places an order

- Actor: Consumer (via mobile app)
- Precondition: Consumer is linked to supplier.
- Steps: Browse catalog, add items, submit order, supplier receives notification.
- Postcondition: Order appears in supplier dashboard (web for Managers/Owners, mobile for Sales).

UC2: Sales Representative handles a consumer complaint

- Actor: Sales Representative (via mobile app)
- Steps: Receives complaint in chat tied to an order, attempts resolution, escalates to Manager if unresolved.
- Postcondition: Complaint either resolved or escalated.

UC3: Manager updates catalog

- Actor: Manager (via web app)
- Steps: Logs in, edits product details, saves changes.
- Postcondition: Updated catalog visible to linked consumers.

UC4: Manager resolves escalated complaint

- Actor: Manager (via web app)
- Steps: Reviews escalated complaint, applies resolution, marks resolved.
- Postcondition: Consumer notified; record stored.

UC5: Owner creates a Manager account

- Actor: Owner (via web app)
- Steps: Navigates to user management, creates Manager, assigns permissions.
- Postcondition: New Manager account is active.

UC6: Owner deletes supplier account

- Actor: Owner (via web app)
- Steps: Navigates to settings, selects delete, confirms action.
- Postcondition: Supplier account deactivated, data archived.

UC7 (OPTIONAL): Platform Admin verifies a supplier

- Actor: Platform Admin (via web app, OPTIONAL)
- Steps: Reviews documents, approves/rejects, updates status.
- Postcondition: Supplier status updated.

Task | Owner | Manager | Sales | Consumer | Platform Admin (OPT)

--------------------------------------------------------------------------------

Account creation/deletion (Supplier) | A | | | I | I

Create/remove Manager accounts | A | | | I | I

Catalog & inventory management | R/A | R/A | | I | C

Process consumer inquiries | I | C | R/A | C | I

Order placement | I | I | I | R/A | I

Order acceptance/rejection | C | R/A | C | I | I

Complaint handling (first-line) | I | C | R/A | C | I

Complaint escalation | C | R/A | C | C | I

Supplier KYB verification | I | I | I | I | R/A

Catalog/category moderation | I | I | I | I | R/A

Analytics dashboards | I | I | I | I | R/A

The following RACI-style matrix clarifies responsibilities of each role in the system.

R = Responsible, A = Accountable, C = Consulted, I = Informed

## <span id="page-8-0"></span>**6. Role-Based Responsibility Matrix**

## <span id="page-8-1"></span>**7. Incident Management**

- Consumers log incidents via orders
- Sales attempt resolution
- Escalation to Manager if unresolved
- Platform Admins may oversee systemic issues (OPTIONAL)
- Status tracked (open, in progress, resolved)
- Exportable logs

## <span id="page-8-2"></span>**8. Data Retention**

- All records retained for compliance
- Read-only archival after X years (TBD)

Figure: Core MVP vs Optional Features

## <span id="page-9-0"></span>**9. MVP Scope & Launch**

Core MVP = Supplier ↔ Consumer B2B workflows only.

The MVP must include:

- Consumer–Supplier linking system
- Catalog visible only to linked consumers
- Order creation, acceptance/rejection, tracking
- Chat with file/audio support
- Complaint handling (Sales → Manager)
- Incident logging & escalation
- Data retention & archival policy

Optional (excluded from MVP):

- Platform Admin functionality
- Analytics dashboards
- Subscription models
- Payments
- Logistics coordination
- Ratings & reviews

Target launch date: November 20, 2025 (adjustable).

## <span id="page-9-1"></span>**10. Recommended Tools**

The following tools are recommended for the successful implementation, design, and deployment of SCP:

- Figma: For collaborative UI/UX design and prototyping
- Docker: For containerization and consistent deployment across environments
- Git/GitHub: For version control and collaboration
- CI/CD pipelines (GitHub Actions, CI, Jenkins, etc.): For automated builds, tests, and deployments
- Postman/Insomnia: For API testing
- Jira/Trello/Asana/GitHub Projects: For project management and task tracking
- Discord/Google Meet/Microsoft Teams: For team communication