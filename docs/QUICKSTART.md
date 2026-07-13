# Stackly ERP - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.12+
- MySQL 8.0+
- Redis (for caching)
- Git

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/stackly/erp-platform.git
cd Employee_Platform
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env

# Edit .env with your configuration
nano .env

# Minimum required:
ENVIRONMENT=development
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/stackly_erp
SECRET_KEY=your-secret-key-change-in-production
```

### 5. Initialize Database
```bash
# Run migrations
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_data.py
```

### 6. Run Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access Application
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Docker Setup (Recommended)

### Quick Start with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Reset everything
docker-compose down -v
```

### Services Started
- **FastAPI**: http://localhost:8000
- **MySQL**: localhost:3306
- **Redis**: localhost:6379
- **Nginx**: http://localhost:80

---

## Common Commands

### Database Operations
```bash
# Create migration
alembic revision --autogenerate -m "Your migration message"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Check current version
alembic current
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# With coverage report
pytest --cov=. --cov-report=html
```

### Code Quality
```bash
# Format code
black .

# Lint
pylint routers/ services/

# Type checking
mypy .
```

---

## API Usage Examples

### Authentication

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```

#### Use Token
```bash
curl -X GET "http://localhost:8000/api/v1/employees" \
  -H "Authorization: Bearer {access_token}"
```

### Refresh Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "{refresh_token}"
  }'
```

### Get Employees (with pagination)
```bash
curl -X GET "http://localhost:8000/api/v1/employees?page=1&size=20" \
  -H "Authorization: Bearer {access_token}"
```

### Create Employee
```bash
curl -X POST "http://localhost:8000/api/v1/employees" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "department_id": 1,
    "designation_id": 1
  }'
```

---

## Configuration

### Development vs Production

**Development** (default):
- Debug mode enabled
- Database echo enabled
- Reload on file change
- CORS: All origins
- Rate limiting: High
- Logging: DEBUG level

**Production**:
- Debug disabled
- Database optimized
- SSL required
- CORS: Specific origins
- Rate limiting: Strict
- Logging: WARNING level
- Monitoring: Enabled

Switch environment:
```bash
export ENVIRONMENT=production
```

---

## Troubleshooting

### Database Connection Error
```bash
# Check MySQL is running
mysql -u root -p

# Verify DATABASE_URL in .env
# Format: mysql+pymysql://user:password@host:port/database

# Check credentials
mysql -u root -h localhost -p
```

### Redis Connection Error
```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Verify REDIS_URL in .env
# Format: redis://host:port/db
```

### Port Already in Use
```bash
# Use different port
uvicorn main:app --port 8001

# Or kill process using port 8000
lsof -i :8000  # Find PID
kill -9 <PID>
```

### JWT Token Expired
```bash
# Use refresh token to get new access token
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "{refresh_token}"
  }'
```

### Permission Denied Error
```json
{
  "status": "error",
  "code": "PERMISSION_DENIED",
  "message": "User does not have required permission: employee.create"
}
```

**Solution**: 
- Check user has correct role assigned
- Verify role has required permission
- Check user is active (is_active=true)

---

## Project Structure

```
Employee_Platform/
├── core/                    # Core functionality
│   ├── authentication.py    # JWT, MFA, password
│   ├── authorization.py     # RBAC permissions
│   ├── config.py           # Configuration
│   ├── database.py         # Database connection
│   └── ...
├── models/                  # SQLAlchemy models
├── schemas/                 # Pydantic schemas
├── routers/                 # API endpoints
├── services/                # Business logic
├── middlewares/             # Request/response middlewares
├── docs/                    # Documentation
├── tests/                   # Test suite
├── main.py                 # Application entry
├── requirements.txt        # Dependencies
└── README.md              # This file
```

---

## Key Features Implemented

✅ Multi-tenant support with row-level security
✅ JWT authentication with refresh tokens
✅ MFA (TOTP + backup codes)
✅ RBAC with 50+ permissions
✅ Password policy enforcement
✅ 200+ database tables designed
✅ Comprehensive API documentation
✅ Docker containerization
✅ Configuration management
✅ Audit middleware

---

## Next Steps

1. **Explore API Documentation**: Visit http://localhost:8000/docs
2. **Read Full Guide**: See `IMPLEMENTATION_GUIDE.md`
3. **Review Architecture**: See `docs/PHASE_3_4_ARCHITECTURE.md`
4. **Run Tests**: `pytest` to ensure everything works
5. **Try API Calls**: Use curl examples above

---

## Documentation Links

- 📄 [Business Requirements (BRD)](docs/PHASE_1_2_BRD_SRS.md) - 80+ pages
- 🏗️ [Architecture & Design](docs/PHASE_3_4_ARCHITECTURE.md) - 70+ pages
- 🛣️ [Implementation Roadmap](docs/PHASE_5_35_ROADMAP.md) - 50+ pages
- 📖 [Full Implementation Guide](IMPLEMENTATION_GUIDE.md) - 400+ lines
- 🔗 [API Documentation](http://localhost:8000/docs) - Interactive Swagger
- 📊 [Database Schema](docs/database_design.md)

---

## Support

For issues or questions:
1. Check `IMPLEMENTATION_GUIDE.md`
2. Review `docs/` directory
3. Check inline code comments
4. Raise GitHub issue

---

**Version**: 1.0.0  
**Last Updated**: 2026-07-08  
**Environment**: Development  
**Status**: Active (Phases 1-9 Complete)

Happy Coding! 🚀
