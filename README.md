# Sentinel Ledger

Cross-chain risk intelligence infrastructure for Base and Ethereum.

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 15+
- Redis 7+
- Neo4j 5+

### Backend Setup

1. **Install Dependencies**
```bash
cd Backend
pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your RPC URLs and database credentials
```

3. **Database Setup**
```bash
# Start PostgreSQL, Redis, Neo4j
docker-compose up -d postgres neo4j redis

# Run migrations
alembic upgrade head
```

4. **Start API Server**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Start Indexer** (in separate terminal)
```bash
python -m indexer.run
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd Frontend
npm install
```

2. **Environment Configuration**
```bash
cp .env.example .env.development
# Edit with your API URL
```

3. **Start Development Server**
```bash
npm run dev
```

## Access Points

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- API: http://localhost:8000/api/v1
- Neo4j Browser: http://localhost:7474

## Architecture

- **Backend**: FastAPI + SQLAlchemy + Neo4j
- **Frontend**: React + Vite + TailwindCSS
- **Database**: PostgreSQL + Neo4j + Redis
- **Blockchain**: Base + Ethereum

## Features

- Real-time token deployment monitoring
- Risk scoring and analysis
- Cross-chain deployer profiling
- Liquidity tracking
- AI-powered explanations

## Development

The system is designed for solo development with modular architecture:
- Indexer services for blockchain data
- Risk engine for scoring
- API layer for frontend
- Graph database for relationships

## License

MIT
