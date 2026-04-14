# Insurance Claims Backend Service - Design Document

## Overview

This document outlines the design and architecture for a high-performance insurance claims backend service built with FastAPI, PostgreSQL, SQLAlchemy ORM, and Alembic for migrations.

**Project Location:** `insurance_claims_service/`

## Monorepo Structure

This project uses a **monorepo architecture** to house multiple services and shared resources:

```
/Users/ankitkumar/Coding/insurance_claims/     # Root directory
├── .gitignore                                 # Root-level ignore patterns
├── .vscode/                                   # Shared IDE configuration
├── insurance_claims_service/                  # Backend API (Python/FastAPI)
│   ├── .gitignore                            # Python-specific patterns
│   ├── app/                                  # Application code
│   ├── tests/                                # Test suite
│   ├── alembic/                              # Database migrations
│   ├── scripts/                              # Utility scripts
│   ├── requirements.txt                      # Python dependencies
│   ├── docker-compose.yml                    # Local development services
│   ├── Dockerfile                            # Container configuration
│   └── README.md                             # Service documentation
├── insurance_claims_web/                      # Frontend (React/Next.js - future)
│   └── .gitignore                            # Node.js-specific patterns (future)
└── knowledge/                                 # Project documentation
    ├── design/                               # Design documents
    │   ├── entities_details.md
    │   └── backend_service_design.md
    └── tasks/                                # Task tracking
        └── tasks.md
```

### Multi-Level .gitignore Strategy

The project uses a **layered .gitignore approach** for optimal organization in a monorepo:

#### 1. Root-Level `.gitignore`
**Location:** `/`  
**Purpose:** Project-wide patterns that apply across all services

**Contains:**
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Generic patterns (`*.log`, `.env.local`)
- Build artifacts (`dist/`, `build/`)

#### 2. Service-Level `.gitignore`
**Location:** `/insurance_claims_service/.gitignore`  
**Purpose:** Backend service-specific patterns

**Contains:**
- Python virtual environments (`venv/`, `.venv/`)
- Python cache files (`__pycache__/`, `*.pyc`, `*.pyo`)
- Python testing (`.pytest_cache/`, `.coverage`)
- Alembic versions (generated migration files)
- Python-specific environment files

#### 3. Future Service `.gitignore`
**Location:** `/insurance_claims_web/.gitignore` (planned)  
**Purpose:** Frontend service-specific patterns

**Will contain:**
- Node.js dependencies (`node_modules/`)
- Next.js build files (`.next/`, `out/`)
- npm/yarn cache files
- Frontend build artifacts

### Benefits of This Structure

✅ **Separation of Concerns**: Each service maintains its own ignore patterns  
✅ **Technology Independence**: Different tech stacks don't interfere with each other  
✅ **Shared Patterns**: Common patterns (IDE, OS) defined once at root level  
✅ **Maintainability**: Easy to understand what's ignored and why  
✅ **Scalability**: New services can be added with their own .gitignore files

### Git Behavior with Multiple .gitignore Files

Git respects `.gitignore` files at **any level** in the directory tree:
- Root `.gitignore` applies to **entire repository**
- Service-level `.gitignore` applies to **that directory and subdirectories**
- Patterns are **additive** (all levels are checked)
- More specific patterns **override** general ones

## Technology Stack

### Core Framework
- **FastAPI** (Python 3.11+): Modern, high-performance web framework
  - Built-in OpenAPI (Swagger) documentation
  - Automatic request validation with Pydantic
  - Async/await support for high concurrency
  - Dependency injection system

### Database
- **PostgreSQL 15+**: Primary data store
  - JSONB support for flexible data
  - Full-text search capabilities
  - Advanced indexing (B-tree, GIN, GiST)
  - Row-level security (RLS)

### ORM & Migrations
- **SQLAlchemy 2.0+**: High-performance ORM
  - Async support with asyncpg
  - Connection pooling
  - Query optimization
  - Relationship management
- **Alembic**: Database migration tool
  - Version control for schema changes
  - Auto-generation of migrations
  - Rollback capabilities

### Additional Libraries
- **asyncpg**: Fast PostgreSQL driver for async operations
- **Pydantic v2**: Data validation and serialization
- **python-jose**: JWT token handling
- **passlib + bcrypt**: Password hashing
- **python-multipart**: File upload support
- **redis**: Caching and session management
- **celery**: Background task processing
- **pytest + pytest-asyncio**: Testing framework
- **httpx**: Async HTTP client for testing
- **uvicorn**: Lightning-fast ASGI server
- **python-dotenv**: Environment variable management
- **aiofiles**: Async file operations
- **slowapi**: Rate limiting for FastAPI
- **pillow**: Image processing for documents
- **boto3**: AWS SDK (S3 storage, SES email)
- **sendgrid** or **mailgun**: Email service integration
- **twilio**: SMS notifications (optional)
- **python-magic**: MIME type detection
- **pypdf2** or **pdfplumber**: PDF processing
- **openpyxl**: Excel file handling
- **faker**: Test data generation
- **factory-boy**: Test fixtures
- **locust**: Load testing
- **sentry-sdk**: Error tracking integration
- **prometheus-client**: Metrics collection
- **python-jose[cryptography]**: Enhanced JWT support
- **aioboto3**: Async AWS SDK
- **aioredis**: Async Redis client

## Project Structure

