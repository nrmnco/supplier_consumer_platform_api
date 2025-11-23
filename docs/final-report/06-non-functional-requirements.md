# Non-functional Requirements

## Quality Attributes with Measurable Acceptance Criteria

### NFR-001: Security

**Description:** The system must implement robust security measures to protect user data, authentication credentials, and API endpoints.

**Quality Attributes:**
- Authentication: JWT-based token system
- Authorization: Role-based access control (RBAC)
- Data Protection: Password hashing using argon2
- API Security: Token validation on protected endpoints

**Acceptance Criteria:**
1. All passwords are hashed using argon2-cffi before storage
2. JWT tokens expire after 15 minutes (access) or 7 days (refresh)
3. All protected endpoints require valid JWT token in Authorization header
4. Role-based permissions are enforced at the API level
5. Invalid or expired tokens return 401 Unauthorized
6. Password verification uses secure comparison (timing-safe)

**Measurement:**
- ✅ Password hashing implemented with `pwdlib.PasswordHash`
- ✅ JWT token creation and validation implemented
- ✅ RBAC checks in all route handlers
- ✅ HTTPBearer security dependency on protected routes

**Status:** ✅ Implemented

---

### NFR-002: Performance

**Description:** The system must respond to API requests within acceptable time limits and handle concurrent users efficiently.

**Quality Attributes:**
- Response Time: API endpoints should respond within 2 seconds for standard operations
- Throughput: System should handle at least 100 concurrent requests
- Database Performance: Efficient queries with proper indexing

**Acceptance Criteria:**
1. Authentication endpoints respond within 500ms
2. CRUD operations respond within 1 second
3. Complex queries (order history, chat messages) respond within 2 seconds
4. WebSocket connections maintain low latency (< 100ms for message delivery)
5. Database queries use indexes on frequently accessed fields (email, phone_number, company_id)

**Measurement:**
- ⚠️ Performance testing not yet conducted
- ✅ Database indexes on email, phone_number, company_id
- ✅ Connection pooling via SQLModel engine
- ⚠️ Load testing TODO

**Status:** ⚠️ Partially Implemented (optimization ongoing)

---

### NFR-003: Scalability

**Description:** The system architecture must support horizontal scaling and handle growth in users and data volume.

**Quality Attributes:**
- Stateless Design: API is stateless, allowing multiple server instances
- Database Scalability: PostgreSQL supports connection pooling
- Containerization: Docker enables easy deployment and scaling

**Acceptance Criteria:**
1. API server is stateless (no session storage)
2. Database connection pooling is configured
3. Docker Compose configuration exists for local deployment
4. Environment variables support different deployment configurations
5. File storage uses external service (AWS S3) for scalability

**Measurement:**
- ✅ Stateless API design (JWT tokens, no server-side sessions)
- ✅ Docker Compose for database
- ✅ AWS S3 for file storage (external, scalable)
- ✅ Environment-based configuration

**Status:** ✅ Implemented

---

### NFR-004: Reliability

**Description:** The system must be available and handle errors gracefully without data loss.

**Quality Attributes:**
- Error Handling: Comprehensive exception handling
- Data Integrity: Database constraints and transactions
- Availability: System should be available 99% of the time (target)

**Acceptance Criteria:**
1. All database operations use transactions where appropriate
2. Foreign key constraints prevent orphaned records
3. HTTP exceptions return appropriate status codes (400, 401, 403, 404, 500)
4. Database connection errors are handled gracefully
5. Invalid input validation returns 400 Bad Request with clear messages
6. Critical operations (order creation, complaint creation) are transactional

**Measurement:**
- ✅ SQLModel relationships with foreign keys
- ✅ HTTPException with appropriate status codes
- ✅ Input validation via Pydantic schemas
- ⚠️ Transaction management could be improved
- ⚠️ Error logging TODO

**Status:** ⚠️ Partially Implemented

---

### NFR-005: Maintainability

**Description:** The codebase must be well-organized, documented, and follow consistent coding standards.

**Quality Attributes:**
- Code Organization: Modular structure (routes, cruds, models, schemas)
- Documentation: Code comments and docstrings
- Consistency: Consistent naming conventions and patterns

**Acceptance Criteria:**
1. Code is organized into logical modules (routes, cruds, models, schemas)
2. Functions have clear, descriptive names
3. Complex logic is commented
4. Database models are clearly defined with relationships
5. API endpoints have clear documentation
6. Configuration is externalized (environment variables)

**Measurement:**
- ✅ Modular structure: routes/, cruds/, models/, schemas/, core/
- ✅ Clear separation of concerns
- ✅ SQLModel for type-safe database models
- ⚠️ Code comments could be more comprehensive
- ⚠️ API documentation (OpenAPI/Swagger) TODO

**Status:** ⚠️ Partially Implemented

---

### NFR-006: Internationalization (i18n)

**Description:** The system must support multiple languages for the Kazakhstan market.

**Quality Attributes:**
- Language Support: English, Russian, Kazakh
- Locale Management: User locale preferences
- Data Localization: City names in multiple languages

