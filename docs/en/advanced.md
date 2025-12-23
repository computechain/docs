# Advanced Topics

Deep dive into ComputeChain architecture, Proof-of-Compute, and technical details.

## Architecture

### Three-Layer Design

ComputeChain operates as three interconnected layers:

**1. Blockchain Layer (State)**
- Stores account balances, validator stakes, delegations
- Maintains transaction history and block headers
- Provides immutable audit trail for all operations

**2. Consensus Layer (Validators)**
- Produces blocks in round-robin fashion (PoA)
- Validates transactions and state transitions
- Enforces protocol rules (gas, slashing, rewards)
- Tracks validator performance (uptime, missed blocks)

**3. Compute Layer (Workers)**
- Executes GPU computation tasks
- Submits results via SUBMIT_RESULT transactions
- Results verified by Proof-of-Compute rules
- Economic incentives reward correct execution

### Network Topology

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Validator A │────▶│ Validator B │────▶│ Validator C │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                            │
                    ┌───────┴────────┐
                    │                │
              ┌──────────┐    ┌──────────┐
              │ Worker 1 │    │ Worker 2 │
              └──────────┘    └──────────┘
```

Validators form P2P mesh network using libp2p. Workers connect via RPC to submit compute results.

## Consensus Mechanism

### Round-Robin PoA

**Block Production:**
- Validators take turns producing blocks
- Proposer determined by: `proposer_index = height % num_active_validators`
- Block time: ~10 seconds (configurable)
- No fork choice needed (deterministic single chain)

**Validator Lifecycle:**

```
INACTIVE → wait 100 blocks → ACTIVE → produce blocks → earn rewards
    ↓                            ↓
    └─────────────────────────JAILED (uptime < 75%)
                                 ↓
                            pay unjail fee → ACTIVE
                                 ↓
                            3x jail → EJECTED (permanent)
```

### Epoch System

**Epoch Length:** 100 blocks

**Epoch Transitions:**
1. Calculate uptime scores for all validators
2. Jail validators with uptime < 75%
3. Apply slashing penalties (5% → 10% → 100%)
4. Activate new validators meeting minimum stake
5. Deactivate validators below minimum power

## Proof-of-Compute (PoC)

### Concept

Traditional blockchains use Proof-of-Work for security, but the computation is "useless" (hash grinding). ComputeChain aims to replace this with **useful** GPU computations while maintaining verifiability.

### PoC v1 (Current)

**Task Creation:**
- Anyone can submit SUBMIT_RESULT transaction
- Task ID (UUID) identifies the computation
- Result hash commits to output

**Verification (Basic):**
- Current MVP accepts results without deep verification
- Future versions will add probabilistic checking

### PoC v2+ (Planned)

**Enhanced Verification:**

1. **Redundant Execution**: Multiple workers execute same task, results compared
2. **Sampling**: Validators randomly verify subset of results
3. **Challenge Period**: Window for disputes on incorrect results
4. **Economic Penalties**: Incorrect results slash worker stake/reputation

**Workflow:**

```
Task Posted → Worker Assigned → Execution → Result Submitted
                                               ↓
                               ┌───────────────┴──────────────┐
                               ↓                              ↓
                          Verification                    Challenge
                          (sampling)                      (dispute)
                               ↓                              ↓
                           Accepted                        Slashed
                               ↓
                          Payment Released
```

### Use Cases

**Current:**
- Simple compute task submissions (proof-of-concept)
- Merkle root tracking in block headers

**Planned:**
- AI inference (LLM, image models)
- 3D rendering (Blender, etc.)
- Video encoding (FFMPEG, x264)
- Scientific computing (simulations, matrix operations)

## Tokenomics

### CPC Token

**Supply:**
- Initial supply: Configured in genesis
- Block rewards: 10 CPC per block (halves every 1M blocks)
- Max supply: Determined by halving schedule

**Utility:**
1. **Staking**: Validators lock CPC as collateral
2. **Delegation**: Passive holders delegate to validators
3. **Gas Fees**: All transactions pay gas in CPC
4. **Compute Payments**: Tasks paid in CPC
5. **Governance**: (Future) voting on protocol parameters

### Block Rewards

**Reward Formula:**

```python
initial_reward = 10 * 10**18  # 10 CPC
halvings = height // 1_000_000
reward = initial_reward >> halvings
```

**Distribution Schedule:**

| Height | Block Reward |
|--------|--------------|
| 0 - 999,999 | 10 CPC |
| 1M - 1.999M | 5 CPC |
| 2M - 2.999M | 2.5 CPC |
| 3M - 3.999M | 1.25 CPC |

### Reward Distribution

**Without Delegations:**
- Validator receives 100% of (block reward + transaction fees)

**With Delegations:**

```
Total Reward = Block Reward + Transaction Fees
Commission = Total Reward × validator.commission_rate (default 10%)
Delegator Share = Total Reward - Commission

