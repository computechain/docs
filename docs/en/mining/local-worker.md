# Local GPU Worker

Guide for running local worker to execute synthetic tasks.

## Implementation Status

**Current Version:** MVP (Stage 4 – L1 support is ready)

Current on-chain capabilities:
- `TxType.SUBMIT_RESULT`
- `ComputeResult` validation on L1
- `compute_root` commitment inside block headers

Off-chain worker status:
- Local GPU worker script — **planned**, not implemented yet
- Synthetic task generator — design outlined below

**Future Version (Stage 5):**
- Real GPU computations (CUDA/ROCm)
- Connection to PoC validator
- Execution of real tasks from marketplace

## Requirements

### Hardware

- **GPU (optional for MVP):** RTX 4090/5090 or similar
- **CPU:** Sufficient for mock computations
- **RAM:** Minimum 4 GB

### Software

- **Python 3.12+**
- **ComputeChain CLI** (`cpc-cli`)
- **Access to L1 node** (local or remote)

## Quick Start

### Step 1: Create Worker Key

```bash
./cpc-cli keys add worker
```

**Output:**

```
Key 'worker' created.
Address: cpc1worker...
Pubkey:  02a1b2c3...
```

### Step 2: Fund Account

```bash
WORKER_ADDR=$(./cpc-cli keys show worker | grep address | awk '{print $2}' | tr -d '",')
./cpc-cli tx send $WORKER_ADDR 100 --from faucet --node http://localhost:8000
```

**Important:** Balance must cover fees for `SUBMIT_RESULT` transactions (80,000 gas * gas_price).

### Step 3: Planned Worker Script (MVP)

**Current Implementation:** Worker script is **not yet implemented**. The pseudocode below illustrates the intended flow:

```python
# scripts/gpu_worker.py (planned)

import time
import uuid
from computechain.cli.keystore import KeyStore
from computechain.protocol.types.tx import Transaction, TxType
from computechain.protocol.types.poc import ComputeResult
from computechain.protocol.crypto.hash import sha256

def generate_synthetic_task(block_hash: str, worker_address: str):
    """Generate synthetic task from block hash"""
    seed = sha256((block_hash + worker_address).encode()).hex()
    return {
        "task_id": str(uuid.uuid4()),
        "challenge_type": "synthetic",
        "seed": seed,
        "matrix_size": 1024
    }

def execute_task(task):
    """Execute task (mock for MVP)"""
    # Future: real GPU computations
    # result = cuda_matrix_mul(task["seed"], task["matrix_size"])
    result = f"mock_result_{task['seed']}"
    result_hash = sha256(result.encode()).hex()
    return result_hash

def submit_result(worker_key, task_id, result_hash, node_url):
    """Submit result to L1"""
    # TODO: reuse `cpc-cli tx submit-result` logic or build Transaction directly
    # ... (payload follows ComputeResult schema)
    pass

def main():
    """Main worker loop"""
    ks = KeyStore()
    worker_key = ks.get_key("worker")
    worker_address = worker_key['address']
    node_url = "http://localhost:8000"
    
    while True:
        # Get latest block
        # block_hash = get_latest_block_hash(node_url)
        
        # Generate task
        # task = generate_synthetic_task(block_hash, worker_address)
        
        # Execute task
        # result_hash = execute_task(task)
        
        # Submit result
        # submit_result(worker_key, task["task_id"], result_hash, node_url)
        
        # Wait for next block
        time.sleep(10)  # Block time

if __name__ == "__main__":
    main()
```

## Using CLI to Submit Results

### Manual Submission (Current Method)

```bash
./cpc-cli tx submit-result \
  --task-id "550e8400-e29b-41d4-a716-446655440000" \
  --result-hash "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd" \
  --from worker \
  --node http://localhost:8000
```

**Parameters:**

- `--task-id`: Task UUID
- `--result-hash`: Computation result hash
- `--from`: Worker key name in keystore
- `--node`: L1 node URL

## Future Implementation (Stage 5)

### Connection to PoC Validator

**WebSocket Protocol:**

```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    if data["type"] == "job":
        # Task received
        job_id = data["job_id"]
        task_id = data["task_id"]
        payload = data["payload"]
        
        # Execute task
        result_hash = execute_job(payload)
        
        # Send result
        response = {
            "type": "job_result",
            "job_id": job_id,
            "worker_address": worker_address,
            "result_hash": result_hash,
            "proof": None
        }
        ws.send(json.dumps(response))

ws = websocket.WebSocketApp("ws://poc-validator:8080/worker",
                            on_message=on_message)
ws.run_forever()
```

### Real GPU Computations

**Example with CUDA:**

```python
import cupy as cp

def cuda_matrix_multiplication(seed: bytes, size: int):
    """Matrix multiplication on GPU"""
    # Generate matrices from seed
    cp.random.seed(int.from_bytes(seed[:4], 'big'))
    A = cp.random.rand(size, size)
    B = cp.random.rand(size, size)
    
    # Multiply on GPU
    C = cp.dot(A, B)
    
    # Return result hash
    result_bytes = C.tobytes()
    return sha256(result_bytes).hex()
```

## Monitoring

### Check Worker Transactions

```bash
# Get block with SUBMIT_RESULT transaction
./cpc-cli query block <HEIGHT> --node http://localhost:8000 | jq '.txs[] | select(.tx_type == "SUBMIT_RESULT")'
```

### Check compute_root

```bash
# Get block header
./cpc-cli query block <HEIGHT> --node http://localhost:8000 | jq '.header.compute_root'
```

## Troubleshooting

### Error: Insufficient balance

**Cause:** Insufficient balance to pay fee

**Solution:**

```bash
# Fund account
./cpc-cli tx send <WORKER_ADDR> 10 --from faucet --node http://localhost:8000
```
*10 CPC is enough to cover many SUBMIT_RESULT transactions on devnet (fee ≈ 0.00008 CPC each).*

### Error: Invalid ComputeResult

**Cause:** Invalid payload format

**Solution:** Ensure:
- `task_id` is valid UUID
- `result_hash` is hex string
- `worker_address` matches `tx.from_address`

### Error: Connection refused

**Cause:** L1 node not running or unavailable

**Solution:**

```bash
# Check node status
curl http://localhost:8000/status
```

## Next Steps

- **[Mining Overview](overview.md)** — Mining overview
- **[Task Market](task-market.md)** — Publishing tasks
- **[PoC Details](../understand/poc.md)** — Proof-of-Compute details
