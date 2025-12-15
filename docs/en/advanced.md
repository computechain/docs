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
- `/metrics` (future) - Prometheus-compatible metrics

## Protocol Upgrades

### Hard Fork Process (Future)

1. **Proposal**: New protocol version proposed with height
2. **Signaling**: Validators signal readiness via block headers
3. **Activation**: At specified height, new rules activate
4. **Migration**: State migrated if needed

### Governance (Planned)

- On-chain voting weighted by stake
- Parameter changes (gas costs, epoch length, etc.)
- Protocol upgrades

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

## Next Steps

- **[Validator Guide](validator-guide.md)** - Run a validator node
- **[Staking Guide](staking-guide.md)** - Stake and earn rewards
- **[API Reference](api-reference.md)** - RPC endpoints
