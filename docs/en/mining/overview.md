# GPU Workers / Mining — Overview

GPU Workers (miners) execute useful computations on GPU and receive rewards for correct task execution.

## Concept

**Proof-of-Compute** replaces meaningless hash rate with useful computations:

- Instead of searching for nonce, workers execute real tasks
- Results are verified and recorded in blockchain
- Workers receive rewards for correct execution

## Worker Role

### Main Functions

1. **Connection to PoC Validator:**
   - WebSocket or HTTP connection
   - Receiving tasks for execution

2. **Computation Execution:**
   - Running CUDA/ROCm kernels on GPU
   - Processing tasks (matrix multiplication, inference, training, etc.)

3. **Result Submission:**
   - Hashing the result
   - Forming proof (future: ZK-proof)
   - Sending `SUBMIT_RESULT` transaction to L1

4. **Reward Receipt:**
   - Off-chain (via PoC validator) or
   - On-chain (via L1 reward mechanism)

## ComputeResult Structure

### Fields

```python
class ComputeResult:
    task_id: str  # Task UUID
    worker_address: str  # Worker address (cpc1...)
    result_hash: str  # Computation result hash
    proof: Optional[str] = None  # Correctness proof (future: ZK-proof)
    nonce: Optional[int] = None  # For synthetic tasks
    signature: Optional[str] = None  # Worker signature
```

### Example Payload

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "worker_address": "cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
  "result_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
  "proof": null,
  "nonce": 12345,
  "signature": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678"
}
```

## SUBMIT_RESULT Transaction

### Transaction Type

**`TxType.SUBMIT_RESULT`**

**Gas Cost:** 80,000 gas

### Transaction Structure

```python
Transaction(
    tx_type=TxType.SUBMIT_RESULT,
    from_address="cpc1worker...",  # Worker address
    to_address=None,
    amount=0,  # Reward not yet integrated in L1
    fee=gas_limit * gas_price,
    nonce=...,
    gas_price=1000,
    gas_limit=80000,
    payload={
        "task_id": "...",
        "worker_address": "cpc1worker...",
        "result_hash": "...",
        "proof": None,
        "nonce": 12345,
        "signature": "..."
    }
)
```

### Validation

**L1 checks:**

1. `ComputeResult` structure is valid
2. `worker_address` matches `tx.from_address`
3. Proof is verified (future: via ZK-verification)
4. `signature` inside `ComputeResult` is currently informational (only `tx.signature` is verified in MVP)

## Blockchain Integration

### compute_root

**In block header:**

```python
class BlockHeader:
    compute_root: str  # Merkle root of all ComputeResult in block
```

**Calculation:**

```python
def compute_poc_root(txs: List[Transaction]) -> str:
    leaves = []
    for tx in txs:
        if tx.tx_type == TxType.SUBMIT_RESULT:
            res = ComputeResult(**tx.payload)
            data = res.model_dump_json().encode("utf-8")
            leaves.append(sha256(data))
    
    if not leaves:
        return ""
    
    # Implementation uses AccountState helper: state._compute_merkle_root_from_leaves(leaves).hex()
    return compute_merkle_root(leaves).hex()
```

## Task Types

### Synthetic Tasks

**Status:** ✅ Implemented on L1 (Stage 4). Off-chain worker is planned in Local Worker guide.

**Purpose:** GPU stress test and benchmark

**Type:** `challenge_type: "synthetic"`

**Properties:**
- Deterministic output
- Fast verification
- Generated from block hash

**Example:**

```python
# Generate task from block hash
block_hash = get_latest_block_hash()
seed = sha256(block_hash + worker_address)
matrix_size = 1024

# Execution
result = matrix_multiplication(seed, matrix_size)
result_hash = sha256(result)
```

### Real Tasks (Future)

**Status:** 🚧 In development (Stage 5)

**Types:**
- `inference` — ML model inference
- `training` — Model training
- `rendering` — Graphics rendering
- `simulation` — Scientific simulations

**Properties:**
- Loaded via Task Market
- Paid by user
- Verified via ZK-proofs or duplicate execution

## Task Execution Workflow

### Current Implementation (Stage 4)

**Simplified flow:**

1. Worker generates task from block hash (synthetic)
2. Worker executes computation (CPU/GPU mock)
3. Worker sends `SUBMIT_RESULT` transaction to L1
4. L1 validator verifies structure and includes in block
5. `compute_root` is updated in block header

### Future Implementation (Stage 5)

**Full flow with marketplace:**

1. User creates task via Task Market API
2. PoC validator receives task and splits into jobs
3. PoC validator distributes jobs to workers via WebSocket
4. Worker executes task on GPU
5. Worker sends result with proof back
6. PoC validator verifies result (selective verification)
7. PoC validator or Worker sends `SUBMIT_RESULT` to L1
8. L1 validator includes transaction in block
9. Worker receives reward (off-chain or via L1 reward)

## Rewards

### Current Implementation

**Status:** Off-chain (in PoC validator) or via simple bonus in `_distribute_rewards`

Rewards are not yet integrated into L1 at protocol level.

### Future Implementation

**L1 Integration:**

- Rewards for `SUBMIT_RESULT` transactions
- Distribution via `_distribute_rewards`
- Worker rating in state (off-chain or on-chain)

## Worker Requirements

### Hardware

- **GPU:** RTX 4090/5090 or similar (CUDA/ROCm support)
- **CPU:** Sufficient for task orchestration
- **RAM:** Depends on task type
- **Storage:** Minimal requirements (for code and data)

### Software

- **Python 3.12+**
- **CUDA Toolkit** or **ROCm** (for GPU computations)
- **L1 node** (for sending transactions)
- **PoC client** (for connecting to orchestrator)

### Network Connection

- Stable internet connection
- Access to L1 node (local or remote)
- Access to PoC validator (WebSocket/HTTP)

## Next Steps

- **[Local Worker](local-worker.md)** — Running a local worker
- **[Task Market](task-market.md)** — Publishing tasks
- **[PoC Details](../understand/poc.md)** — Proof-of-Compute details
