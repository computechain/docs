# Glossary

ComputeChain terminology.

## A

### Account

Blockchain account containing balance and nonce. Identified by address with prefix `cpc1...`.

### Address

Bech32-encoded identifier for account or validator. Formats:
- `cpc1...` — accounts
- `cpcvalcons1...` — validators (consensus addresses)

## B

### Block

Data structure containing header and transaction list. Blocks linked in chain via `prev_hash`.

### Block Reward

Reward validator receives for producing block. Planned schedule: initial reward 10 CPC with halving every 1,000,000 blocks. (Current MVP implementation may differ; see protocol code for actual emission.)

## C

### Compute Result

Data structure containing compute task execution result. Includes `task_id`, `worker_address`, `result_hash`, `proof`.

### Compute Root

Merkle root of all `ComputeResult` transactions in block. Stored in `BlockHeader.compute_root`.

### Consensus

Mechanism for coordinating blockchain state between nodes. ComputeChain uses PoA (Proof-of-Authority) with Round-Robin.

## D

### Devnet

Local network for development and testing. Parameters:
- Block Time: 10 seconds
- Epoch Length: 10 blocks
- Min Validator Stake: 1,000 CPC
- Max Validators: 5

## E

### Epoch

Period between validator set recalculations. Length:
- Devnet: 10 blocks
- Testnet: 100 blocks
- Mainnet: 72 blocks

### ECDSA

Digital signature algorithm used in MVP. Planned transition to Post-Quantum signatures (Dilithium, Falcon).

## F

### Fee

Transaction fee, calculated as `gas_used * gas_price`. Fees go to validator who produced block.

### Fork

Blockchain fork when different nodes have different chain versions. In the current MVP, if a block with mismatched `prev_hash` arrives during sync the node rolls back the latest block and retries synchronization. Full longest-chain handling is planned for future versions.

## G

### Gas

Unit of measurement for transaction computational complexity. Each transaction type has base gas cost:
- TRANSFER: 21,000 gas
- STAKE: 40,000 gas
- SUBMIT_RESULT: 80,000 gas

### Gas Limit

Maximum amount of gas that can be used by transaction or block.

### Gas Price

Price per unit of gas (in wei). Minimum values:
- Devnet: 1,000 wei
- Testnet: 5,000 wei
- Mainnet: 1,000,000,000 wei (1 Gwei)

### Genesis Block

First block of blockchain (height 0). Contains initial token distribution and network configuration.

## H

### Halving

Reduction of block reward by half. In ComputeChain occurs every 1,000,000 blocks.

## M

### Mainnet

Production ComputeChain network. Parameters:
- Block Time: 60 seconds
- Epoch Length: 72 blocks
- Min Validator Stake: 100,000 CPC
- Max Validators: 100

### Mempool

Pool of transactions waiting to be included in block. Validators select transactions from mempool when producing block.

### Merkle Root

Root of Merkle tree used for compact representation of data set (e.g., transactions or computation results).

## N

### Network ID

Network identifier: "devnet", "testnet", "mainnet". Used to prevent connecting to wrong network.

### Nonce

Sender transaction number. Starts at 0 and increments by 1 for each transaction. Used to prevent transaction replay.

## P

### PoA (Proof-of-Authority)

Consensus mechanism where validators produce blocks in turn (Round-Robin). Validators selected based on stake.

### PoC (Proof-of-Compute)

Mechanism for proving useful computation execution. Workers execute tasks on GPU and provide results with proofs.

### Post-Quantum (PQ)

Quantum-resistant cryptographic algorithms. ComputeChain is designed with PQ signatures (Dilithium, Falcon) in mind, but the MVP currently uses ECDSA.

### Proposer

Validator that produces block in current round. Selected via Round-Robin mechanism.

## R

### Round-Robin

Proposer selection mechanism where validators produce blocks strictly in turn.

### Reward Address

Account address where validator receives rewards for blocks and fees. By default set to sender address of STAKE transaction.

## S

### Stake

Amount of CPC tokens locked by validator. Determines validator position in ranking and ability to participate in consensus.

### State

Current blockchain state: account balances, validator stakes, nonce. Updated when applying transactions.

### Submit Result

Transaction of type `SUBMIT_RESULT` containing compute task execution result. Included in block and updates `compute_root`.

## T

### Testnet

Public test network. Parameters:
- Block Time: 30 seconds
- Epoch Length: 100 blocks
- Min Validator Stake: 100,000 CPC
- Max Validators: 21

### Transaction

Blockchain operation: token transfer, staking, submitting computation result. Signed by sender and included in block.

## V

### Validator

Network participant that produces blocks and maintains consensus. Identified by consensus address `cpcvalcons1...`. Selected based on stake.

### Validator Set

List of active validators that can produce blocks. Recalculated each epoch based on stake.

## W

### Wei

Minimum unit of CPC token. 1 CPC = 10^18 wei.

### Worker

Network participant that executes compute tasks on GPU and sends results via `SUBMIT_RESULT` transaction.

## Z

### ZK-Proof (Zero-Knowledge Proof)

Zero-knowledge proof allowing to prove computation correctness without revealing computations themselves. Planned for result verification in future.

## Next Steps

- **[Transaction Types](tx-types.md)** — Transaction types
- **[RPC API](rpc.md)** — RPC endpoints
- **[Overview](../understand/overview.md)** — ComputeChain overview