```
insurance_claims_service/
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration version files
│   └── env.py                    # Alembic configuration
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Configuration management
│   ├── database.py               # Database connection and session
│   ├── dependencies.py           # Common dependencies
│   │
│   ├── enums/                    # Enum definitions
│   │   ├── __init__.py
│   │   ├── policy_enums.py      # Policy types, statuses
│   │   ├── claim_enums.py       # Claim types, statuses
│   │   ├── payment_enums.py     # Payment methods, statuses
│   │   ├── user_enums.py        # User roles, permissions
│   │   └── common_enums.py      # Shared enums
│   │
│   ├── constants/                # Application constants
│   │   ├── __init__.py
│   │   ├── business_rules.py    # Business rule constants
│   │   ├── messages.py          # Error/success messages
│   │   └── limits.py            # Rate limits, file sizes
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py              # Base model with common fields
│   │   ├── policy.py
│   │   ├── claim.py
│   │   ├── customer.py
│   │   ├── agent.py
│   │   ├── insurer.py
│   │   ├── premium.py
│   │   ├── coverage.py
│   │   ├── beneficiary.py
│   │   ├── underwriter.py
│   │   ├── risk_assessment.py
│   │   ├── payment.py
│   │   ├── document.py
│   │   ├── incident.py
│   │   ├── vehicle.py
│   │   ├── property.py
│   │   ├── medical_record.py
│   │   ├── quote.py
│   │   ├── policy_renewal.py
│   │   ├── commission.py
│   │   ├── endorsement.py
│   │   ├── address.py
│   │   ├── payment_method.py
│   │   └── user.py              # Authentication user model
│   │
│   ├── schemas/                  # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── policy.py            # PolicyCreate, PolicyUpdate, PolicyResponse
│   │   ├── claim.py
│   │   ├── customer.py
│   │   ├── agent.py
│   │   ├── insurer.py
│   │   ├── premium.py
│   │   ├── coverage.py
│   │   ├── beneficiary.py
│   │   ├── underwriter.py
│   │   ├── risk_assessment.py
│   │   ├── payment.py
│   │   ├── document.py
│   │   ├── incident.py
│   │   ├── vehicle.py
│   │   ├── property.py
│   │   ├── medical_record.py
│   │   ├── quote.py
│   │   ├── policy_renewal.py
│   │   ├── commission.py
│   │   ├── endorsement.py
│   │   ├── address.py
│   │   ├── payment_method.py
│   │   ├── auth.py              # Login, Token schemas
│   │   └── common.py            # Pagination, filters
│   │
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py              # API dependencies
│   │   └── v1/                  # API version 1
│   │       ├── __init__.py
│   │       ├── router.py        # Main router aggregator
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── policies.py
│   │       ├── claims.py
│   │       ├── customers.py
│   │       ├── agents.py
│   │       ├── insurers.py
│   │       ├── premiums.py
│   │       ├── coverages.py
│   │       ├── beneficiaries.py
│   │       ├── underwriters.py
│   │       ├── risk_assessments.py
│   │       ├── payments.py
│   │       ├── documents.py
│   │       ├── incidents.py
│   │       ├── vehicles.py
│   │       ├── properties.py
│   │       ├── medical_records.py
│   │       ├── quotes.py
│   │       ├── policy_renewals.py
│   │       ├── commissions.py
│   │       ├── endorsements.py
│   │       ├── dashboard.py     # Analytics and statistics
│   │       └── reports.py       # Reporting endpoints
│   │
│   ├── crud/                     # CRUD operations
│   │   ├── __init__.py
│   │   ├── base.py              # Base CRUD class
│   │   ├── policy.py
│   │   ├── claim.py
│   │   ├── customer.py
│   │   ├── agent.py
│   │   ├── insurer.py
│   │   ├── premium.py
│   │   ├── coverage.py
│   │   ├── beneficiary.py
│   │   ├── underwriter.py
│   │   ├── risk_assessment.py
│   │   ├── payment.py
│   │   ├── document.py
│   │   ├── incident.py
│   │   ├── vehicle.py
│   │   ├── property.py
│   │   ├── medical_record.py
│   │   ├── quote.py
│   │   ├── policy_renewal.py
│   │   ├── commission.py
│   │   └── endorsement.py
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── policy_service.py    # Complex policy operations
│   │   ├── claim_service.py     # Claim processing logic
│   │   ├── underwriting_service.py
│   │   ├── payment_service.py   # Payment processing
│   │   ├── commission_service.py
│   │   ├── notification_service.py
│   │   ├── document_service.py  # File handling
│   │   ├── analytics_service.py
│   │   └── export_service.py    # Data export
│   │
│   ├── core/                     # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py          # JWT, password hashing
│   │   ├── config.py            # Settings management
│   │   ├── cache.py             # Redis caching
│   │   ├── exceptions.py        # Custom exceptions
│   │   ├── logging.py           # Logging configuration
│   │   └── middleware.py        # Custom middleware
│   │
│   ├── utils/                    # Helper utilities
│   │   ├── __init__.py
│   │   ├── validators.py        # Custom validators
│   │   ├── formatters.py        # Data formatters
│   │   ├── calculators.py       # Premium, commission calculations
│   │   ├── file_handler.py      # File upload/download
│   │   └── email.py             # Email utilities
│   │
│   └── tasks/                    # Background tasks (Celery)
│       ├── __init__.py
│       ├── celery_app.py
│       ├── policy_tasks.py      # Policy renewal reminders
│       ├── payment_tasks.py     # Payment processing
│       ├── notification_tasks.py
│       └── report_tasks.py      # Generate reports
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_api/                # API endpoint tests
│   ├── test_crud/               # CRUD operation tests
│   ├── test_services/           # Service layer tests
│   └── test_utils/              # Utility function tests
│
├── scripts/                      # Utility scripts
│   ├── init_db.py               # Initialize database
│   ├── seed_data.py             # Seed sample data
│   └── backup_db.py             # Database backup
│
├── .env.example                  # Environment variables template
├── .gitignore
├── alembic.ini                   # Alembic configuration
├── docker-compose.yml            # Docker setup
├── Dockerfile
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## Architecture Patterns

### 1. Layered Architecture

```
┌─────────────────────────────────────┐
│     API Layer (FastAPI Routes)      │  ← HTTP requests, validation
├─────────────────────────────────────┤
│     Service Layer (Business Logic)  │  ← Complex operations, orchestration
├─────────────────────────────────────┤
│     CRUD Layer (Data Access)        │  ← Database operations
├─────────────────────────────────────┤
│     Models Layer (SQLAlchemy ORM)   │  ← Data structure, relationships
├─────────────────────────────────────┤
│     Database (PostgreSQL)           │  ← Data persistence
└─────────────────────────────────────┘
```

### 2. Repository Pattern
- Generic CRUD base class for common operations
- Specialized methods in entity-specific CRUD classes
- Separation of data access from business logic

### 3. Dependency Injection
- FastAPI's dependency injection for database sessions
- Authentication dependencies
- Pagination and filtering dependencies

### 4. Schema Validation
- Request validation with Pydantic schemas
- Response serialization
- Type safety and auto-documentation

## Database Design

### Connection Management

```python
# Async connection pool for high performance
# Connection pooling: min=10, max=100 connections
# Statement timeout: 30 seconds
# Connection timeout: 10 seconds
```

### Indexes Strategy

**High Priority Indexes:**
- Primary keys (automatic)
- Foreign keys for all relationships
- Policy: `policy_number`, `policy_holder_id`, `status`
- Claim: `claim_number`, `policy_id`, `status`, `claim_date`
- Customer: `email`, `phone_number`, `identification_number`
- Premium: `policy_id`, `due_date`, `payment_status`
- Payment: `transaction_reference`, `payment_date`

**Composite Indexes:**
- `(policy_id, status)` for active policy queries
- `(customer_id, status)` for customer-specific queries
- `(claim_date, status)` for date range + status queries

**Full-Text Search:**
- GIN index on customer names
- GIN index on policy/claim descriptions

### Partitioning Strategy

For high-volume tables:
- **Claims**: Range partition by `claim_date` (yearly)
- **Payments**: Range partition by `payment_date` (monthly)
- **Documents**: Range partition by `upload_date` (monthly)

### Data Retention

- **Soft deletes**: Use `deleted_at` timestamp
- **Audit logs**: Separate audit table for critical changes
- **Archive strategy**: Move old data to archive tables after 7 years

## API Design

### RESTful Endpoints Structure

Each entity follows this pattern:

```
GET     /api/v1/{entity}              - List all (with pagination, filtering)
POST    /api/v1/{entity}              - Create new
GET     /api/v1/{entity}/{id}         - Get by ID
PUT     /api/v1/{entity}/{id}         - Full update
PATCH   /api/v1/{entity}/{id}         - Partial update
DELETE  /api/v1/{entity}/{id}         - Delete (soft delete)
```

### Entity-Specific Endpoints

#### Policy Endpoints
```
GET     /api/v1/policies
POST    /api/v1/policies
GET     /api/v1/policies/{policy_id}
PUT     /api/v1/policies/{policy_id}
PATCH   /api/v1/policies/{policy_id}
DELETE  /api/v1/policies/{policy_id}

# Additional operations
GET     /api/v1/policies/{policy_id}/claims
GET     /api/v1/policies/{policy_id}/premiums
GET     /api/v1/policies/{policy_id}/coverages
GET     /api/v1/policies/{policy_id}/beneficiaries
GET     /api/v1/policies/{policy_id}/documents
POST    /api/v1/policies/{policy_id}/renew
POST    /api/v1/policies/{policy_id}/cancel
POST    /api/v1/policies/{policy_id}/endorse
GET     /api/v1/policies/{policy_id}/history
GET     /api/v1/policies/expiring           # Expiring soon
GET     /api/v1/policies/by-customer/{customer_id}
```

#### Claim Endpoints
```
GET     /api/v1/claims
POST    /api/v1/claims
GET     /api/v1/claims/{claim_id}
PUT     /api/v1/claims/{claim_id}
PATCH   /api/v1/claims/{claim_id}
DELETE  /api/v1/claims/{claim_id}

# Additional operations
POST    /api/v1/claims/{claim_id}/approve
POST    /api/v1/claims/{claim_id}/reject
POST    /api/v1/claims/{claim_id}/settle
GET     /api/v1/claims/{claim_id}/documents
POST    /api/v1/claims/{claim_id}/documents
GET     /api/v1/claims/{claim_id}/history
GET     /api/v1/claims/{claim_id}/timeline
GET     /api/v1/claims/pending
GET     /api/v1/claims/by-policy/{policy_id}
GET     /api/v1/claims/by-status/{status}
```

#### Customer Endpoints
```
GET     /api/v1/customers
POST    /api/v1/customers
GET     /api/v1/customers/{customer_id}
PUT     /api/v1/customers/{customer_id}
PATCH   /api/v1/customers/{customer_id}
DELETE  /api/v1/customers/{customer_id}