For each delegator:
  Reward = (Delegator Share × delegation.amount) / validator.total_delegated
```

**Example:**

```
Block Reward: 10 CPC
Tx Fees: 0.0001 CPC
Total: 10.0001 CPC
Commission (10%): 1.00001 CPC → Validator
Delegator Share (90%): 9.00009 CPC

Delegator A (60% of stake): 5.40 CPC
Delegator B (40% of stake): 3.60 CPC
```

### Slashing Penalties

**Graduated Slashing:**

| Jail Count | Penalty | Action |
|------------|---------|--------|
| 1st | 5% of stake slashed | Temporary jail |
| 2nd | 10% of stake slashed | Temporary jail |
| 3rd | 100% of stake slashed | **EJECTED** (permanent) |

**Unstake Penalty:**
- Unstaking while jailed: Additional 10% penalty

## Gas Model

### Gas Costs

Transaction types have base gas costs:

```python
GAS_PER_TYPE = {
    TxType.TRANSFER: 21_000,
    TxType.STAKE: 40_000,
    TxType.UNSTAKE: 40_000,
    TxType.DELEGATE: 35_000,
    TxType.UNDELEGATE: 35_000,
    TxType.UNJAIL: 50_000,
    TxType.UPDATE_VALIDATOR: 30_000,
    TxType.SUBMIT_RESULT: 80_000,
}
```

### Fee Calculation

```python
fee = gas_limit × gas_price
```

**Example:**
```
TRANSFER transaction:
gas_limit = 21,000
gas_price = 1000 wei
fee = 21,000,000 wei = 0.000021 CPC
```

### Gas Price Market

**Current:** Fixed gas price (1000 wei recommended)

**Future:** Dynamic gas price based on network congestion:
- Base fee burns (EIP-1559 style)
- Priority fee tips validators

## Cryptography

### Current Implementation (ECDSA)

**Signing:**
- secp256k1 curve (same as Bitcoin/Ethereum)
- 32-byte private keys
- Recoverable signatures (65 bytes)

**Address Derivation:**

```
Private Key → Public Key (33 bytes compressed) → Hash → Bech32 Encode
```

**Address Formats:**
- Regular accounts: `cpc1...`
- Validators: `cpcvalcons1...`

### Post-Quantum Ready

**Architecture supports:**
- Dilithium (NIST standard)
- Falcon (compact signatures)
- Future migration path without protocol breaking changes

**Fields reserved in BlockHeader:**
```python
pq_signature: Optional[bytes]
pq_pub_key: Optional[bytes]
```

## State Management

### Account State

```python
class Account:
    address: str
    balance: int  # in wei
    nonce: int
    reward_history: Dict[int, int]  # epoch → rewards
```

### Validator State

```python
class Validator:
    address: str  # cpcvalcons1...
    pq_pub_key: str
    power: int  # staked amount
    is_active: bool
    is_jailed: bool
    reward_address: str  # where rewards go
    commission_rate: float  # 0.0-1.0
    delegations: List[Delegation]
```

### State Root

Each block header includes:
- `tx_root`: Merkle root of transactions
- `state_root`: Hash of account state
- `compute_root`: Merkle root of compute results

## Network Parameters

### Devnet

```
Chain ID: computechain-devnet
Block Time: 10 seconds
Epoch Length: 100 blocks
Min Stake: 100 CPC
Min Uptime: 75%
Unjail Fee: 1000 CPC
```

### Testnet (Planned)

```
Chain ID: computechain-testnet-1
Validators: ~21
Block Time: 10 seconds
```

### Mainnet (Future)

```
Chain ID: computechain-1
Validators: 50-100
Block Time: 6 seconds
Epoch Length: 200 blocks
```

## Performance Tracking

### Uptime Score

```python
uptime_score = blocks_signed / total_expected_blocks
```

**Calculation:**
- Track every block within epoch
- If validator was proposer but didn't produce → missed block
- Uptime < 75% → jailed at epoch transition

### Monitoring Metrics

**Node exposes:**
- `/status` - Current height, epoch, mempool size
- `/validators` - All validators with uptime scores
- `/metrics` ✅ **Implemented** - Prometheus-compatible metrics

**Prometheus metrics (Phase 1.3):**
- `computechain_block_height` - Current block height
- `computechain_transactions_total` - Total transactions processed (by type)
- `computechain_mempool_size` - Mempool size
- `computechain_validator_count` - Number of validators
- `computechain_total_supply` - Total supply in circulation
- `computechain_total_burned` - Total tokens burned
- `computechain_total_minted` - Total tokens minted
- `computechain_accounts_total` - Number of accounts in network

**Grafana integration:**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'computechain'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s
```

