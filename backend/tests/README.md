# Backend Tests

## Test Structure

```
tests/
├── conftest.py                          # Shared fixtures
├── unit/                                # Unit tests (no external dependencies)
│   └── domains/
│       └── user/
│           ├── test_user_model.py       # Domain model tests
│           └── test_user_app_service.py # Application service tests
└── api/                                 # Integration/API tests
    ├── infra/
    │   └── test_user_repository_integration.py
    └── domains/
        └── user/
            └── test_user_router.py      # Full HTTP endpoint tests
```

## Running Tests

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run all tests
```bash
pytest
```

### Run unit tests only
```bash
pytest tests/unit/
```

### Run integration tests (requires Docker)
```bash
pytest tests/api/
```

### Run specific test file
```bash
pytest tests/unit/domains/user/test_user_model.py -v
```

### Run with coverage
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

## Test Categories

### Unit Tests
- **Domain Model** (`test_user_model.py`): Business logic validation
  - User factory method
  - Field validation (username, email)
  - Change methods (change_full_name)
  - Serialization (to_dict)

- **Application Service** (`test_user_app_service.py`): Use case orchestration
  - Create user (with duplicates, invalid data)
  - Update user (not found, validation)
  - Delete user
  - Get user / List users with pagination

### Integration Tests
- **Repository** (`test_user_repository_integration.py`): Database operations with Testcontainers
  - CRUD operations
  - Uniqueness constraints
  - Pagination
  - Existence checks

- **API Router** (`test_user_router.py`): Full HTTP stack with real database
  - POST /api/users
  - GET /api/users/{id}
  - GET /api/users (pagination)
  - PATCH /api/users/{id}
  - DELETE /api/users/{id}

## Test Coverage Goals

- **Target**: 70%+ coverage
- **Critical paths**: All business logic and use cases
- **Integration**: All repository methods and API endpoints

## Notes

- Integration tests use Testcontainers for isolated PostgreSQL instances
- Each test has isolated database state via `clean_db` fixture
- Async tests use pytest-asyncio
- FastAPI TestClient for HTTP endpoint testing