# Additional operations
GET     /api/v1/customers/{customer_id}/policies
GET     /api/v1/customers/{customer_id}/claims
GET     /api/v1/customers/{customer_id}/quotes
GET     /api/v1/customers/{customer_id}/payments
GET     /api/v1/customers/{customer_id}/dashboard
GET     /api/v1/customers/search
```

#### Quote Endpoints
```
GET     /api/v1/quotes
POST    /api/v1/quotes
GET     /api/v1/quotes/{quote_id}
PUT     /api/v1/quotes/{quote_id}
PATCH   /api/v1/quotes/{quote_id}
DELETE  /api/v1/quotes/{quote_id}

# Additional operations
POST    /api/v1/quotes/{quote_id}/accept
POST    /api/v1/quotes/{quote_id}/convert
POST    /api/v1/quotes/calculate           # Calculate premium
GET     /api/v1/quotes/by-customer/{customer_id}
```

#### Risk Assessment Endpoints
```
GET     /api/v1/risk-assessments
POST    /api/v1/risk-assessments
GET     /api/v1/risk-assessments/{assessment_id}
PUT     /api/v1/risk-assessments/{assessment_id}
PATCH   /api/v1/risk-assessments/{assessment_id}
DELETE  /api/v1/risk-assessments/{assessment_id}

# Additional operations
POST    /api/v1/risk-assessments/calculate
GET     /api/v1/risk-assessments/by-policy/{policy_id}
GET     /api/v1/risk-assessments/by-underwriter/{underwriter_id}
```

#### Payment Endpoints
```
GET     /api/v1/payments
POST    /api/v1/payments
GET     /api/v1/payments/{payment_id}
PUT     /api/v1/payments/{payment_id}
PATCH   /api/v1/payments/{payment_id}
DELETE  /api/v1/payments/{payment_id}

# Additional operations
POST    /api/v1/payments/process
POST    /api/v1/payments/refund
GET     /api/v1/payments/by-policy/{policy_id}
GET     /api/v1/payments/by-claim/{claim_id}
GET     /api/v1/payments/pending
```

#### Document Endpoints
```
GET     /api/v1/documents
POST    /api/v1/documents
GET     /api/v1/documents/{document_id}
PUT     /api/v1/documents/{document_id}
DELETE  /api/v1/documents/{document_id}

# Additional operations
GET     /api/v1/documents/{document_id}/download
POST    /api/v1/documents/upload
POST    /api/v1/documents/{document_id}/verify
GET     /api/v1/documents/by-policy/{policy_id}
GET     /api/v1/documents/by-claim/{claim_id}
```

#### Agent Endpoints
```
GET     /api/v1/agents
POST    /api/v1/agents
GET     /api/v1/agents/{agent_id}
PUT     /api/v1/agents/{agent_id}
PATCH   /api/v1/agents/{agent_id}
DELETE  /api/v1/agents/{agent_id}

# Additional operations
GET     /api/v1/agents/{agent_id}/policies
GET     /api/v1/agents/{agent_id}/commissions
GET     /api/v1/agents/{agent_id}/performance
GET     /api/v1/agents/{agent_id}/customers
GET     /api/v1/agents/top-performers
GET     /api/v1/agents/by-specialization/{specialization}
```

#### Insurer Endpoints
```
GET     /api/v1/insurers
POST    /api/v1/insurers
GET     /api/v1/insurers/{insurer_id}
PUT     /api/v1/insurers/{insurer_id}
PATCH   /api/v1/insurers/{insurer_id}
DELETE  /api/v1/insurers/{insurer_id}

# Additional operations
GET     /api/v1/insurers/{insurer_id}/policies
GET     /api/v1/insurers/{insurer_id}/statistics
GET     /api/v1/insurers/{insurer_id}/ratings
```

#### Premium Endpoints
```
GET     /api/v1/premiums
POST    /api/v1/premiums
GET     /api/v1/premiums/{premium_id}
PUT     /api/v1/premiums/{premium_id}
PATCH   /api/v1/premiums/{premium_id}
DELETE  /api/v1/premiums/{premium_id}

# Additional operations
GET     /api/v1/premiums/overdue
GET     /api/v1/premiums/due-soon
GET     /api/v1/premiums/by-policy/{policy_id}
POST    /api/v1/premiums/{premium_id}/pay
GET     /api/v1/premiums/calculate
```

#### Coverage Endpoints
```
GET     /api/v1/coverages
POST    /api/v1/coverages
GET     /api/v1/coverages/{coverage_id}
PUT     /api/v1/coverages/{coverage_id}
PATCH   /api/v1/coverages/{coverage_id}
DELETE  /api/v1/coverages/{coverage_id}

# Additional operations
GET     /api/v1/coverages/by-policy/{policy_id}
GET     /api/v1/coverages/types
GET     /api/v1/coverages/available
```

#### Beneficiary Endpoints
```
GET     /api/v1/beneficiaries
POST    /api/v1/beneficiaries
GET     /api/v1/beneficiaries/{beneficiary_id}
PUT     /api/v1/beneficiaries/{beneficiary_id}
PATCH   /api/v1/beneficiaries/{beneficiary_id}
DELETE  /api/v1/beneficiaries/{beneficiary_id}

# Additional operations
GET     /api/v1/beneficiaries/by-policy/{policy_id}
POST    /api/v1/beneficiaries/{beneficiary_id}/verify
```

#### Underwriter Endpoints
```
GET     /api/v1/underwriters
POST    /api/v1/underwriters
GET     /api/v1/underwriters/{underwriter_id}
PUT     /api/v1/underwriters/{underwriter_id}
PATCH   /api/v1/underwriters/{underwriter_id}
DELETE  /api/v1/underwriters/{underwriter_id}

# Additional operations
GET     /api/v1/underwriters/{underwriter_id}/assessments
GET     /api/v1/underwriters/{underwriter_id}/statistics
GET     /api/v1/underwriters/{underwriter_id}/workload
```

#### Incident Endpoints
```
GET     /api/v1/incidents
POST    /api/v1/incidents
GET     /api/v1/incidents/{incident_id}
PUT     /api/v1/incidents/{incident_id}
PATCH   /api/v1/incidents/{incident_id}
DELETE  /api/v1/incidents/{incident_id}

# Additional operations
GET     /api/v1/incidents/by-policy/{policy_id}
GET     /api/v1/incidents/by-claim/{claim_id}
GET     /api/v1/incidents/by-type/{incident_type}
GET     /api/v1/incidents/by-date-range
```

#### Vehicle Endpoints
```
GET     /api/v1/vehicles
POST    /api/v1/vehicles
GET     /api/v1/vehicles/{vehicle_id}
PUT     /api/v1/vehicles/{vehicle_id}
PATCH   /api/v1/vehicles/{vehicle_id}
DELETE  /api/v1/vehicles/{vehicle_id}

# Additional operations
GET     /api/v1/vehicles/by-policy/{policy_id}
GET     /api/v1/vehicles/by-vin/{vin_number}
GET     /api/v1/vehicles/by-customer/{customer_id}
```

#### Property Endpoints
```
GET     /api/v1/properties
POST    /api/v1/properties
GET     /api/v1/properties/{property_id}
PUT     /api/v1/properties/{property_id}
PATCH   /api/v1/properties/{property_id}
DELETE  /api/v1/properties/{property_id}

# Additional operations
GET     /api/v1/properties/by-policy/{policy_id}
GET     /api/v1/properties/by-customer/{customer_id}
GET     /api/v1/properties/valuation/{property_id}
```

#### Medical Record Endpoints
```
GET     /api/v1/medical-records
POST    /api/v1/medical-records
GET     /api/v1/medical-records/{record_id}
PUT     /api/v1/medical-records/{record_id}
PATCH   /api/v1/medical-records/{record_id}
DELETE  /api/v1/medical-records/{record_id}

# Additional operations
GET     /api/v1/medical-records/by-customer/{customer_id}
GET     /api/v1/medical-records/by-policy/{policy_id}
POST    /api/v1/medical-records/{record_id}/verify
```

#### Policy Renewal Endpoints
```
GET     /api/v1/policy-renewals
POST    /api/v1/policy-renewals
GET     /api/v1/policy-renewals/{renewal_id}
PUT     /api/v1/policy-renewals/{renewal_id}
PATCH   /api/v1/policy-renewals/{renewal_id}
DELETE  /api/v1/policy-renewals/{renewal_id}