**Acceptance Criteria:**
1. User model includes locale field (en, ru, kz)
2. Cities table stores names in English, Russian, and Kazakh
3. API responses can be localized based on user locale
4. Default locale is English
5. Currency formatting supports KZT (Kazakhstani Tenge)

**Measurement:**
- ✅ User locale field (Locale enum: en, ru, kz)
- ✅ Cities table with city_name, city_name_ru, city_name_kz
- ✅ City data seeded with multi-language names
- ⚠️ API response localization not fully implemented
- ⚠️ Currency formatting (KZT) TODO in frontend

**Status:** ⚠️ Partially Implemented

---

### NFR-007: Usability

**Description:** The API should be intuitive, well-documented, and provide clear error messages.

**Quality Attributes:**
- API Design: RESTful principles
- Error Messages: Clear, actionable error messages
- Documentation: OpenAPI/Swagger documentation

**Acceptance Criteria:**
1. API follows RESTful conventions (GET, POST, PUT, PATCH, DELETE)
2. Endpoint URLs are intuitive and consistent
3. Error messages are descriptive and actionable
4. Request/response formats are consistent
5. OpenAPI documentation is available at /docs endpoint

**Measurement:**
- ✅ RESTful API design
- ✅ Consistent endpoint naming
- ✅ Descriptive error messages
- ⚠️ FastAPI auto-generates OpenAPI docs (available at /docs)
- ⚠️ Manual API documentation TODO

**Status:** ⚠️ Partially Implemented

---

### NFR-008: Compatibility

**Description:** The system must be compatible with standard web and mobile clients.

**Quality Attributes:**
- API Standards: REST API with JSON
- CORS: Cross-origin resource sharing support
- WebSocket: Standard WebSocket protocol

**Acceptance Criteria:**
1. API accepts and returns JSON format
2. CORS is configured to allow frontend origins
3. WebSocket connections use standard protocol
4. Content-Type headers are properly set
5. API versioning strategy (if needed)

**Measurement:**
- ✅ JSON request/response format
- ✅ CORS middleware configured (allows localhost:3000, localhost:8000, and regex patterns)
- ✅ WebSocket implementation using FastAPI WebSocket
- ✅ Proper Content-Type headers

**Status:** ✅ Implemented

---

### NFR-009: Data Integrity

**Description:** The system must ensure data consistency and prevent data corruption.

**Quality Attributes:**
- Database Constraints: Foreign keys, unique constraints, not null constraints
- Validation: Input validation at API and database levels
- Referential Integrity: Cascade rules for related data

**Acceptance Criteria:**
1. All foreign key relationships are enforced
2. Unique constraints on email and phone_number
3. Required fields are marked as nullable=False
4. Enum types are validated (UserRole, CompanyType, OrderStatus, etc.)
5. Data validation occurs at schema level (Pydantic) and database level

**Measurement:**
- ✅ Foreign key constraints in all models
- ✅ Unique indexes on email and phone_number
- ✅ Required fields properly marked
- ✅ Enum types for status fields
- ✅ Pydantic schema validation

**Status:** ✅ Implemented

---

### NFR-010: Extensibility

**Description:** The system architecture must allow for future enhancements and feature additions.

**Quality Attributes:**
- Modular Design: Loose coupling between components
- Plugin Architecture: Easy to add new features
- Configuration: Externalized configuration

**Acceptance Criteria:**
1. New routes can be added without modifying existing code
2. New models can be added following existing patterns
3. Configuration is externalized (environment variables)
4. Service layer (S3 service) can be easily replaced
5. Database schema changes can be managed via migrations

**Measurement:**
- ✅ Modular route structure (easy to add new routes)
- ✅ Consistent model patterns
- ✅ Environment-based configuration
- ✅ Service abstraction (S3 service)
- ⚠️ Database migrations TODO (currently using SQLModel metadata.create_all)

**Status:** ⚠️ Partially Implemented

---

## Summary Table

| NFR ID | Quality Attribute | Priority | Status | Notes |
|--------|------------------|----------|--------|-------|
| NFR-001 | Security | High | ✅ | Fully implemented |
| NFR-002 | Performance | High | ⚠️ | Optimization ongoing |
| NFR-003 | Scalability | High | ✅ | Fully implemented |
| NFR-004 | Reliability | High | ⚠️ | Error handling needs improvement |
| NFR-005 | Maintainability | Medium | ⚠️ | Documentation needs enhancement |
| NFR-006 | Internationalization | Medium | ⚠️ | Partial implementation |
| NFR-007 | Usability | Medium | ⚠️ | API docs need manual enhancement |
| NFR-008 | Compatibility | High | ✅ | Fully implemented |
| NFR-009 | Data Integrity | High | ✅ | Fully implemented |
| NFR-010 | Extensibility | Medium | ⚠️ | Migrations needed |

**Legend:**
- ✅ Fully Implemented
- ⚠️ Partially Implemented
- ❌ Not Implemented

