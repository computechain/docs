# Proof-of-Compute (PoC)

## Concept

**Proof-of-Compute** is a mechanism that replaces the meaningless hash rate of classical Proof-of-Work with **useful computations** executed on GPU.

Instead of searching for a nonce that satisfies a hash condition, workers execute real computational tasks and provide proofs of correct execution.

## PoC Architecture

### L1 Integration

**In block header:**

```python
class BlockHeader:
    # ... other fields ...
    compute_root: str  # Merkle root of computation results
    zk_state_proof: Optional[str] = None  # Reserved for ZK-proofs
    zk_compute_proof: Optional[str] = None  # Reserved for ZK-proofs
```

**`compute_root`** is calculated as Merkle root of all `ComputeResult` transactions in the block:

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
    
    return compute_merkle_root(leaves).hex()
```

### Data Structures

#### ComputeTask

**Status:** In development (Stage 5)

Task for execution on GPU:

```python
class ComputeTask:
    task_id: str  # Task UUID
    challenge_type: str  # "matrix_mul", "synthetic", etc.
    payload: dict  # Task parameters (seed, matrix_size, etc.)
    reward: int  # Execution reward in wei (internal representation)
    deadline: int  # Deadline timestamp
```
> In external APIs (Task Market), rewards are usually specified as decimal CPC strings (e.g. `"10.0"`). The internal protocol stores rewards as integers in wei.

#### ComputeResult

**Implemented:** ✅ Stage 4

Task execution result:

```python
class ComputeResult:
    task_id: str  # Task UUID
    worker_address: str  # Worker address (cpc1...)
    result_hash: str  # Result hash
    proof: Optional[str] = None  # Correctness proof (future: ZK-proof)
    nonce: Optional[int] = None  # For synthetic tasks
    signature: Optional[str] = None  # Worker signature
```

### SUBMIT_RESULT Transaction

**Transaction Type:** `TxType.SUBMIT_RESULT`

**Gas Cost:** 80,000 gas

**Payload:**

```json
{
  "task_id": "uuid-here",
  "worker_address": "cpc1...",
  "result_hash": "1234567890abcdef...",
  "proof": "...",
  "nonce": 12345,
  "signature": "..."
}
```

**Validation:**

1. `ComputeResult` structure must be valid
2. `worker_address` must match `tx.from_address`
3. Proof is verified (future: via ZK-verification)

## Task Execution Workflow

### Current Implementation (Stage 4)

**Simplified flow:**

1. **Worker** generates task from block hash (synthetic)
2. **Worker** executes computation (CPU/GPU mock)
3. **Worker** sends `SUBMIT_RESULT` transaction to L1
4. **L1 validator** verifies structure and includes in block
5. **`compute_root`** is updated in block header

### Future Implementation (Stage 5)

**Full flow with marketplace:**

1. **User** creates task via Task Market API
2. **PoC validator** receives task and splits into jobs
3. **PoC validator** distributes jobs to workers via WebSocket
4. **Worker** executes task on GPU
5. **Worker** sends result with proof back
6. **PoC validator** verifies result (selective verification)
7. **PoC validator** or **Worker** sends `SUBMIT_RESULT` to L1
8. **L1 validator** includes transaction in block
9. **Worker** receives reward (off-chain or via L1 reward)

## Task Types

### Synthetic Tasks

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

**Purpose:** Useful computations (inference, training, etc.)

**Type:** `challenge_type: "inference"`, `"training"`, etc.

**Properties:**
- Loaded via Task Market
- Paid by user
- Verified via ZK-proofs or duplicate execution

## Result Verification

### Current Implementation

**MVP:** Data structure validation only

- `ComputeResult` format validation
- Address matching check
- Actual computation result is not recomputed on L1; correctness is assumed or checked off-chain by PoC validators

### Future Implementation

**ZK-Proofs:**

- Worker generates ZK-proof of correct execution
- L1 validator verifies proof without recomputation
- Fast verification even for complex tasks

**Selective Verification:**

- PoC validator selects random results for checking
- Duplicate execution on other workers
- Slashing for incorrect results

## Computation Rewards

### Current Implementation

**Status:** Off-chain (in PoC validator) or via simple bonus in `_distribute_rewards`

Rewards are not yet integrated into L1 at protocol level.

### Future Implementation

**L1 Integration:**

- Rewards for `SUBMIT_RESULT` transactions
- Distribution via `_distribute_rewards`
- Worker rating in state (off-chain or on-chain)

## Next Steps

- **[GPU Workers](../mining/overview.md)** — How to become a worker
- **[Task Market](../mining/task-market.md)** — Publishing tasks
- **[Local Worker](../mining/local-worker.md)** — Running a local worker
