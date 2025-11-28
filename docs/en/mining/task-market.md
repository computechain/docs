# Task Market

Marketplace for tasks to be executed on GPU workers.

## Status

**Current Version:** 🚧 In development (Stage 5)

**Planned Features:**
- API for publishing tasks
- Task payment via CPC
- Task distribution among workers
- Worker payouts for execution

*Task Market is an off-chain component that will reuse existing on-chain features described in [Mining Overview](overview.md) (`SUBMIT_RESULT`, `compute_root`). All hex strings in examples are shown without the `0x` prefix for consistency with L1 payloads.*

## Concept

### Roles

1. **Customer (User):**
   - Creates task via API
   - Pays CPC for execution
   - Receives results

2. **Worker:**
   - Receives tasks from PoC validator
   - Executes computations on GPU
   - Submits results
   - Receives rewards

3. **PoC Validator (Orchestrator):**
   - Receives tasks from market
   - Splits into jobs
   - Distributes to workers
   - Verifies results
   - Pays rewards

## API (Planned)

### Create Task

**Endpoint:** `POST /tasks`

**Request:**

```json
{
  "challenge_type": "inference",
  "payload": {
    "model_id": "gpt-3.5-turbo",
    "prompt": "Hello, world!",
    "max_tokens": 100
  },
  "reward": "10.0",
  "deadline": 1700000000
}
```

**Response:**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": 1699999999
}
```

### Get Task Status

**Endpoint:** `GET /tasks/{task_id}`

**Response:**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": {
    "result_hash": "1234abcd5678ef90",
    "worker_address": "cpc1worker...",
    "completed_at": 1700000100
  }
}
```

### List Tasks

**Endpoint:** `GET /tasks`

**Query Parameters:**
- `status`: `pending`, `in_progress`, `completed`, `failed`
- `challenge_type`: Task type
- `limit`: Number of results
- `offset`: Offset

**Response:**

```json
{
  "tasks": [
    {
      "task_id": "...",
      "challenge_type": "inference",
      "status": "pending",
      "reward": "10.0"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

## Task Types

### Inference (Model Inference)

**Type:** `challenge_type: "inference"`

**Payload:**

```json
{
  "model_id": "gpt-3.5-turbo",
  "prompt": "Generate a story",
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Usage:**
- Text generation
- Image classification
- Text translation

### Training (Model Training)

**Type:** `challenge_type: "training"`

**Payload:**

```json
{
  "model_architecture": "resnet50",
  "dataset_url": "https://...",
  "epochs": 10,
  "batch_size": 32
}
```

**Usage:**
- Fine-tuning models
- Training from scratch
- Transfer learning

### Rendering

**Type:** `challenge_type: "rendering"`

**Payload:**

```json
{
  "scene_file": "https://...",
  "resolution": "1920x1080",
  "frames": 100
}
```

**Usage:**
- 3D rendering
- Animation
- Visualization

### Synthetic

**Type:** `challenge_type: "synthetic"`

**Payload:**

```json
{
  "seed": "1234abcd5678ef90",
  "matrix_size": 1024,
  "iterations": 100
}
```

**Usage:**
- GPU stress test
- Benchmarks
- Network testing

## Finance

### Task Payment

**Current Implementation (MVP):**

- Work "on credit" or manual market wallet funding
- Worker payouts via regular `TRANSFER` (batching)

**Future Implementation:**

- L1 deposits via special transaction
- Automatic worker payouts
- Escrow for execution guarantee

### Payment Distribution

**Planned:**

```
Task Payment: 100 CPC

60 CPC (60%) → BURNED (deflation)
25 CPC (25%) → Worker (executor)
10 CPC (10%) → Validators (verifiers)
5 CPC (5%)   → Treasury
```

## L1 Integration

### SUBMIT_RESULT Transactions

**Current Implementation:**

- Worker or PoC validator sends `SUBMIT_RESULT` to L1
- Transaction included in block
- `compute_root` updated

**Future Implementation:**

- Automatic sending from PoC validator
- Result batching for gas savings
- ZK-proofs for verification

## Usage Examples

### Example 1: Publish Task via API

```python
import requests

# Create task
response = requests.post("http://task-market:8080/tasks", json={
    "challenge_type": "inference",
    "payload": {
        "model_id": "gpt-3.5-turbo",
        "prompt": "Hello, world!",
        "max_tokens": 100
    },
    "reward": "10.0"
})

task_id = response.json()["task_id"]
print(f"Task created: {task_id}")

# Check status
status = requests.get(f"http://task-market:8080/tasks/{task_id}")
print(status.json())
```

### Example 2: Worker Receiving Tasks

```python
# Worker connects to PoC validator
# Receives tasks via WebSocket
# Executes and submits results
```

## Roadmap

### Phase 1 (Current)

- ✅ Basic `ComputeResult` structure
- ✅ `SUBMIT_RESULT` transaction
- ✅ `compute_root` in block headers

### Phase 2 (Next)

- 🚧 Task Market API
- 🚧 PoC validator (orchestrator)
- 🚧 WebSocket protocol for workers

### Phase 3 (Future)

- ⏳ ZK-proofs for verification
- ⏳ Automatic payouts
- ⏳ Worker reputation

## Next Steps

- **[Mining Overview](overview.md)** — Mining overview
- **[Local Worker](local-worker.md)** — Running local worker
- **[PoC Details](../understand/poc.md)** — Proof-of-Compute details
