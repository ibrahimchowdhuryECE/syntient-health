# Python SDK

This directory will contain OpenAPI-generated Python client libraries for the chatbot platform services.

## Services

- **Orchestrator Client** - Client for the main orchestrator service
- **DM Client** - Client for the Diagnosis Model service
- **MAM Client** - Client for the Medical Assistant Model service
- **CMM Client** - Client for the Clash/Booking Model service
- **Retrieval Client** - Client for the Retrieval service

## Generation

Client libraries will be generated using OpenAPI Generator from the specifications in `../contracts/openapi/`.

### Example Generation Command

```bash
# Generate orchestrator client
openapi-generator-cli generate \
  -i ../contracts/openapi/orchestrator.yaml \
  -g python \
  -o orchestrator-client \
  --additional-properties=packageName=chatbot_orchestrator_client

# Generate DM client
openapi-generator-cli generate \
  -i ../contracts/openapi/dm.yaml \
  -g python \
  -o dm-client \
  --additional-properties=packageName=chatbot_dm_client

# Generate MAM client
openapi-generator-cli generate \
  -i ../contracts/openapi/mam.yaml \
  -g python \
  -o mam-client \
  --additional-properties=packageName=chatbot_mam_client

# Generate CMM client
openapi-generator-cli generate \
  -i ../contracts/openapi/cmm.yaml \
  -g python \
  -o cmm-client \
  --additional-properties=packageName=chatbot_cmm_client

# Generate Retrieval client
openapi-generator-cli generate \
  -i ../contracts/openapi/retrieval.yaml \
  -g python \
  -o retrieval-client \
  --additional-properties=packageName=chatbot_retrieval_client
```

## Usage

Once generated, clients can be used in Python applications:

```python
# Example usage (to be implemented)
from chatbot_orchestrator_client import OrchestratorApi
from chatbot_orchestrator_client.models import TurnRequest

# Initialize client
orchestrator_client = OrchestratorApi()
orchestrator_client.api_client.configuration.host = "http://localhost:8080"

# Create request
request = TurnRequest(
    conversation_id="conv_123",
    turn_id="turn_456",
    payload={
        "patient_id": "patient_789",
        "presenting_complaint": "chest pain",
        "fields": {"age": 45, "gender": "M"},
        "free_text": "Chest pain started 2 hours ago"
    }
)

# Make API call
response = orchestrator_client.process_turn(request)
print(f"Route: {response.route}")
```

## Dependencies

- OpenAPI Generator CLI
- Python 3.11+
- requests
- urllib3
- pydantic (for data validation)
