 Executive Summary

Supplier Consumer Platform (SCP)

# **Purpose**

The Supplier Consumer Platform (SCP) is a B2B web and mobile application designed to streamline collaboration between food suppliers and institutional consumers (restaurants and hotels). It enables direct, pre-approved relationships with controlled access to supplier catalogs, order workflows, chat-based communication, and complaint handling.

# **Scope**

SCP is not a public marketplace. Instead, it provides a controlled environment where:

- Suppliers manage products, catalogs, and relationships.
- Consumers (restaurants/hotels) can view and order only after approval.
- Sales Representatives use the mobile app to interact directly with consumers.
- Managers/Owners handle catalog integrity and escalations.
- Platform Admins (optional, future) may handle compliance, moderation, and analytics.

# **Stakeholders**

- Consumers (restaurants, hotels)
- Suppliers (producers, distributors)
- Supplier Staff: Owners, Managers, Sales Representatives
- Platform Admins (optional, SCP staff)
- Development Team (engineers, designers, QA)
- Business Stakeholders (sponsors, investors, management)

# **Core MVP (Launch Scope)**

Core MVP = Supplier ↔ Consumer workflows only

#### In Scope for MVP:

- Supplier and Consumer onboarding
- Link-based access to supplier catalogs
- Catalog management (products, pricing, stock)
- Order creation, acceptance/rejection, tracking
- Complaint handling (Sales → Manager escalation)
- Chat & notifications (text, file, audio)

- Incident logging & resolution
- Data retention & archival

Excluded from MVP (Future Enhancements): Platform Admin features, analytics dashboards, subscriptions, logistics, payments, ratings/reviews.

# **Technology Stack**

Database: PostgreSQL

Backend: Python (Django/FastAPI), or Java (Spring), or Go

Frontend (Web): React (Next.js), Vue.js, Angular, or Svelte + Tailwind CSS

Mobile: Flutter or React Native

Deployment: Localhost (dev/demo), Staging, Production — with Docker containerization

Design: Figma for UI/UX prototyping

# **Recommended Tools**

- Figma (UI/UX design)

- Docker (containerization)
- GitHub (version control)
- CI/CD (GitHub Actions, CI, Jenkins)
- Postman/Insomnia (API testing)
- Jira/Trello/Asana/GitHub Projects (project management)
- Discord/Google Meet/Telegram (communication)