# Additional operations
GET     /api/v1/policy-renewals/pending
GET     /api/v1/policy-renewals/by-policy/{policy_id}
POST    /api/v1/policy-renewals/{renewal_id}/approve
POST    /api/v1/policy-renewals/{renewal_id}/reject
```

#### Commission Endpoints
```
GET     /api/v1/commissions
POST    /api/v1/commissions
GET     /api/v1/commissions/{commission_id}
PUT     /api/v1/commissions/{commission_id}
PATCH   /api/v1/commissions/{commission_id}
DELETE  /api/v1/commissions/{commission_id}

# Additional operations
GET     /api/v1/commissions/by-agent/{agent_id}
GET     /api/v1/commissions/pending
GET     /api/v1/commissions/by-period
POST    /api/v1/commissions/{commission_id}/approve
POST    /api/v1/commissions/{commission_id}/pay
POST    /api/v1/commissions/calculate
```

#### Endorsement Endpoints
```
GET     /api/v1/endorsements
POST    /api/v1/endorsements
GET     /api/v1/endorsements/{endorsement_id}
PUT     /api/v1/endorsements/{endorsement_id}
PATCH   /api/v1/endorsements/{endorsement_id}
DELETE  /api/v1/endorsements/{endorsement_id}

# Additional operations
GET     /api/v1/endorsements/by-policy/{policy_id}
POST    /api/v1/endorsements/{endorsement_id}/approve
POST    /api/v1/endorsements/{endorsement_id}/implement
GET     /api/v1/endorsements/pending
```

#### Analytics & Reports Endpoints
```
GET     /api/v1/dashboard/summary
GET     /api/v1/dashboard/statistics
GET     /api/v1/dashboard/trends
GET     /api/v1/reports/policies
GET     /api/v1/reports/claims
GET     /api/v1/reports/revenue
GET     /api/v1/reports/agent-performance
GET     /api/v1/reports/claim-settlement-ratio
GET     /api/v1/reports/customer-retention
GET     /api/v1/reports/premium-breakdown
POST    /api/v1/reports/export
POST    /api/v1/reports/custom
```

### Bulk Operations

All entities support bulk operations:

```
POST    /api/v1/{entity}/bulk-create         - Create multiple entities
POST    /api/v1/{entity}/bulk-update         - Update multiple entities
POST    /api/v1/{entity}/bulk-delete         - Delete multiple entities
POST    /api/v1/{entity}/import              - Import from CSV/Excel
GET     /api/v1/{entity}/export              - Export to CSV/Excel/PDF
```

### System Management Endpoints

```
GET     /api/v1/system/health                - Health check
GET     /api/v1/system/ready                 - Readiness check
GET     /api/v1/system/metrics               - Prometheus metrics
GET     /api/v1/system/info                  - System information
POST    /api/v1/system/cache/clear           - Clear cache
GET     /api/v1/audit-logs                   - Audit trail
GET     /api/v1/audit-logs/by-entity/{entity_type}/{entity_id}
GET     /api/v1/audit-logs/by-user/{user_id}
```

### Standard Query Parameters

All list endpoints support:
- `page`: Page number (default: 1)
- `size`: Items per page (default: 20, max: 100)
- `sort_by`: Field to sort by
- `order`: Sort order (asc/desc)
- `search`: Full-text search
- Entity-specific filters (e.g., `status`, `date_from`, `date_to`)

### Response Format

**Success Response:**
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful",
  "timestamp": "2026-04-09T19:30:00Z"
}
```

**List Response with Pagination:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 150,
    "page": 1,
    "size": 20,
    "pages": 8
  },
  "timestamp": "2026-04-09T19:30:00Z"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [...]
  },
  "timestamp": "2026-04-09T19:30:00Z"
}
```

## Authentication & Authorization

### JWT-Based Authentication

**Login Flow:**
1. User provides credentials (email/password)
2. Server validates and returns JWT access token + refresh token
3. Client includes access token in `Authorization: Bearer <token>` header
4. Server validates token for protected endpoints

**Token Structure:**
- Access token: 30 minutes expiry
- Refresh token: 7 days expiry
- Stored user info: user_id, role, permissions

### Role-Based Access Control (RBAC)

**Roles:**
- `super_admin`: Full system access
- `admin`: Administrative operations
- `underwriter`: Risk assessment, policy approval
- `agent`: Create quotes, policies, customer management
- `claims_adjuster`: Claim processing
- `customer`: View own policies, submit claims
- `auditor`: Read-only access for compliance

**Permission Examples:**
- `policy:create`, `policy:read`, `policy:update`, `policy:delete`
- `claim:approve`, `claim:reject`, `claim:settle`
- `customer:create`, `customer:read`, `customer:update`

### Security Measures

1. **Password Security**
   - Bcrypt hashing with salt
   - Minimum 8 characters, complexity requirements
   - Password history (prevent reuse)

2. **Rate Limiting**
   - 100 requests/minute per IP for authenticated users
   - 20 requests/minute for unauthenticated
   - Stricter limits for sensitive operations (login: 5 attempts/15 min)

3. **Data Encryption**
   - TLS 1.3 for data in transit
   - Sensitive fields encrypted at rest (SSN, medical data)
   - Database-level encryption for backups

4. **Audit Logging**
   - Log all create, update, delete operations
   - Track user actions with timestamps
   - Separate audit table with retention policy

## Performance Optimization

### 1. Database Optimization

**Query Optimization:**
- Use select_related/joinedload for foreign keys
- Use subqueryload for collections
- Implement pagination for all list queries
- Add appropriate indexes based on query patterns

**Connection Pooling:**
```python
# SQLAlchemy async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### 2. Caching Strategy

**Redis Cache:**
- Cache frequently accessed data (insurers, coverage types)
- Cache TTL: 5-60 minutes based on data volatility
- Cache invalidation on updates

**Cache Patterns:**
- Read-through cache for GET operations
- Write-through cache for updates
- Cache-aside for complex queries

### 3. Async Operations

- Use `async/await` for all database operations
- Parallel processing with `asyncio.gather()` for independent queries
- Background tasks with Celery for:
  - Email notifications
  - Report generation
  - Premium calculations
  - Policy renewal reminders

### 4. Pagination & Filtering

- Default page size: 20 items
- Maximum page size: 100 items
- Cursor-based pagination for large datasets
- Efficient filtering with indexed fields

### 5. API Response Optimization

- Response compression (gzip)
- Field selection (allow clients to specify fields)
- Lazy loading of related entities
- HTTP caching headers (ETag, Last-Modified)

## Error Handling

### Exception Hierarchy

```python
BaseAPIException
├── ValidationException (400)
├── UnauthorizedException (401)
├── ForbiddenException (403)
├── NotFoundException (404)
├── ConflictException (409)
├── UnprocessableException (422)
└── InternalServerException (500)
```

### Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_FAILED`: Invalid credentials
- `AUTHORIZATION_FAILED`: Insufficient permissions
- `RESOURCE_NOT_FOUND`: Entity not found
- `DUPLICATE_ENTRY`: Unique constraint violation
- `BUSINESS_RULE_VIOLATION`: Business logic error
- `DATABASE_ERROR`: Database operation failed
- `EXTERNAL_SERVICE_ERROR`: Third-party service error

### Global Exception Handler

FastAPI middleware to catch all exceptions and return standardized error responses.

## Testing Strategy

### 1. Unit Tests
- Test CRUD operations
- Test business logic in services
- Test utility functions
- Coverage target: 80%+

### 2. Integration Tests
- Test API endpoints with test database
- Test database transactions
- Test authentication flow

### 3. Load Testing
- Use Locust or Apache JMeter
- Test concurrent users: 100, 500, 1000
- Identify bottlenecks

### 4. Test Data
- Factory pattern for test fixtures
- Faker library for realistic test data
- Separate test database

## Monitoring & Logging

### Application Logging
- Structured logging with JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log rotation and retention (30 days)

### Monitoring Metrics
- Request/response times
- Database query performance
- Cache hit/miss ratio
- Error rates by endpoint
- Active user sessions

