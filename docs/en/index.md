# ComputeChain Documentation

**ComputeChain** — an experimental blockchain with **Proof-of-Compute** architecture, focused on executing **useful computations on GPU** (RTX 4090/5090 and beyond).

## What is ComputeChain?

ComputeChain replaces the meaningless hash rate of classical Proof-of-Work with **useful computations** executed on mass-market GPUs. The network provides deterministic consensus, state, staking, and security, ready to transition to quantum-resistant signatures (Post-Quantum Security).

## Roles in the Network

### 👤 Users
Create tasks for execution (inference, training, synthetic computations). Pay CPC for task execution through the marketplace.

### ⚙️ Workers (GPU Workers / Miners)
Execute tasks on GPU, send results through `SUBMIT_RESULT` transaction and receive rewards for correct computation execution.

### ✅ Validators
Maintain consensus (PoA Round-Robin), verify transactions and included compute results at the protocol level, produce blocks and receive block rewards and fees.

### 💰 Stakers
Stake CPC tokens to become validators, ensuring network security and receiving block rewards and fees.

## Quick Start

### Running a Local Testnet with Two Nodes

**Terminal 1 — Node A (Genesis Validator):**

```bash
cd computechain
chmod +x start_node_a.sh
./start_node_a.sh
```

**Terminal 2 — Node B (Second Validator):**

```bash
cd computechain
chmod +x start_node_b.sh
./start_node_b.sh
```

After one epoch (10 blocks), validators will start alternating in block production.

### Sending Transactions via CLI

```bash
# Check balance
./cpc-cli query balance <ADDRESS> --node http://localhost:8000

# Send tokens
./cpc-cli tx send <TO_ADDR> <AMOUNT> --from <KEY_NAME> --node http://localhost:8000

# Stake (become validator)
./cpc-cli tx stake <AMOUNT> --from <KEY_NAME> --node http://localhost:8000
```

## Current Status

**Stage 4 (Proof-of-Compute Framework)** — ✅ Implemented:

- ✅ **Consensus:** Multi-Validator PoA (Round-Robin) with PQ-ready signature abstraction (secp256k1 in MVP)
- ✅ **Economics:** Gas Model (like Ethereum) for spam protection
- ✅ **Staking:** Dynamic validator set
- ✅ **PoC Core:** Task data structures, result transactions, `compute_root` validation

**Stage 5 (Proof-of-Compute & Market)** — 🚧 In Development:

- 🚧 GPU Workers: Real task processing on Python/CUDA
- 🚧 PoC-Validator: Task and worker orchestration
- 🚧 Task Market: API for publishing and paying for tasks

## Architecture

```
ComputeChain/
├── blockchain/      # L1 node (consensus, state, staking, validators)
├── protocol/        # Common protocol (types, crypto, config shared by L1 & PoC)
├── miner/           # PoC worker stack (GPU miner, scheduler, tooling)
├── validator/       # PoC validator/orchestrator services
├── cli/             # User CLI (keys, staking, txs)
└── scripts/         # Launch scripts, demos, localnet tooling
```

## Documentation

- **[Understand ComputeChain](understand/overview.md)** — Architecture and concepts
- **[Wallets & Keys](wallets/address-formats.md)** — Working with wallets
- **[Staking & Validators](staking/staking-basic.md)** — How to become a validator
- **[GPU Workers / Mining](mining/overview.md)** — Executing computations
- **[Node & Network](node/run-local.md)** — Running and configuring a node
- **[CLI & SDK](cli/cpc-cli.md)** — CLI commands
- **[Testnet & Bug Bounty](testnet/join.md)** — Connecting to testnet

## Useful Links

- [GitHub Repository](https://github.com/computechain/computechain)
- [Technical Specification](../TZ_POC) (external file)

---

**Documentation Version:** corresponds to Stage 4 (Proof-of-Compute Framework)

