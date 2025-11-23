# Abstract and Keywords

## Abstract

The Supplier Consumer Platform (SCP) is a B2B web and mobile application designed to streamline collaboration between food suppliers and institutional consumers (restaurants and hotels). This report documents the implementation of the backend API for the SCP platform, built using FastAPI and PostgreSQL. The system enables direct, pre-approved relationships with controlled access to supplier catalogs, order workflows, real-time chat-based communication, and comprehensive complaint handling with escalation mechanisms.

The platform implements role-based access control (RBAC) with distinct user roles (Owner, Manager, Staff) for both suppliers and consumers. Key features include company onboarding, linking management between suppliers and consumers, product catalog management, order creation and tracking, WebSocket-based real-time messaging, and a multi-level complaint resolution system. The API supports internationalization (i18n) with English, Russian, and Kazakh language support, and integrates with AWS S3 for file storage.

The implementation follows RESTful API principles with JWT-based authentication, comprehensive error handling, and Docker containerization for deployment. This report provides a complete overview of the system architecture, functional and non-functional requirements, API documentation, testing strategies, and operational procedures.

## Keywords

B2B Platform, Supplier-Consumer Collaboration, FastAPI, PostgreSQL, REST API, WebSocket, Role-Based Access Control, Order Management, Complaint Handling, Real-time Chat, Internationalization, Docker, AWS S3, JWT Authentication

---

# Table of Contents

1. [Title Page](#title-page)
2. [Abstract and Keywords; Table of Contents](#abstract-and-keywords-table-of-contents)
3. [Vision & Scope; Glossary](#vision--scope-glossary)
4. [SRS Reading Summary](#srs-reading-summary)
5. [Functional Requirements](#functional-requirements)
6. [Non-functional Requirements](#non-functional-requirements)
7. [Models and Diagrams](#models-and-diagrams)
8. [API Section](#api-section)
9. [User Interface Design](#user-interface-design)
10. [Implementation Methodology](#implementation-methodology)
11. [Testing & Verification](#testing--verification)
12. [CI/CD & Operations](#cicd--operations)
13. [Limitations & Future Work; References; Appendices](#limitations--future-work-references-appendices)