### Tools
- **Logging**: Python logging + structlog
- **Monitoring**: Prometheus + Grafana
- **APM**: Sentry for error tracking
- **Health checks**: `/health` and `/ready` endpoints

## Deployment

### Docker Setup

```dockerfile
# Multi-stage build for optimization
# Python 3.11 slim image
# Non-root user for security
# Environment-based configuration
```

### Environment Configuration

**Required Environment Variables:**
```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<strong-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000"]
```

### CI/CD Pipeline

1. **Build:** Run tests, linting (flake8, black, mypy)
2. **Test:** Run full test suite
3. **Build Docker Image**
4. **Push to Registry**
5. **Deploy:** Rolling deployment with health checks

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Documentation

### Swagger UI
- Accessible at `/docs`
- Interactive API testing
- Request/response examples
- Authentication integration

### ReDoc
- Alternative documentation at `/redoc`
- Better for printing and sharing

### Schema Descriptions
- All Pydantic models include field descriptions
- Examples for complex schemas
- Enum value descriptions

## Performance Targets

- **Response Time:** 
  - GET operations: < 100ms (p95)
  - POST/PUT operations: < 200ms (p95)
  - Complex queries: < 500ms (p95)

- **Throughput:**
  - 1000 requests/second per instance
  - Horizontal scaling capability

- **Database:**
  - Query time: < 50ms (p95)
  - Connection pool utilization: < 80%

- **Availability:**
  - Uptime: 99.9%
  - Zero-downtime deployments

## Security Checklist

- [ ] HTTPS only (TLS 1.3)
- [ ] JWT token authentication
- [ ] Role-based access control
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] Secure password storage (bcrypt)
- [ ] Audit logging
- [ ] Data encryption at rest
- [ ] Regular security updates
- [ ] Environment variable management
- [ ] Secrets management (no hardcoded secrets)
- [ ] CORS configuration
- [ ] HTTP security headers

## Future Enhancements

1. **GraphQL API**: Alternative to REST for flexible queries
2. **WebSocket Support**: Real-time notifications
3. **Microservices**: Break into smaller services if needed
4. **Event Sourcing**: Track all state changes
5. **CQRS Pattern**: Separate read/write models
6. **Multi-tenancy**: Support multiple insurers
7. **API Gateway**: Centralized routing and rate limiting
8. **Service Mesh**: Istio for advanced traffic management
9. **Machine Learning**: Premium prediction, fraud detection
10. **Mobile API**: Optimized endpoints for mobile apps

## Code Examples

### 1. Base Model (models/base.py)

```python
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all models"""
    pass

class BaseModel(Base):
    """Abstract base model with common fields"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
```

### 2. Policy Model Example (models/policy.py)

```python
from sqlalchemy import Column, String, Integer, Numeric, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.enums.policy_enums import PolicyType, PolicyStatus

class Policy(BaseModel):
    __tablename__ = "policies"
    
    policy_number = Column(String(50), unique=True, nullable=False, index=True)
    policy_type = Column(SQLEnum(PolicyType), nullable=False)
    policy_holder_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    insurer_id = Column(Integer, ForeignKey("insurers.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(SQLEnum(PolicyStatus), nullable=False, index=True)
    premium_amount = Column(Numeric(12, 2), nullable=False)
    coverage_amount = Column(Numeric(15, 2), nullable=False)
    deductible = Column(Numeric(10, 2), nullable=False)
    renewal_date = Column(Date)
    
    # Relationships
    policy_holder = relationship("Customer", back_populates="policies")
    insurer = relationship("Insurer", back_populates="policies")
    claims = relationship("Claim", back_populates="policy", cascade="all, delete-orphan")
    premiums = relationship("Premium", back_populates="policy", cascade="all, delete-orphan")
    coverages = relationship("Coverage", back_populates="policy", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiary", back_populates="policy", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="policy")
```

### 3. Pydantic Schema Examples (schemas/policy.py)

```python
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.enums.policy_enums import PolicyType, PolicyStatus

class PolicyBase(BaseModel):
    """Base schema for Policy"""
    policy_number: str = Field(..., min_length=1, max_length=50)
    policy_type: PolicyType
    policy_holder_id: int
    insurer_id: int
    start_date: date
    end_date: date
    premium_amount: Decimal = Field(..., gt=0, decimal_places=2)
    coverage_amount: Decimal = Field(..., gt=0, decimal_places=2)
    deductible: Decimal = Field(..., ge=0, decimal_places=2)

class PolicyCreate(PolicyBase):
    """Schema for creating a new policy"""
    pass

class PolicyUpdate(BaseModel):
    """Schema for updating a policy"""
    policy_type: Optional[PolicyType] = None
    status: Optional[PolicyStatus] = None
    premium_amount: Optional[Decimal] = None
    coverage_amount: Optional[Decimal] = None
    deductible: Optional[Decimal] = None
    end_date: Optional[date] = None

class PolicyResponse(PolicyBase):
    """Schema for policy response"""
    id: int
    status: PolicyStatus
    renewal_date: Optional[date]
    created_date: datetime
    last_modified_date: datetime
    
    model_config = ConfigDict(from_attributes=True)
```

### 4. Base CRUD Class (crud/base.py)

```python
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Get a single record by ID"""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    
    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination"""
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record"""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        """Soft delete a record"""
        obj = await self.get(db=db, id=id)
        if obj:
            obj.deleted_at = datetime.utcnow()
            await db.commit()
        return obj
```

