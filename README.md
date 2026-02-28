# Sentinel Ledger

Cross-chain risk intelligence infrastructure for Base and Ethereum.

## 🎯 Overview

Sentinel Ledger is a production-grade risk intelligence platform that monitors blockchain deployments, analyzes token behavior, and provides actionable risk insights. Built for solo founders and scaling teams, it combines real-time indexing, behavioral analysis, and AI-powered explanations to deliver institutional-grade blockchain intelligence.

### Core Capabilities

- **Real-time Token Monitoring**: Track new ERC20 deployments across Base and Ethereum
- **Multi-Dimensional Risk Scoring**: Contract, liquidity, ownership, and deployer risk analysis
- **Cross-Chain Intelligence**: Correlate behavior patterns across multiple networks
- **Liquidity Surveillance**: Monitor pool creation, locking, and removal events
- **Behavioral Profiling**: Build comprehensive deployer reputation models
- **AI-Powered Explanations**: Generate human-readable risk narratives
- **Graph-Based Analysis**: Discover relationships and patterns through Neo4j

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │     API         │    │   Indexer       │
│   (React)       │◄──►│   (FastAPI)    │◄──►│   (Python)      │
│   Port: 3000   │    │   Port: 8000   │    │   Background    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Data Layer    │
                       │ PostgreSQL      │
                       │ Neo4j          │
                       │ Redis           │
                       └─────────────────┘
```

### Technology Stack

**Backend**
- **Framework**: FastAPI + SQLAlchemy
- **Blockchain**: Web3.py (Base + Ethereum)
- **Databases**: PostgreSQL + Neo4j + Redis
- **AI**: OpenRouter integration
- **Task Queue**: Celery

**Frontend**
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS
- **State Management**: React Query
- **Charts**: Recharts
- **Routing**: React Router

**Infrastructure**
- **Containerization**: Docker + Docker Compose
- **Migrations**: Alembic
- **Monitoring**: Structured logging
- **Development**: Hot reload + auto-restart

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- Git

### One-Command Setup

```bash
# Clone and setup
git clone <repository-url>
cd sentinel-ledger
./setup.sh

# Start services
cd Backend && ./start.sh &
cd Frontend && ./start.sh
```

### Manual Setup

#### Backend Configuration

1. **Install Dependencies**
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Setup**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```bash
# RPC Endpoints
BASE_RPC_URL=https://mainnet.base.org
ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Database
POSTGRES_USER=sentinel_user
POSTGRES_PASSWORD=strong_password
NEO4J_PASSWORD=strong_password

# Optional AI
OPENROUTER_API_KEY=your_key_here
```

3. **Start Services**
```bash
# Start databases
docker-compose up -d postgres neo4j redis

# Run migrations
alembic upgrade head

# Start API server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Start indexer (separate terminal)
python -m indexer.run
```

#### Frontend Configuration

1. **Install Dependencies**
```bash
cd Frontend
npm install
```

2. **Environment Setup**
```bash
cp .env.example .env.development
# Edit with your API URL
```

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

3. **Start Development Server**
```bash
npm run dev
```

## 📊 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main application dashboard |
| API Documentation | http://localhost:8000/docs | Interactive API docs |
| API Base | http://localhost:8000/api/v1 | REST API endpoints |
| Health Check | http://localhost:8000/health | Service status |
| Neo4j Browser | http://localhost:7474 | Graph database interface |

## 🔍 Risk Intelligence Model

Sentinel Ledger employs a multi-factor risk scoring system:

### Risk Categories

1. **Contract Risk (35%)**
   - Mint function accessibility
   - Blacklist capabilities
   - Ownership renouncement status
   - Proxy/upgradeability patterns
   - Pause mechanisms

2. **Liquidity Risk (30%)**
   - Initial liquidity depth
   - LP token locking status
   - Early liquidity removal patterns
   - Pool distribution analysis

3. **Ownership Risk (20%)**
   - Deployer token holdings
   - Centralization metrics
   - Control mechanism analysis

4. **Deployer Risk (15%)**
   - Historical deployment patterns
   - Cross-chain behavior correlation
   - Wallet age and funding sources
   - Previous rug indicators

### Risk Levels

- **LOW** (0-30): Minimal risk indicators
- **MEDIUM** (31-60): Moderate concerns present
- **HIGH** (61-80): Significant risk factors
- **CRITICAL** (81-100): Extreme risk, likely malicious

## 🛠 Development

### Project Structure

```
sentinel-ledger/
├── Backend/                 # Python API services
│   ├── api/                # FastAPI routes
│   ├── indexer/            # Blockchain data collection
│   ├── intelligence/       # Analysis engines
│   ├── risk/              # Scoring algorithms
│   ├── db/                # Database models
│   └── config/            # Configuration
├── Frontend/               # React application
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   └── utils/        # Utilities
└── docker-compose.yml     # Infrastructure
```

### Adding New Features

1. **Backend**: Add routes in `api/routes/`, implement logic in appropriate modules
2. **Frontend**: Create components in `src/components/`, pages in `src/pages/`
3. **Database**: Modify models in `db/models.py`, run migrations with Alembic

### Testing

```bash
# Backend API tests
cd Backend
python test_api.py

# Frontend component tests
cd Frontend
npm run test
```

## 🔧 Configuration

### Risk Scoring Weights

Adjust risk model weights in `.env`:

```bash
CONTRACT_RISK_WEIGHT=0.35
LIQUIDITY_RISK_WEIGHT=0.30
OWNERSHIP_RISK_WEIGHT=0.20
DEPLOYER_RISK_WEIGHT=0.15
```

### Processing Parameters

```bash
BATCH_INTERVAL_SECONDS=120    # Analysis frequency
MAX_BLOCK_BATCH=100         # Blocks processed per batch
```

## 📈 Monitoring & Logging

- **API Logs**: `Backend/logs/api.log`
- **Indexer Logs**: `Backend/logs/indexer.log`
- **Database Queries**: SQLAlchemy logging enabled in debug mode
- **Health Monitoring**: `/health` endpoint for uptime checks

## 🚀 Production Deployment

### Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# Scale services as needed
docker-compose up -d --scale api=3 --scale indexer=2
```

### Environment Considerations

- Use environment-specific `.env` files
- Enable HTTPS with reverse proxy (nginx/caddy)
- Configure database backups
- Set up monitoring and alerting
- Use managed database services for scale

## 🔐 Security

- No private keys stored in application
- Read-only blockchain access
- Rate limiting on API endpoints
- CORS properly configured
- Environment variable encryption recommended
- Database connection encryption

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

### Code Standards

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use ESLint + Prettier configuration
- **Commits**: Conventional commit messages
- **Tests**: Write tests for new features

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Documentation**: This README and inline code comments
- **API Documentation**: `/docs` endpoint
- **Issues**: GitHub Issues for bug reports
- **Community**: [Discord/Telegram links if applicable]

## 🎯 Roadmap

### v0.2 - Enhanced Intelligence
- Machine learning anomaly detection
- Cross-bridge analysis
- Advanced graph clustering
- Real-time alert system

### v0.3 - Enterprise Features
- Multi-tenant support
- Advanced analytics dashboard
- Custom risk models
- API rate limiting tiers

### v1.0 - Production Infrastructure
- Horizontal scaling
- Geographic distribution
- Advanced monitoring
- SLA guarantees

---

Built with ❤️ for the decentralized ecosystem. Sentinel Ledger provides the intelligence layer needed for safe blockchain interaction.