## State Snapshots

### Snapshot System (Phase 1.3) ✅ **Implemented**

**Automatic creation:**
- Every N blocks (default: 1000)
- At epoch boundaries
- Gzip compression (~60-80% size reduction)
- SHA256 integrity verification

**Fast Sync:**
- Load state from snapshot
- Sync in <5 minutes (instead of hours)
- Automatic cleanup (keeps last 10 snapshots)

**API endpoints:**
- `GET /snapshots` - List available snapshots
- `GET /snapshots/{height}` - Info about specific snapshot

**CLI commands:**
- `./cpc-cli snapshot list` - List snapshots
- `./cpc-cli snapshot info <height>` - Detailed information

**Snapshot contents:**
- All account balances
- Validator stakes and delegations
- Unbonding queue
- Reward history
- Economic tracking (total_burned, total_minted)
- Treasury state

## Protocol Upgrades

### Upgrade System (Phase 1.3) ✅ **Implemented**

**Semantic versioning:**
- MAJOR.MINOR.PATCH (e.g., 1.0.0)
- MAJOR - breaking changes
- MINOR - new features (backward compatible)
- PATCH - bug fixes

**Upgrade process:**
1. **Planning**: UpgradePlan created with target_version and upgrade_height
2. **Migration**: @migration decorators for state migration
3. **Execution**: At upgrade_height, migrations applied
4. **Validation**: Version and compatibility checks

**Migration example:**
```python
from blockchain.upgrade.migrations import migration

@migration(from_version="1.0.0", to_version="1.1.0")
def migrate_add_new_field(state):
    # State migration logic
    for account in state.accounts.values():
        if not hasattr(account, 'new_field'):
            account.new_field = default_value
```

**Components:**
- `blockchain/upgrade/manager.py` - UpgradeManager
- `blockchain/upgrade/types.py` - Version, UpgradePlan, ChainVersion
- `blockchain/upgrade/migrations.py` - MigrationRegistry

**Status:** Framework ready, testing in testnet (Phase 3)

### Governance (Phase 4 - Planned)

- On-chain voting weighted by stake
- Parameter changes (gas costs, epoch length, etc.)
- Protocol upgrades via governance

## Technical Specifications

### Transaction Structure

```python
class Transaction:
    tx_type: TxType
    from_address: str
    to_address: Optional[str]
    amount: int
    fee: int
    nonce: int
    gas_price: int
    gas_limit: int
    timestamp: int
    signature: str
    pub_key: str
    payload: Dict
```

### Block Structure

```python
class BlockHeader:
    height: int
    timestamp: int
    prev_hash: str
    proposer_address: str
    tx_root: str
    state_root: str
    compute_root: str
    chain_id: str
    signature: str
    pub_key: str
```

### P2P Protocol

**Transport:** libp2p with TCP/QUIC

**Topics:**
- `/computechain/blocks/1.0.0` - Block propagation
- `/computechain/txs/1.0.0` - Transaction gossip

**Peer Discovery:**
- Bootstrap nodes (seeds)
- Kademlia DHT

## Security Considerations

### Attack Vectors

**Validator Cartels:**
- Mitigated by minimum uptime requirements
- Slashing for coordinated attacks

**Nothing-at-Stake:**
- N/A (PoA has deterministic block proposer)

**Long-Range Attacks:**
- Mitigated by social consensus on genesis
- Checkpointing (future)

**Compute Result Fraud:**
- Addressed by PoC verification (v2+)
- Economic penalties for incorrect results

## Transaction Lifecycle (Phase 1.4)

### Transaction States

Every transaction goes through the following lifecycle:

```
SUBMITTED → PENDING → CONFIRMED / FAILED / EXPIRED
```

**1. Submitted**
- Transaction sent via `/tx/send` API
- Initial validation (signature, nonce, balance)
- Added to mempool if valid

**2. Pending**
- Transaction waiting in mempool
- Not yet included in a block
- Can be queried via `/tx/{hash}/receipt`

**3. Confirmed**
- Transaction included in a block
- State updated (balance transferred, stake recorded, etc.)
- Receipt available with block height

**4. Failed**
- Invalid transaction (insufficient balance, invalid nonce)
- Rejected by validator
- Error message in receipt

**5. Expired** (Phase 1.4 - NEW!)
- Transaction not confirmed within TTL (Time-To-Live)
- Automatically removed from mempool after 1 hour
- Prevents mempool overflow