### 5. API Endpoint Example (api/v1/policies.py)

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud.policy import policy as policy_crud
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyResponse
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[PolicyResponse])
async def list_policies(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> List[PolicyResponse]:
    """List all policies with pagination"""
    policies = await policy_crud.get_multi(db=db, skip=skip, limit=limit)
    return policies

@router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    *,
    db: AsyncSession = Depends(deps.get_db),
    policy_in: PolicyCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> PolicyResponse:
    """Create new policy"""
    policy = await policy_crud.create(db=db, obj_in=policy_in)
    return policy

@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> PolicyResponse:
    """Get policy by ID"""
    policy = await policy_crud.get(db=db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    return policy

@router.patch("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: int,
    policy_in: PolicyUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> PolicyResponse:
    """Update policy"""
    policy = await policy_crud.get(db=db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    policy = await policy_crud.update(db=db, db_obj=policy, obj_in=policy_in)
    return policy

@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Soft delete policy"""
    policy = await policy_crud.get(db=db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    await policy_crud.remove(db=db, id=policy_id)
```

### 6. Authentication Dependency (api/deps.py)

```python
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM
from app.database import async_session
from app.models.user import User
from app.crud.user import user as user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency"""
    async with async_session() as session:
        yield session

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_crud.get(db=db, id=user_id)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
```

## File Storage Strategy

### Storage Options

**1. Local File System (Development/Small Scale)**
```python
# utils/file_handler.py
import aiofiles
from pathlib import Path

async def save_file_locally(file_content: bytes, file_path: str):
    """Save file to local filesystem"""
    path = Path(f"uploads/{file_path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    
    async with aiofiles.open(path, 'wb') as f:
        await f.write(file_content)
    
    return str(path)
```

**2. AWS S3 (Production - Recommended)**
```python
# services/storage_service.py
import aioboto3
from typing import BinaryIO
from app.core.config import settings

class S3StorageService:
    def __init__(self):
        self.bucket_name = settings.AWS_S3_BUCKET
        self.region = settings.AWS_REGION
    
    async def upload_file(
        self,
        file_content: bytes,
        file_key: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """Upload file to S3"""
        session = aioboto3.Session()
        async with session.client(
            's3',
            region_name=self.region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        ) as s3_client:
            await s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_content,
                ContentType=content_type
            )
            
            # Return S3 URL
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_key}"
    
    async def get_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for secure file access"""
        session = aioboto3.Session()
        async with session.client('s3', region_name=self.region) as s3_client:
            url = await s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=expiration
            )
            return url
    
    async def delete_file(self, file_key: str):
        """Delete file from S3"""
        session = aioboto3.Session()
        async with session.client('s3', region_name=self.region) as s3_client:
            await s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)
```

### File Organization Strategy

```
s3://insurance-documents/
├── policies/
│   ├── {policy_id}/
│   │   ├── documents/
│   │   │   ├── {year}/{month}/{filename}
│   │   └── photos/
├── claims/
│   ├── {claim_id}/
│   │   ├── evidence/
│   │   ├── reports/
│   │   └── photos/
├── customers/
│   ├── {customer_id}/
│   │   ├── identification/
│   │   ├── medical/
│   │   └── contracts/
└── temp/
    └── {upload_session_id}/
```

### File Upload Handling

```python
# api/v1/documents.py
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.document_service import DocumentService

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    entity_type: str = "policy",
    entity_id: int = ...,
    document_type: str = ...,
    db: AsyncSession = Depends(deps.get_db),
    document_service: DocumentService = Depends(deps.get_document_service),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Upload document with validation"""
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'application/pdf', 'application/msword']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed"
        )
    
    # Validate file size (max 10MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB")
    
    # Upload to storage
    file_url = await document_service.save_document(
        file_content=content,
        filename=file.filename,
        content_type=file.content_type,
        entity_type=entity_type,
        entity_id=entity_id,
        document_type=document_type,
        uploaded_by_id=current_user.id,
        db=db
    )
    
    return {"file_url": file_url, "message": "File uploaded successfully"}
```

### Security & Access Control

**File Size Limits:**
- Images: 5MB max
- PDFs: 10MB max
- Excel/CSV: 5MB max
- Medical documents: 10MB max

**Allowed MIME Types:**
```python
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif',
    'application/pdf',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/csv'
}
```

**Virus Scanning (Optional but Recommended):**
```python
# Using ClamAV
import clamd

async def scan_file_for_virus(file_content: bytes) -> bool:
    """Scan file for viruses"""
    cd = clamd.ClamdUnixSocket()
    result = cd.scan_stream(file_content)
    return result['stream'][0] == 'OK'
```

## Third-Party Integrations

### 1. Payment Gateway Integration

**Stripe Integration:**
```python
# integrations/payment_gateway.py
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentGatewayService:
    async def process_payment(
        self,
        amount: Decimal,
        currency: str = "usd",
        payment_method_id: str = ...,
        customer_email: str = ...,
        metadata: dict = None
    ):
        """Process payment through Stripe"""
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                payment_method=payment_method_id,
                confirm=True,
                receipt_email=customer_email,
                metadata=metadata or {}
            )
            
            return {
                "success": True,
                "transaction_id": payment_intent.id,
                "status": payment_intent.status
            }
        except stripe.error.CardError as e:
            return {
                "success": False,
                "error": e.user_message
            }
    
    async def create_refund(self, payment_intent_id: str, amount: Optional[Decimal] = None):
        """Process refund"""
        refund_data = {"payment_intent": payment_intent_id}
        if amount:
            refund_data["amount"] = int(amount * 100)
        
        refund = stripe.Refund.create(**refund_data)
        return refund
