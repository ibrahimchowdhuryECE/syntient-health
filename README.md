# Hospital Appointment-Triage Chatbot Platform

A microservices-based platform for intelligent hospital appointment scheduling and triage.

## Architecture

The platform consists of five core services:

**NOTE** UPDATE THIS DOCK. WHAT CURSOR DID WAS CREATE KUBERNETES, SDKS...I DONT THINK WE NEED THIS NOW. WE CAN USE DOCKER FOR OUR APP AND JUST RUN IT ON A SITE OR SMT?

- **Orchestrator (ORCH)**: Java Spring Boot service - HTTP REST API, source of truth, routes calls
- **Diagnosis Model (DM)**: Python FastAPI service - triage/urgency evaluation
- **Medical Assistant Model (MAM)**: Python FastAPI service - follow-up questions/messages
- **Clash/Booking Model (CMM)**: Python FastAPI service - appointment scheduling with OR-Tools
- **Retrieval**: Python FastAPI service - RAG (Retrieval-Augmented Generation) placeholder

## Prerequisites

- Docker & Docker Compose
- JDK 21
- Python 3.11
- Make (optional, for convenience commands)

## Quick Start

### Local Development

1. **Start all services:**
   ```bash
   make up
   # or
   docker compose up
   ```

2. **Verify services are running:**
   ```bash
   curl http://localhost:8080/health  # Orchestrator
   curl http://localhost:8001/health  # DM
   curl http://localhost:8002/health  # MAM
   curl http://localhost:8003/health  # CMM
   curl http://localhost:8004/health  # Retrieval
   ```

### Testing Individual Services

**Orchestrator (Main Entry Point):**
```bash
curl -X POST http://localhost:8080/orch/turn \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_123",
    "turn_id": "turn_456",
    "payload": {
      "patient_id": "patient_789",
      "presenting_complaint": "chest pain",
      "fields": {"age": 45, "gender": "M"},
      "free_text": "Chest pain started 2 hours ago"
    }
  }'
```

**Diagnosis Model:**
```bash
curl -X POST http://localhost:8001/dm/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "policy": {"confidence_threshold": 0.7},
    "evidence": {
      "patient_id": "patient_789",
      "presenting_complaint": "chest pain",
      "fields": {"age": 45, "gender": "M"},
      "free_text": "Chest pain started 2 hours ago"
    }
  }'
```

**Medical Assistant Model:**
```bash
curl -X POST http://localhost:8002/mam/ask \
  -H "Content-Type: application/json" \
  -d '{
    "followups": ["duration", "severity"],
    "locale": "en-US"
  }'
```

**Clash/Booking Model:**
```bash
curl -X POST http://localhost:8003/cmm/propose \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient_789",
    "mts_category": "urgent",
    "window": "same_day",
    "constraints": {"preferred_time": "morning"}
  }'
```

**Retrieval Service:**
```bash
curl -X POST http://localhost:8004/kb/search \
  -H "Content-Type: application/json" \
  -d '{
    "pathway": "cardiology",
    "query": "chest pain assessment"
  }'
```

## Development Commands

```bash
# Build all Docker images
make build

# Run unit tests
make test

# Start services
make up

# Stop services
make down

# View logs
make logs
```

## Project Structure

```
chatbot-platform/
├── contracts/          # OpenAPI specifications
├── deploy/            # Docker Compose & K8s manifests
├── services/          # Individual microservices
│   ├── orchestrator/  # Java Spring Boot
│   ├── dm/           # Diagnosis Model (Python)
│   ├── mam/          # Medical Assistant Model (Python)
│   ├── cmm/          # Clash/Booking Model (Python)
│   └── retrieval/    # Retrieval service (Python)
├── sdks/             # Generated client libraries
└── .github/          # CI/CD workflows
```

## API Documentation

Each service exposes OpenAPI documentation at `/docs` when running:

- Orchestrator: http://localhost:8080/docs
- DM: http://localhost:8001/docs
- MAM: http://localhost:8002/docs
- CMM: http://localhost:8003/docs
- Retrieval: http://localhost:8004/docs

## Current Status

⚠️ **STUB IMPLEMENTATION ONLY** ⚠️

This is a scaffold with:
- ✅ Service infrastructure and networking
- ✅ API contracts (OpenAPI specs)
- ✅ Docker containerization
- ✅ Kubernetes manifests
- ✅ CI/CD pipeline structure
- ❌ No business logic implemented
- ❌ No database connections
- ❌ No authentication/authorization
- ❌ No state management

All services return static stub responses for development and testing purposes.

## Contributing

1. Follow the established service boundaries
2. Implement business logic within service boundaries
3. Update OpenAPI contracts when changing interfaces
4. Add tests for new functionality
5. Update this README with new endpoints/examples

## License

[Add your license here]
