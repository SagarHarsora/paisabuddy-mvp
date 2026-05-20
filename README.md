# PaisaBuddy — Monthly Financial Clarity for Salaried Indians

A full-stack fintech PWA that helps salaried Indians understand their monthly spending patterns through AI-powered bank statement analysis.

## Features

- **PDF Bank Statement Parser** — Extracts transactions from HDFC, SBI, and Union Bank statements
- **Smart Categorization** — Automatically categorizes spending into food, transport, shopping, etc.
- **Paisa Score** — 0-100 financial health score based on savings rate, spending patterns, and EMI management
- **Monthly Reports** — AI-generated insights and personalized financial narratives
- **Mobile-First PWA** — Works on Android phones, offline-capable
- **Sentry Monitoring** — Production-grade error tracking and monitoring
- **Structured Logging** — All events logged with PII masking

## Tech Stack

### Backend
- **FastAPI** — Async Python web framework
- **PostgreSQL** — Relational database
- **SQLAlchemy** — ORM
- **pdfplumber** — PDF extraction
- **Redis** — Caching and task queue
- **Sentry** — Error monitoring

### Frontend
- **React 18** — UI library
- **Vite** — Build tool
- **Tailwind CSS** — Styling
- **Zustand** — State management

## Project Structure

```
paisabuddy-mvp/
├── backend/
│   ├── app/
│   │   ├── models/        # Database models
│   │   ├── api/v1/        # API endpoints
│   │   ├── services/      # Parser, score, categorizer
│   │   └── utils/         # Errors, logging, validators
│   ├── tests/             # Unit and integration tests
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/         # React pages
│   │   ├── components/    # React components
│   │   └── store/         # Zustand state
│   └── package.json
└── README.md
```

## Getting Started (Local Development)

### Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run tests
pytest tests/ -v --cov=app

# Run server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## API Endpoints

### Health
- `GET /api/v1/health` — Health check

### Auth (Coming Soon)
- `POST /api/v1/auth/request-otp` — Request OTP
- `POST /api/v1/auth/verify-otp` — Verify OTP and get JWT

### Upload (Coming Soon)
- `POST /api/v1/upload` — Upload bank statement PDF

### Reports (Coming Soon)
- `GET /api/v1/reports` — List user's reports
- `GET /api/v1/reports/{report_id}` — Get specific report

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_health.py -v

# Run only unit tests
pytest tests/ -m unit -v
```

**Coverage requirement:** 80% minimum (enforced in CI/CD)

## Deployment

### Railway (Recommended)

1. Push code to GitHub
2. Connect GitHub repo to Railway
3. Railway automatically detects `railway.toml`
4. Set environment variables
5. Deploy

See `DEPLOYMENT_GUIDE.md` for detailed steps.

## Environment Variables

See `.env.example` for all required environment variables.

Key variables:
- `DATABASE_URL` — PostgreSQL connection
- `REDIS_URL` — Redis connection
- `JWT_SECRET` — Secret key for JWT signing
- `SENTRY_DSN` — Sentry error tracking
- `AWS_*` — S3 bucket credentials (for PDF storage)

## Parser Accuracy Targets

- **HDFC digital statements:** ≥95% accuracy
- **SBI mixed statements:** ≥85% accuracy
- **Union Bank mixed statements:** ≥85% accuracy

Measured against test fixtures with known transactions.

## Security

- ✅ DPDP Act compliant (phone hashing, data deletion)
- ✅ Encryption at rest (PostgreSQL)
- ✅ HTTPS enforced in production
- ✅ JWT authentication
- ✅ Rate limiting (OTP, uploads, reports)
- ✅ PII masking in logs
- ✅ Sentry monitoring (no PII sent)

## Code Quality

- Type hints enforced (mypy)
- Linting (ruff)
- Formatting (black)
- 80%+ test coverage required
- Pre-commit hooks (tests, lint)

## Contributing

1. Create feature branch
2. Write tests first
3. Implement feature
4. Ensure tests pass
5. Submit PR

## License

Proprietary — PaisaBuddy Inc.

## Support

For issues or questions:
- GitHub Issues: [Project Issues](https://github.com/paisabuddy/mvp/issues)
- Email: support@paisabuddy.in

---

**Status:** MVP Phase — Parser & API Complete, Frontend In Progress

**Last Updated:** May 2026
