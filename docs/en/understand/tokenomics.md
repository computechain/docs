# Tokenomics

## CPC Token

**Name:** ComputeChain  
**Ticker:** CPC  
**Decimals:** 18  
**Minimum Unit:** 1 wei = 10^-18 CPC

## Emission

### Genesis Distribution

**Devnet:**
- Genesis premine: 1,000,000,000 CPC (for testing)
- Faucet key: Deterministic key for token distribution

**Testnet:**
- Genesis premine: defined in testnet config (non-zero to fund faucets and testing accounts)
- Distribution via faucet, team allocations, or mock exchanges

**Mainnet:**
- Genesis premine: 0 CPC (fair launch in current design)
- Distribution model: fair launch; if design changes (e.g., presale), it will be reflected in config/docs

### Block Rewards

**Formula:**

```python
def calculate_block_reward(height: int) -> int:
    initial_reward = 10 * 10**18  # 10 CPC
    halvings = height // 1_000_000
    reward = initial_reward >> halvings
    return reward
```

**Halving:**
- Every 1,000,000 blocks
- Initial reward: 10 CPC
- After first halving: 5 CPC
- After second halving: 2.5 CPC
- And so on...

### Reward Distribution

**Block Reward + Transaction Fees:**

```
Total Reward = Block Reward + Fees Total

Block Reward: 10 CPC (initial)
Fees Total: sum of all fees in block
```

**Recipient:** Validator who produced the block

**Reward Address:**
- Uses validator's `reward_address`
- If not specified, calculated from validator's `pq_pub_key`
- Fallback: validator doesn't receive reward (warning logged)

## Gas & Fees

### Gas Costs

**Base Gas Costs:**

| Transaction Type | Gas Cost |
|-----------------|----------|
| TRANSFER | 21,000 |
| STAKE | 40,000 |
| SUBMIT_RESULT | 80,000 |

### Gas Price

**Minimum Gas Price:**
- Devnet: 1,000 wei
- Testnet: 5,000 wei
- Mainnet: 1,000,000,000 wei (1 Gwei)

**Fee Calculation:**

```
fee = gas_used * gas_price
```

**Example:**

```python
# Transfer transaction
gas_used = 21_000
gas_price = 1_000
fee = 21_000 * 1_000 = 21_000_000 wei = 0.000021 CPC
```

### Block Gas Limit

**Limits:**

- Devnet: 10,000,000 gas
- Testnet: 15,000,000 gas
- Mainnet: 30,000,000 gas

**Maximum transactions per block:**

- Devnet: 100 transactions (at average gas ~100,000)
- Testnet: 1,000 transactions
- Mainnet: 5,000 transactions

## Staking

### Minimum Stake

**Validator Requirements:**

- Devnet: 1,000 CPC
- Testnet: 100,000 CPC
- Mainnet: 100,000 CPC

### Maximum Validators

- Devnet: 5 validators
- Testnet: 21 validators
- Mainnet: 100 validators

### Epoch

**Epoch Length:**

- Devnet: 10 blocks (~100 seconds)
- Testnet: 100 blocks (~50 minutes)
- Mainnet: 72 blocks (~72 minutes)

**What happens in epoch:**

1. Validator set recalculation
2. Sort by stake (descending)
3. Select top-N validators (N = max_validators)
4. Activate/deactivate validators

## Economic Incentives

### For Validators

**Revenue:**
- Block rewards (10 CPC initial)
- Transaction fees (fees from all transactions in block)
- Block production frequency depends on position in Round-Robin

**Expenses:**
- Gas fees for staking transactions
- Infrastructure (server, internet)

**Risks:**
- Slashing (future) for incorrect behavior
- Deactivation if stake is insufficient

### For Workers (GPU Workers)

**Current Implementation:**
- Rewards off-chain (via PoC validator)
- Or via simple bonus in `_distribute_rewards`

**Future Implementation:**
- Rewards for `SUBMIT_RESULT` transactions
- Distribution via Task Market
- Worker rating and reputation

**Expenses:**
- Gas fees for `SUBMIT_RESULT` transactions (80,000 gas)
- Electricity for GPU
- Infrastructure (L1 node, connection to PoC validator)

### For Users

**Expenses:**
- Task payment via Task Market
- Gas fees for transactions (if sending directly)

**Benefits:**
- Access to distributed GPU resources
- Decentralized computation execution

## Deflationary Mechanisms

### Burning (Future)

**Planned:**
- Part of fees burned
- Part of task payments burned
- Effective supply decreases over time

**Current Implementation:**
- Burning not implemented
- All fees go to validators

## Inflation

### Current Model

**Emission Inflation (example using devnet parameters for intuition):**

```
Annual Emission ≈ (Block Reward * Blocks per Year)

Example:
Block Reward = 10 CPC
Block Time = 10 sec (devnet)
Blocks per Year ≈ 3,153,600
Annual Emission ≈ 31,536,000 CPC
```

For testnet/mainnet, actual emission depends on network parameters (block time, halving schedule, validator count).

**Halving reduces inflation (per schedule above).**

### Deflationary Pressure

**Future Mechanisms:**
- Fee burning
- Task payment burning
- Staking (tokens locked)

## Next Steps

- **[Staking Guide](../staking/staking-basic.md)** — How to stake
- **[Rewards](../staking/rewards.md)** — Reward details
- **[Validator Lifecycle](../staking/validator-lifecycle.md)** — Validator lifecycle
