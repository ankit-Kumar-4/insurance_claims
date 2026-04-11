# Insurance Claims Backend Service

A high-performance insurance claims management API built with FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- ✅ RESTful API with 20+ entity types
- ✅ Async/await for high concurrency
- ✅ PostgreSQL with advanced indexing
- ✅ JWT authentication with RBAC
- ✅ Redis caching
- ✅ Celery background tasks
- ✅ Swagger documentation at `/docs`
- ✅ File storage (AWS S3)
- ✅ Payment processing (Stripe)
- ✅ Email/SMS notifications

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+ (async)
- **Cache**: Redis 7+
- **Task Queue**: Celery
- **Python**: 3.11+

## Project Structure

```
insurance_claims_service/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── api/v1/          # API endpoints
│   ├── crud/            # CRUD operations
│   ├── services/        # Business logic
│   ├── core/            # Core utilities
│   ├── utils/           # Helper functions
│   ├── tasks/           # Celery tasks
│   ├── enums/           # Enum definitions
│   └── constants/       # Constants
├── tests/               # Test suite
├── scripts/             # Utility scripts
├── alembic/             # Database migrations
└── docker-compose.yml   # Docker setup
```

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd insurance_claims_service
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# At minimum, set a strong SECRET_KEY
nano .env  # or use your preferred editor
```

### 5. Start Services with Docker

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Verify services are running
docker-compose ps

# View logs (optional)
docker-compose logs -f
```

### 6. Initialize Database

```bash
# Run migrations (to be created in Phase 2)
alembic upgrade head

# Seed sample data (optional)
python scripts/seed_data.py
```

### 7. Run Application

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 8. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development Tools

### Start with Debug Tools

```bash
# Start with pgAdmin and Redis Commander
docker-compose --profile debug up -d

# Access tools:
# - pgAdmin: http://localhost:5050
# - Redis Commander: http://localhost:8081
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Code Quality

```bash
# Format code
black app tests

# Sort imports
isort app tests

# Lint code
flake8 app tests

# Type check
mypy app
```

### Load Testing

```bash
# Run Locust
locust -f tests/load/locustfile.py
```

## API Endpoints

### Core Entities (20+)

- `/api/v1/policies` - Policy management
- `/api/v1/claims` - Claim processing
- `/api/v1/customers` - Customer management
- `/api/v1/agents` - Agent management
- `/api/v1/premiums` - Premium tracking
- `/api/v1/payments` - Payment processing
- `/api/v1/documents` - Document management
- `/api/v1/quotes` - Quote generation
- And 12+ more entities...

### System

- `/api/v1/system/health` - Health check
- `/api/v1/system/metrics` - Prometheus metrics
- `/api/v1/audit-logs` - Audit trail

## Environment Variables

See `.env.example` for all available configuration options.

### Required Variables

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<strong-secret-key-min-32-chars>
```

### Optional Variables

- AWS credentials for S3 storage
- Stripe keys for payment processing
- SendGrid/Twilio for notifications
- Sentry DSN for error tracking

## Docker Deployment

### Build Image

```bash
docker build -t insurance-claims-api:latest .
```

### Run with Docker Compose

```bash
# Production setup
docker-compose -f docker-compose.prod.yml up -d
```

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
docker exec -it insurance_postgres psql -U postgres -d insurance_claims

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

### Redis Connection Issues

```bash
# Test Redis connection
docker exec -it insurance_redis redis-cli ping
```

## Performance Targets

- GET operations: < 100ms (p95)
- POST/PUT operations: < 200ms (p95)
- Throughput: 1000 req/sec per instance
- Database queries: < 50ms (p95)

## Security

- HTTPS/TLS 1.3 only in production
- JWT authentication with 30-min expiry
- RBAC with 7 roles
- Rate limiting (100 req/min authenticated)
- Field-level encryption for sensitive data
- GDPR compliance features

## Contributing

1. Create feature branch from `develop`
2. Make changes with tests
3. Run code quality checks
4. Submit pull request

## License

Proprietary - All Rights Reserved

## Support

For issues and questions, please contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: April 2026
