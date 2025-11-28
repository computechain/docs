# ComputeChain Overview

## Architecture

ComputeChain consists of two main layers:

### L1 (Layer 1) — Blockchain Layer

**Purpose:** Provides deterministic consensus, state, staking, and security.

**Components:**

- **Consensus Engine:** PoA (Proof-of-Authority) with Round-Robin mechanism
- **State Management:** Account-based model with balances, nonce, and stakes
- **Post-Quantum Security:** Architecture ready for transition to quantum-resistant signatures (Dilithium, Falcon)
- **Gas & Fees:** Economic spam protection through fee model
- **P2P Network:** Decentralized synchronization of blocks and transactions

### PoC (Proof-of-Compute) — Compute Layer

**Purpose:** Distributes, executes, and verifies compute tasks.

**Components:**

- **ComputeTask:** Data structure for tasks to be executed
- **ComputeResult:** Task execution result with proof
- **L1 Integration:** `compute_root` in block headers (Merkle root of results)
- **Future:** ZK-Proofs for verification (`zk_state_proof`, `zk_compute_proof`)

## Participant Roles

### 1. Users

**Functions:**
- Create tasks through marketplace (web or API)
- Pay CPC for task execution
- Receive computation results

**Tools:**
- CLI wallet (`cpc-cli`)
- Task Market API (in development)

### 2. GPU Workers (Miners)

**Functions:**
- Have L1 address `cpc1...` and key
- Execute tasks on GPU (RTX 4090/5090 and beyond)
- Connect to PoC validator (orchestrator) via WebSocket/HTTP
- Send results through `SUBMIT_RESULT` transaction

**Requirements:**
- GPU with CUDA/ROCm support
- L1 node for sending transactions
- Connection to PoC validator

### 3. Validators

**Functions:**
- Produce blocks strictly in turn (Round-Robin)
- Verify transactions and basic validity of computation results (future: full proof verification)
- Maintain network consensus
- Receive transaction fees and block rewards

**Requirements (by network):**
- Devnet: min stake 1,000 CPC, max 5 validators, epoch every 10 blocks (~100 sec)
- Testnet: min stake 100,000 CPC, max 21 validators, epoch every 100 blocks (~50 min)
- Mainnet: min stake 100,000 CPC, max 100 validators, epoch every 72 blocks (~72 min)

### 4. PoC Validator / Orchestrator (off-chain)

**Functions:**
- Receives tasks from marketplace
- Splits them into computational jobs
- Distributes jobs to workers
- Verifies results and proofs
- Sends (or validates) `SUBMIT_RESULT` on behalf of worker to L1

**Status:** In development (Stage 5)

## Consensus

### PoA (Proof-of-Authority)

**Mechanism:** Round-Robin (in turn)

- Validators produce blocks strictly in turn
- If a validator misses a slot, the network waits for the next round
- Validator set is recalculated every **10 blocks** (epoch)

### Post-Quantum Security

**Current Implementation:**
- Blocks are signed through `PQ-Scheme` abstraction
- Devnet uses secp256k1 wrapper
- Data structure (`pq_signature`, `pq_pub_key`) is ready for Dilithium/Falcon integration

### Fork Resolution

**Mechanism (MVP):** Rollback on mismatch

- If a node receives a block whose `prev_hash` mismatches the local head during sync, it rolls back the latest block and retries synchronization.
- Full multi-branch / longest-chain selection is planned for future releases.

## Economics

### Gas Model

**Spam Protection:** Similar to Ethereum

- Each transaction has `gas_limit` and `gas_price`
- Fee `fee = gas_used * gas_price` goes to the validator

**Base Gas Costs:**
- Transfer: 21,000 gas
- Stake: 40,000 gas
- Submit Result: 80,000 gas

**Network Parameters:**
- `BLOCK_GAS_LIMIT`: 10,000,000 (devnet)
- `MIN_GAS_PRICE`: 1,000 (devnet)

### Rewards

**Block Reward:**
- Initial reward: 10 CPC
- Halving every 1,000,000 blocks

**Distribution:**
- Validator receives `block_reward + fees_total`
- Fees collected from all transactions in the block
- Reward sent to validator's `reward_address`

## Storage

**Database:** SQLite

- Blocks stored in `chain.db`
- State (accounts, validators) in memory with periodic persistence
- Race condition protection through DB transactions

## Network

**P2P Protocol:**
- TCP-based protocol for synchronization
- Handshake on connection
- Block and transaction propagation
- Automatic peer saving to `peers.json` (MVP implementation continues to be improved)

**RPC API:**
- FastAPI server on port 8000 (default)
- Endpoints: `/status`, `/block/{height}`, `/balance/{address}`, `/validators`, `/tx/send`

## Next Steps

- **[Proof-of-Compute](poc.md)** — PoC layer details
- **[Tokenomics](tokenomics.md)** — Economic model
- **[Node Setup](../node/run-local.md)** — Running a node
