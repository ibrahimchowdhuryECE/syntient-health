# Java SDK

This directory will contain OpenAPI-generated Java client libraries for the chatbot platform services.

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
  -g java \
  -o orchestrator-client \
  --additional-properties=artifactId=chatbot-orchestrator-client

# Generate DM client
openapi-generator-cli generate \
  -i ../contracts/openapi/dm.yaml \
  -g java \
  -o dm-client \
  --additional-properties=artifactId=chatbot-dm-client

# Generate MAM client
openapi-generator-cli generate \
  -i ../contracts/openapi/mam.yaml \
  -g java \
  -o mam-client \
  --additional-properties=artifactId=chatbot-mam-client

# Generate CMM client
openapi-generator-cli generate \
  -i ../contracts/openapi/cmm.yaml \
  -g java \
  -o cmm-client \
  --additional-properties=artifactId=chatbot-cmm-client

# Generate Retrieval client
openapi-generator-cli generate \
  -i ../contracts/openapi/retrieval.yaml \
  -g java \
  -o retrieval-client \
  --additional-properties=artifactId=chatbot-retrieval-client
```

## Usage

Once generated, clients can be used in Java applications:

```java
// Example usage (to be implemented)
OrchestratorApi orchestratorClient = new OrchestratorApi();
orchestratorClient.setBasePath("http://localhost:8080");

TurnRequest request = new TurnRequest();
// ... set request properties

TurnResponse response = orchestratorClient.processTurn(request);
```

## Dependencies

- OpenAPI Generator CLI
- Java 21+
- Maven or Gradle for dependency management
