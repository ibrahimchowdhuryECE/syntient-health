.PHONY: help build test up down logs clean

# Default target
help:
	@echo "Available commands:"
	@echo "  build    - Build all Docker images"
	@echo "  test     - Run unit tests for all services"
	@echo "  up       - Start all services with docker-compose"
	@echo "  down     - Stop all services"
	@echo "  logs     - View logs from all services"
	@echo "  clean    - Clean up Docker images and containers"

# Build all Docker images
build:
	@echo "Building all Docker images..."
	docker build -t chatbot-orchestrator:latest services/orchestrator/
	docker build -t chatbot-dm:latest services/dm/
	docker build -t chatbot-mam:latest services/mam/
	docker build -t chatbot-cmm:latest services/cmm/
	docker build -t chatbot-retrieval:latest services/retrieval/
	@echo "All images built successfully!"

# Run unit tests
test:
	@echo "Running tests for Orchestrator..."
	cd services/orchestrator && ./gradlew test
	@echo "Running tests for Python services..."
	cd services/dm && python -m pytest tests/ -v
	cd services/mam && python -m pytest tests/ -v
	cd services/cmm && python -m pytest tests/ -v
	cd services/retrieval && python -m pytest tests/ -v
	@echo "All tests completed!"

# Start services
up:
	@echo "Starting all services..."
	docker compose up -d
	@echo "Services started! Check health endpoints:"
	@echo "  Orchestrator: http://localhost:8080/health"
	@echo "  DM: http://localhost:8001/health"
	@echo "  MAM: http://localhost:8002/health"
	@echo "  CMM: http://localhost:8003/health"
	@echo "  Retrieval: http://localhost:8004/health"

# Stop services
down:
	@echo "Stopping all services..."
	docker compose down
	@echo "Services stopped!"

# View logs
logs:
	docker compose logs -f

# Clean up
clean:
	@echo "Cleaning up Docker resources..."
	docker compose down -v
	docker rmi chatbot-orchestrator:latest chatbot-dm:latest chatbot-mam:latest chatbot-cmm:latest chatbot-retrieval:latest 2>/dev/null || true
	@echo "Cleanup completed!"

# Health check
health:
	@echo "Checking service health..."
	@curl -s http://localhost:8080/health || echo "Orchestrator: DOWN"
	@curl -s http://localhost:8001/health || echo "DM: DOWN"
	@curl -s http://localhost:8002/health || echo "MAM: DOWN"
	@curl -s http://localhost:8003/health || echo "CMM: DOWN"
	@curl -s http://localhost:8004/health || echo "Retrieval: DOWN"