### Transaction Receipts

Query transaction status:

```bash
GET /tx/{tx_hash}/receipt

Response:
{
  "tx_hash": "abc123...",
  "status": "confirmed",      // pending | confirmed | failed
  "block_height": 12345,
  "timestamp": 1703347200,
  "confirmations": 5,          // current_height - block_height + 1
  "error": null
}
```

### TX TTL (Time-To-Live)

**Problem:** Pending transactions could get stuck in mempool forever.

**Solution:** Automatic cleanup after 1 hour (3600 seconds).

**How it works:**
1. Transaction added to mempool → timestamp recorded
2. Periodic cleanup (every 30 seconds)
3. If `age > TTL` → transaction removed and marked as `expired`
4. Nonce unblocked → user can retry with higher fee

**Benefits:**
- ✅ Prevents mempool bloat
- ✅ Unblocks stuck nonces
- ✅ Improves system performance

## Finality Guarantees

### Instant Finality (Tendermint BFT)

**ComputeChain uses Tendermint consensus** which provides **instant finality**:

**1 block = FINAL** ✅

Once a block is added to the blockchain, it **cannot be reverted** (no reorgs).

### Comparison with Other Blockchains

| Blockchain | Finality Type | Time to Final |
|------------|---------------|---------------|
| **Bitcoin** | Probabilistic (6 blocks) | ~60 minutes |
| **Ethereum PoW** | Probabilistic (12 blocks) | ~3 minutes |
| **Ethereum PoS** | Casper FFG (2 epochs) | ~15 minutes |
| **Solana** | Vote-based (~32 blocks) | ~13 seconds |
| **ComputeChain** | **Instant (Tendermint)** | **0 seconds!** ✅ |

### How Tendermint Finality Works

1. **Proposer** creates block
2. **Validators** vote on block (2/3+ required)
3. Block added to chain → **FINAL**
4. Next block references it → impossible to change

### Byzantine Fault Tolerance

- System safe if < 1/3 validators are Byzantine (malicious)
- If ≥ 2/3 honest → finality guaranteed
- No possibility of chain reorganization

### Recommended Confirmations

While 1 confirmation is technically final, exchanges and applications may want extra safety:

```python
# Normal transfers
MIN_CONFIRMATIONS = 1  # Instant finality!

# Critical operations (extra paranoia)
CRITICAL_CONFIRMATIONS = 3  # ~30 seconds

# Large withdrawals (exchange standard)
EXCHANGE_CONFIRMATIONS = 6  # ~60 seconds
```

## Gas Model

### Phase 1: Fixed Fee (Current)

ComputeChain currently uses a **simple fixed-fee model**:

```python
class Transaction:
    fee: int = 0         # Fixed fee per transaction
    gas_price: int = 0   # Reserved for Phase 2
    gas_limit: int = 0   # Reserved for Phase 2
```

**Why fixed fees?**
- ✅ Simplicity for MVP
- ✅ Predictable costs
- ✅ No fee market competition needed (low TPS)

**Current fee:** Zero or minimal (set by validators)

### Phase 2: Dynamic Gas (Planned)

**EIP-1559 style gas pricing** (Q2 2025+):

```python
class Transaction:
    base_fee: int        # Algorithmic (burned 🔥)
    priority_fee: int    # Tip for validators 💰
    max_fee: int         # User protection cap 🛡️
```

**How it will work:**

1. **Base Fee** - Algorithmically adjusted based on block congestion
   - Blocks > 50% full → base fee increases
   - Blocks < 50% full → base fee decreases
   - **Burned** (removed from supply) → deflationary

2. **Priority Fee** - User-set tip for validators
   - Incentivizes block inclusion
   - Goes to block proposer

3. **Max Fee Cap** - Protection from fee spikes
   - TX fails if `base_fee + priority_fee > max_fee`

**Benefits:**
- ✅ Better fee estimation
- ✅ Reduced volatility
- ✅ Deflationary pressure (burned fees)

### Transaction Gas Costs

Reserved for Phase 2 (placeholders):

| Transaction Type | Base Gas |
|-----------------|----------|
| TRANSFER | 21,000 |
| STAKE | 50,000 |
| UNSTAKE | 50,000 |
| DELEGATE | 30,000 |
| COMPUTE_SUBMIT | 100,000 |
| COMPUTE_RESULT | 150,000 |

## Next Steps

- **[Validator Guide](validator-guide.md)** - Run a validator node
- **[Staking Guide](staking-guide.md)** - Stake and earn rewards
- **[API Reference](api-reference.md)** - RPC endpoints
