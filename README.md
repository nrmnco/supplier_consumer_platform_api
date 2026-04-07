# Supplier-Consumer Platform API

A robust backend API built with FastAPI designed to facilitate interactions between suppliers and consumers. The platform includes features for product management, order processing, real-time chat, and a structured complaint system.

## Features

- Authentication and Authorization: Secure user registration and login using JWT and Argon2 password hashing.
- Role-Based Access Control: Support for company owners, managers, and staff with specific permissions for suppliers and consumers.
- Company Management: Detailed company profiles, including logos and locations.
- Product Management: Comprehensive product catalogs with stock tracking, threshold alerts, and bulk pricing for suppliers.
- Linking System: Formal connection requests and approvals between suppliers and consumers.
- Order Management: Seamless order creation and status tracking between linked companies.
- Real-Time Chat: Integrated messaging system for direct communication between platform participants.
- Complaint System: Structured handling of issues with detailed history tracking and resolution workflows.
- City Pre-population: Automated initialization of major Kazakhstan cities on startup.
- File Storage: Integration with AWS S3 for secure file and image uploads.
- Monitoring: Integrated Sentry SDK for error tracking and performance monitoring.

## Tech Stack

- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLModel (SQLAlchemy wrapper)
- Authentication: JWT (PyJWT)
- Hashing: Argon2
- Cloud Storage: AWS S3 (Boto3)
- Monitoring: Sentry
- Containerization: Docker and Docker Compose

## Project Structure

- src/core: Configuration, database connection, security, and middleware.
- src/models: SQLModel database definitions.
- src/routes: API endpoint implementations grouped by feature.
- src/schemas: Pydantic models for data validation and serialization.
- src/services: Business logic layer.
- src/cruds: Low-level database CRUD operations.
- docs: Documentation and PlantUML diagrams.
- create_mock_data.py: Utility script for generating a realistic development environment.

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (or Docker for running the database)
- AWS Account (for S3 features)

### Installation

1. Clone the repository:
   bash
   git clone <repository_url>
   cd supplier_consumer_platform_api
   

2. Create and activate a virtual environment:
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   

3. Install dependencies:
   bash
   pip install -r requirements.txt
   

4. Set up environment variables:
   bash
   cp env.example .env
   
   Update the `.env` file with your specific configuration.

### Database Setup

1. Start the PostgreSQL database using Docker:
   bash
   docker-compose up -d
   

2. The application will automatically create tables and pre-populate city data on the first startup.

### Generating Mock Data

To populate the platform with sample companies, users, products, and orders, run:
bash
python create_mock_data.py


## Running the Application

Start the FastAPI development server:
bash
fastapi dev src/__init__.py


The API will be available at http://localhost:8000.

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Diagrams

The project includes PlantUML diagrams located in the `docs` directory. To export them, ensure `plantuml.jar` is present and run:
bash
./export-diagrams.sh -png