```

### 2. Email Service Integration

**SendGrid Integration:**
```python
# integrations/email_service.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = settings.FROM_EMAIL
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: str = None
    ):
        """Send email via SendGrid"""
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
            plain_text_content=plain_content
        )
        
        try:
            response = self.client.send(message)
            return {"success": True, "status_code": response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def send_policy_renewal_reminder(self, policy, customer):
        """Send policy renewal reminder"""
        subject = f"Policy Renewal Reminder - {policy.policy_number}"
        html_content = f"""
        <html>
            <body>
                <h2>Policy Renewal Reminder</h2>
                <p>Dear {customer.first_name},</p>
                <p>Your policy {policy.policy_number} is due for renewal on {policy.renewal_date}.</p>
                <p>Please contact us to renew your policy.</p>
            </body>
        </html>
        """
        
        return await self.send_email(customer.email, subject, html_content)
```

### 3. SMS Service Integration

**Twilio Integration:**
```python
# integrations/sms_service.py
from twilio.rest import Client
from app.core.config import settings

class SMSService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = settings.TWILIO_PHONE_NUMBER
    
    async def send_sms(self, to_number: str, message: str):
        """Send SMS via Twilio"""
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return {"success": True, "message_sid": message.sid}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def send_claim_status_update(self, claim, customer):
        """Send claim status update SMS"""
        message = f"Claim {claim.claim_number}: Status updated to {claim.status}. Check your email for details."
        return await self.send_sms(customer.phone_number, message)
```

### 4. Document Signing Integration

**DocuSign Integration:**
```python
# integrations/document_signing.py
from docusign_esign import ApiClient, EnvelopesApi
from docusign_esign.client.api_exception import ApiException

class DocumentSigningService:
    def __init__(self):
        self.api_client = ApiClient()
        self.api_client.host = settings.DOCUSIGN_BASE_PATH
        self.api_client.set_default_header("Authorization", f"Bearer {settings.DOCUSIGN_ACCESS_TOKEN}")
    
    async def send_document_for_signature(
        self,
        signer_email: str,
        signer_name: str,
        document_path: str,
        document_name: str
    ):
        """Send document for electronic signature"""
        try:
            # Create envelope definition
            envelope_definition = {
                "emailSubject": f"Please sign: {document_name}",
                "documents": [{
                    "documentBase64": self._get_document_base64(document_path),
                    "name": document_name,
                    "fileExtension": "pdf",
                    "documentId": "1"
                }],
                "recipients": {
                    "signers": [{
                        "email": signer_email,
                        "name": signer_name,
                        "recipientId": "1",
                        "routingOrder": "1"
                    }]
                },
                "status": "sent"
            }
            
            envelopes_api = EnvelopesApi(self.api_client)
            results = envelopes_api.create_envelope(
                settings.DOCUSIGN_ACCOUNT_ID,
                envelope_definition=envelope_definition
            )
            
            return {"success": True, "envelope_id": results.envelope_id}
        except ApiException as e:
            return {"success": False, "error": str(e)}
```

## Business Logic & Workflows

### Premium Calculation Algorithm

```python
# utils/calculators.py
from decimal import Decimal
from typing import Dict

class PremiumCalculator:
    """Calculate insurance premiums based on various factors"""
    
    BASE_RATES = {
        'auto': Decimal('500.00'),
        'health': Decimal('300.00'),
        'life': Decimal('400.00'),
        'property': Decimal('800.00')
    }
    
    def calculate_auto_premium(
        self,
        vehicle_value: Decimal,
        driver_age: int,
        accident_history: int,
        vehicle_age: int,
        coverage_type: str
    ) -> Decimal:
        """Calculate auto insurance premium"""
        base_rate = self.BASE_RATES['auto']
        
        # Vehicle value factor (0.5% - 2% of vehicle value)
        vehicle_factor = vehicle_value * Decimal('0.015')
        
        # Age factor
        if driver_age < 25:
            age_factor = Decimal('1.5')
        elif driver_age < 30:
            age_factor = Decimal('1.2')
        elif driver_age < 60:
            age_factor = Decimal('1.0')
        else:
            age_factor = Decimal('1.1')
        
        # Accident history factor
        accident_factor = Decimal('1.0') + (Decimal('0.2') * accident_history)
        
        # Vehicle age factor
        if vehicle_age > 10:
            vehicle_age_factor = Decimal('0.9')
        elif vehicle_age > 5:
            vehicle_age_factor = Decimal('1.0')
        else:
            vehicle_age_factor = Decimal('1.1')
        
        # Coverage type multiplier
        coverage_multipliers = {
            'liability': Decimal('1.0'),
            'collision': Decimal('1.3'),
            'comprehensive': Decimal('1.5')
        }
        coverage_factor = coverage_multipliers.get(coverage_type, Decimal('1.0'))
        
        # Calculate final premium
        premium = (
            (base_rate + vehicle_factor) *
            age_factor *
            accident_factor *
            vehicle_age_factor *
            coverage_factor
        )
        
        return premium.quantize(Decimal('0.01'))
    
    def calculate_health_premium(
        self,
        age: int,
        bmi: float,
        smoking_status: bool,
        pre_existing_conditions: int,
        coverage_amount: Decimal
    ) -> Decimal:
        """Calculate health insurance premium"""
        base_rate = self.BASE_RATES['health']
        
        # Age factor
        age_factor = Decimal('1.0') + (Decimal(age) - Decimal('25')) * Decimal('0.02')
        
        # BMI factor
        if bmi < 18.5 or bmi > 30:
            bmi_factor = Decimal('1.3')
        elif bmi > 25:
            bmi_factor = Decimal('1.1')
        else:
            bmi_factor = Decimal('1.0')
        
        # Smoking factor
        smoking_factor = Decimal('1.5') if smoking_status else Decimal('1.0')
        
        # Pre-existing conditions factor
        condition_factor = Decimal('1.0') + (Decimal('0.15') * pre_existing_conditions)
        
        # Coverage amount factor
        coverage_factor = coverage_amount / Decimal('100000')
        
        premium = (
            base_rate *
            age_factor *
            bmi_factor *
            smoking_factor *
            condition_factor *
            coverage_factor
        )
        
        return premium.quantize(Decimal('0.01'))
```

### Commission Calculation Rules

```python
# utils/calculators.py (continued)
class CommissionCalculator:
    """Calculate agent commissions"""
    
    COMMISSION_TIERS = {
        'new_business': {
            'tier1': {'min': 0, 'max': 10, 'rate': Decimal('0.15')},      # 15%
            'tier2': {'min': 10, 'max': 25, 'rate': Decimal('0.18')},     # 18%
            'tier3': {'min': 25, 'max': 50, 'rate': Decimal('0.20')},     # 20%
            'tier4': {'min': 50, 'max': float('inf'), 'rate': Decimal('0.22')}  # 22%
        },
        'renewal': {
            'rate': Decimal('0.05')  # 5% for renewals
        },
        'referral': {
            'rate': Decimal('0.03')  # 3% for referrals
        }
    }
    
    def calculate_commission(
        self,
        premium_amount: Decimal,
        commission_type: str,
        policies_sold_this_month: int = 0
    ) -> Decimal:
        """Calculate commission based on type and tier"""
        if commission_type == 'new_business':
            # Tiered commission based on policies sold
            for tier in self.COMMISSION_TIERS['new_business'].values():
                if tier['min'] <= policies_sold_this_month < tier['max']:
                    rate = tier['rate']
                    break
        else:
            rate = self.COMMISSION_TIERS[commission_type]['rate']
        
        commission = premium_amount * rate
        return commission.quantize(Decimal('0.01'))
```

### Risk Scoring Model

```python
# services/underwriting_service.py
class UnderwritingService:
    """Risk assessment and underwriting logic"""
    
    def calculate_risk_score(
        self,
        customer_age: int,
        income: Decimal,
        credit_score: int,
        occupation_risk: str,
        previous_claims: int,
        coverage_amount: Decimal
    ) -> Dict:
        """Calculate risk score (0-100, lower is better)"""
        score = 50  # Base score
        
        # Age factor (+/- 10 points)
        if customer_age < 25:
            score += 10
        elif customer_age < 35:
            score += 5
        elif 35 <= customer_age <= 55:
            score -= 5
        else:
            score += 3
        
        # Income factor (+/- 10 points)
        income_to_coverage = float(income / coverage_amount)
        if income_to_coverage > 0.5:
            score -= 10
        elif income_to_coverage > 0.3:
            score -= 5
        elif income_to_coverage < 0.1:
            score += 10
        
        # Credit score factor (+/- 15 points)
        if credit_score >= 750:
            score -= 15
        elif credit_score >= 650:
            score -= 5
        elif credit_score < 550:
            score += 15
        else:
            score += 5
        
        # Occupation risk factor (+/- 10 points)
        occupation_scores = {
            'low': -10,
            'medium': 0,
            'high': 10,
            'very_high': 15
        }
        score += occupation_scores.get(occupation_risk, 0)
        
        # Previous claims factor (+ points)
        score += previous_claims * 5
        
        # Normalize score (0-100)
        score = max(0, min(100, score))
        
        # Determine risk category
        if score < 30:
            category = 'low'
            recommendation = 'approve'
        elif score < 50:
            category = 'medium'
            recommendation = 'approve'
        elif score < 70:
            category = 'high'
            recommendation = 'approve_with_conditions'
        else:
            category = 'very_high'
            recommendation = 'reject'
        
        return {
            'risk_score': score,
            'risk_category': category,
            'recommendation': recommendation
        }
```

### Claim Settlement Workflow

```python
# services/claim_service.py
class ClaimService:
    """Claim processing business logic"""
    
    async def process_claim_submission(
        self,
        claim_id: int,
        db: AsyncSession
    ):
        """Process new claim submission"""
        claim = await claim_crud.get(db=db, id=claim_id)
        
        # Step 1: Validate claim against policy
        policy = claim.policy
        if not self._is_claim_valid(claim, policy):
            await self._reject_claim(claim, "Policy conditions not met", db)
            return
        
        # Step 2: Check for fraud indicators
        fraud_score = await self._check_fraud_indicators(claim)
        if fraud_score > 70:
            claim.status = "under_investigation"
            await db.commit()
            await self._notify_fraud_team(claim)
            return
        
        # Step 3: Auto-approve small claims
        if claim.claim_amount < Decimal('5000'):
            await self._approve_claim(claim, db)
            return
        
        # Step 4: Assign to adjuster for review
        await self._assign_to_adjuster(claim, db)
        await self._notify_adjuster(claim)
    
    def _is_claim_valid(self, claim, policy) -> bool:
        """Validate claim against policy terms"""
        # Check if policy is active
        if policy.status != 'active':
            return False
        
        # Check if claim is within coverage dates
        if not (policy.start_date <= claim.incident_date <= policy.end_date):
            return False
        
        # Check if claim amount is within coverage limit
        if claim.claim_amount > policy.coverage_amount:
            return False
        
        # Check waiting period (e.g., 30 days for some policies)
        days_since_policy_start = (claim.incident_date - policy.start_date).days
        if days_since_policy_start < 30:
            return False
        
        return True
    
    async def _check_fraud_indicators(self, claim) -> int:
        """Calculate fraud risk score"""
        score = 0
        
        # Multiple claims in short period
        recent_claims = await self._get_recent_claims(claim.policy_id, days=180)
        if len(recent_claims) > 2:
            score += 30
        
        # Claim amount suspiciously close to coverage limit
        if claim.claim_amount > claim.policy.coverage_amount * Decimal('0.95'):
            score += 20
        
        # Claim submitted soon after policy start
        days_after_start = (claim.claim_date - claim.policy.start_date).days
        if days_after_start < 30:
            score += 25
        
        # Missing or incomplete documentation
        if not claim.documents or len(claim.documents) < 2:
            score += 15
        
        return score
```

## Backup & Disaster Recovery

### Backup Strategy

**Database Backups:**
```bash
# Daily automated backups
0 2 * * * /opt/scripts/backup_postgres.sh

# backup_postgres.sh
#!/bin/bash
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="insurance_db"

# Create backup
pg_dump -U postgres -h localhost $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz s3://insurance-backups/postgres/daily/

# Keep only last 30 days locally
find $BACKUP_DIR -type f -mtime +30 -delete
```

**Backup Schedule:**
- **Full backup**: Daily at 2 AM
- **Incremental backup**: Every 6 hours
- **Transaction log backup**: Every 15 minutes
- **Configuration backup**: Weekly

**Retention Policy:**
- Daily backups: 30 days (local + S3)
- Weekly backups: 6 months (S3)
- Monthly backups: 7 years (S3 Glacier)

### Point-in-Time Recovery (PITR)

```sql
-- Enable WAL archiving for PITR
-- postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'aws s3 cp %p s3://insurance-backups/wal/%f'
archive_timeout = 300
```

### Disaster Recovery Plan

**RTO (Recovery Time Objective): 4 hours**
**RPO (Recovery Point Objective): 15 minutes**

**Recovery Steps:**
1. Assess the incident and declare disaster
2. Spin up standby infrastructure (if not already running)
3. Restore latest backup
4. Apply WAL files for PITR
5. Update DNS to point to new infrastructure
6. Verify data integrity
7. Resume operations
8. Post-mortem analysis

### High Availability Setup

```yaml
# docker-compose.ha.yml
version: '3.8'

services:
  postgres-primary:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-primary-data:/var/lib/postgresql/data
    command: postgres -c wal_level=replica -c hot_standby=on
  
  postgres-replica:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-replica-data:/var/lib/postgresql/data
    command: postgres -c hot_standby=on
  
  redis-master:
    image: redis:7
    command: redis-server --appendonly yes
  
  redis-replica:
    image: redis:7
    command: redis-server --appendonly yes --replicaof redis-master 6379
  
  app:
    image: insurance-claims-api:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

## API Versioning Strategy

### URL-Based Versioning

Current structure: `/api/v1/{endpoint}`

**Version Lifecycle:**
1. **v1** (Current): Active support, all new features
2. **v2** (Future): Planning phase
3. **Deprecated versions**: 6-month sunset period

### Version Deprecation Process

```python
# middleware/version_deprecation.py
from fastapi import Request
from datetime import datetime

DEPRECATED_VERSIONS = {
    'v0': {'sunset_date': datetime(2026, 12, 31), 'message': 'v0 will be sunset on Dec 31, 2026'}
}

async def check_api_version(request: Request, call_next):
    """Add deprecation warnings to response headers"""
    response = await call_next(request)
    
    # Extract version from path
    version = request.url.path.split('/')[2]  # /api/v1/...
    
    if version in DEPRECATED_VERSIONS:
        info = DEPRECATED_VERSIONS[version]
        response.headers['X-API-Deprecation'] = 'true'
        response.headers['X-API-Sunset-Date'] = info['sunset_date'].isoformat()
        response.headers['X-API-Deprecation-Info'] = info['message']
    
    return response
```

### Backward Compatibility Rules

1. **Never remove** fields from responses
2. **Never change** field types
3. **Never rename** endpoints
4. **New optional** fields are acceptable
5. **Stricter validation** requires new version

## Monitoring & Observability (Expanded)

### Distributed Tracing with OpenTelemetry

```python
# core/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracer
resource = Resource(attributes={
    SERVICE_NAME: "insurance-claims-api"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Use in code
tracer = trace.get_tracer(__name__)

async def process_claim(claim_id: int):
    with tracer.start_as_current_span("process_claim") as span:
        span.set_attribute("claim.id", claim_id)
        # Process claim
        span.add_event("Claim validation complete")
```

### Custom Metrics

```python
# core/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Business metrics
active_policies = Gauge('active_policies_total', 'Total active policies')
pending_claims = Gauge('pending_claims_total', 'Total pending claims')
premium_collected = Counter('premium_collected_total', 'Total premium collected')

# Database metrics
db_connection_pool_size = Gauge('db_connection_pool_size', 'DB connection pool size')
db_query_duration = Histogram('db_query_duration_seconds', 'DB query duration', ['operation'])
```

### Alerting Rules

**Configuration (alerts.yml):**
```yaml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"
      
      - alert: SlowResponseTime
        expr: http_request_duration_seconds{quantile="0.95"} > 1
        for: 10m
        annotations:
          summary: "Slow API response time"
      
      - alert: DatabaseConnectionPoolExhausted
        expr: db_connection_pool_size > 80
        for: 5m
        annotations:
          summary: "Database connection pool nearly exhausted"
      
      - alert: HighClaimBacklog
        expr: pending_claims_total > 100
        for: 30m
        annotations:
          summary: "High number of pending claims"
```

## Compliance & Data Privacy

### GDPR Compliance

**Right to Access:**
```python
# api/v1/gdpr.py
@router.get("/customers/{customer_id}/data-export")
async def export_customer_data(
    customer_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Export all customer data (GDPR Right to Access)"""
    customer_data = await gdpr_service.export_all_customer_data(customer_id, db)
    
    return {
        "customer": customer_data['customer'],
        "policies": customer_data['policies'],
        "claims": customer_data['claims'],
        "payments": customer_data['payments'],
        "medical_records": customer_data['medical_records'],
        "communications": customer_data['communications']
    }
```

**Right to be Forgotten:**
```python
@router.delete("/customers/{customer_id}/gdpr-delete")
async def delete_customer_gdpr(
    customer_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """Delete customer data (GDPR Right to be Forgotten)"""
    # Anonymize instead of delete (for regulatory requirements)
    await gdpr_service.anonymize_customer_data(customer_id, db)
    
    return {"message": "Customer data anonymized successfully"}
```

### Data Retention Policies

```python
# tasks/data_retention_tasks.py
@celery_app.task
def apply_retention_policies():
    """Apply data retention policies"""
    # Archive old claims (>7 years)
    archive_old_claims()
    
    # Delete temporary files (>30 days)
    delete_temp_files()
    
    # Anonymize old audit logs (>3 years)
    anonymize_old_audit_logs()
    
    # Delete expired quotes (>90 days)
    delete_expired_quotes()
```

### Audit Trail

```python
# models/audit_log.py
class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(50))  # CREATE, UPDATE, DELETE, VIEW
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    old_data = Column(JSONB, nullable=True)
    new_data = Column(JSONB, nullable=True)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
```

## Development Workflow

### Local Development Setup

```bash
# 1. Clone repository
git clone https://github.com/yourorg/insurance-claims-service.git
cd insurance-claims-service

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your local configuration

# 5. Start services with Docker Compose
docker-compose up -d postgres redis

# 6. Run database migrations
alembic upgrade head

# 7. Seed test data (optional)
python scripts/seed_data.py

# 8. Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 9. Access Swagger documentation
# http://localhost:8000/docs
```

### Git Branching Strategy (GitFlow)

```
main (production)
  ├── develop (integration)
  │   ├── feature/add-policy-endpoints
  │   ├── feature/implement-payments
  │   ├── bugfix/fix-claim-validation
  │   └── release/v1.1.0
  └── hotfix/critical-security-patch
```

**Branch Naming Conventions:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `release/` - Release preparation
- `docs/` - Documentation updates

### Code Review Process

**Pull Request Template:**
```markdown
## Description
[Describe the changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Dependent changes merged
```

### CI/CD Pipeline

```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          flake8 app tests
          black --check app tests
          mypy app
      
      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t insurance-claims-api:latest .
      
      - name: Push to registry
        run: |
          docker push insurance-claims-api:latest
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to production
        run: |
          # Deploy using your preferred method
          kubectl apply -f k8s/
```

## Conclusion

This comprehensive design provides a production-ready, scalable, and maintainable backend service for the insurance claims system. The design includes:

✅ **Complete API Coverage**: All 20+ entities with full CRUD operations  
✅ **Modern Technology Stack**: FastAPI, PostgreSQL, SQLAlchemy 2.0, Redis, Celery  
✅ **High Performance**: Async/await, connection pooling, caching, indexing strategies  
✅ **Enterprise Security**: JWT auth, RBAC, encryption, audit logging, GDPR compliance  
✅ **Scalability**: Horizontal scaling, database partitioning, load balancing  
✅ **Observability**: Distributed tracing, metrics, logging, alerting  
✅ **Business Logic**: Premium calculation, risk scoring, commission rules, claim workflows  
✅ **Integrations**: Payment gateways, email/SMS, document signing, file storage  
✅ **Disaster Recovery**: Automated backups, PITR, HA setup, 4-hour RTO  
✅ **Developer Experience**: Code examples, local setup, CI/CD, git workflow  

The architecture follows software engineering best practices with clear separation of concerns, comprehensive error handling, and extensive documentation. The system is designed to handle high loads while maintaining code quality and security standards.

**Swagger documentation** is automatically generated at `/docs`, providing interactive API testing and comprehensive endpoint documentation as required.

---

**Next Steps:**
1. Set up project structure
2. Configure PostgreSQL database with indexes and partitions
3. Implement all 20 models with relationships
4. Create Pydantic schemas for validation
5. Build CRUD base classes and entity-specific operations
6. Implement JWT authentication and RBAC
7. Develop API endpoints for all entities
8. Add business logic services (premium calculation, risk scoring, etc.)
9. Integrate third-party services (payments, email, SMS, storage)
10. Write comprehensive tests (unit, integration, load)
11. Set up monitoring and logging
12. Configure CI/CD pipeline
13. Deploy to staging for testing
14. Conduct security audit and penetration testing
15. Deploy to production with zero-downtime strategy
