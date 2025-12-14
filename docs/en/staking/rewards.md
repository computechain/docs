# Validator Rewards

Validators receive rewards for block production and transaction fees.

## Reward Sources

### 1. Block Reward

**Initial Reward (planned schedule):** 10 CPC

**Formula:**

```python
def calculate_block_reward(height: int) -> int:
    initial_reward = 10 * 10**18  # 10 CPC
    halvings = height // 1_000_000
    reward = initial_reward >> halvings
    return reward
```

**Halving (planned schedule):**

- Every 1,000,000 blocks
- Reward decreases by half

**Examples:**

| Block Height | Reward |
|-------------|---------|
| 0 - 999,999 | 10 CPC |
| 1,000,000 - 1,999,999 | 5 CPC |
| 2,000,000 - 2,999,999 | 2.5 CPC |

> Current MVP implementation may use a fixed or zero block reward. Check the code (`calculate_block_reward`) for the exact behavior in your build.

### 2. Transaction Fees

**Source:** Fees from all transactions in block

**Calculation:**

```python
fees_total = sum(GAS_PER_TYPE.get(tx.tx_type, 0) * tx.gas_price for tx in block.txs)
```

**Gas Costs:**

| Transaction Type | Base Gas |
|---------------|----------|
| TRANSFER | 21,000 |
| STAKE | 40,000 |
| SUBMIT_RESULT | 80,000 |

**Example:**

```
Block contains:
- 5 TRANSFER transactions (gas_price=1000)
- 1 STAKE transaction (gas_price=1000)

Fees = (5 * 21_000 * 1000) + (1 * 40_000 * 1000)
     = 105_000_000 + 40_000_000
     = 145_000_000 wei
     = 0.000145 CPC
```

## Reward Distribution

### Distribution Process

**Trigger:** When block is added

**Distribution Logic:**

1. **Calculate Total Reward:** `total_reward = block_reward + transaction_fees`
2. **Check for Delegations:**
   - If validator has delegations → apply commission split
   - If no delegations → validator receives 100%

### Without Delegations

Validator receives full reward:

```python
total_reward = block_reward + fees_total
validator_account.balance += total_reward
```

### With Delegations & Commission

**Commission Model (Default: 10%):**

```python
# Validator has delegations
commission_amount = int(total_reward * validator.commission_rate)  # 10%
delegators_share = total_reward - commission_amount  # 90%

# Validator receives commission
validator_account.balance += commission_amount

# Delegators receive proportional share
for delegation in validator.delegations:
    delegator_reward = (delegators_share * delegation.amount) // validator.total_delegated
    delegator_account.balance += delegator_reward
    delegator_account.reward_history[epoch] += delegator_reward  # Track rewards
```

**Example:**

```
Total Reward: 10 CPC
Validator Commission: 10%
Total Delegated: 100 CPC

Commission to Validator: 1 CPC
Delegators Share: 9 CPC

Delegator A (60 CPC delegated): 5.4 CPC
Delegator B (40 CPC delegated): 3.6 CPC
```

### Reward Address

**Priority:**

1. `val.reward_address` (if set)
2. Address calculated from `val.pq_pub_key` with prefix `cpc`
3. If cannot determine — reward not credited (warning logged)

**By Default:**

When creating validator via `STAKE`:
```python
val.reward_address = tx.from_address  # Sender address
```

## Reward Frequency

### Round-Robin Mechanism

**Block Distribution:**

If there are N active validators in network, each validator produces block every N blocks.

**Example (3 validators):**

```
Block 10: Validator A → receives reward
Block 11: Validator B → receives reward
Block 12: Validator C → receives reward
Block 13: Validator A → receives reward
...
```

**Frequency:**

- Devnet (5 validators): every 5th block
- Testnet (21 validators): every 21st block
- Mainnet (100 validators): every 100th block

### Yield Calculation

**Annual Yield (example for Devnet):**

```
Block Reward = 10 CPC
Block Time = 10 sec
Blocks per Year ≈ 3,153,600
Blocks per Validator per Year ≈ 3,153,600 / 5 = 630,720

Annual Reward ≈ 630,720 * 10 CPC = 6,307,200 CPC
+ Transaction Fees (depends on network activity)
```

**Important:** This is simplified calculation. Actual yield depends on:
- Number of active validators
- Network activity (fees)
- Halving (reward decreases)

## Examples

### Example 1: Simple Block

**Block 15:**

```
Proposer: Validator A
Block Reward: 10 CPC
Transactions: 0
Fees: 0

Total Reward: 10 CPC → validator A's reward_address
```

### Example 2: Block with Transactions

**Block 20:**

```
Proposer: Validator B
Block Reward: 10 CPC
Transactions:
  - TRANSFER (gas_price=1000): fee = 21_000 * 1000 = 21_000_000 wei
  - TRANSFER (gas_price=1000): fee = 21_000 * 1000 = 21_000_000 wei
  - STAKE (gas_price=1000): fee = 40_000 * 1000 = 40_000_000 wei

Fees Total: 82_000_000 wei = 0.000082 CPC

Total Reward: 10.000082 CPC → validator B's reward_address
```

### Example 3: Balance Check

**Before Block:**

```bash
./cpc-cli query balance cpc1alice... --node http://localhost:8000
# Balance: 500.0 CPC
```

**After Block (Validator A produced block):**

```bash
./cpc-cli query balance cpc1alice... --node http://localhost:8000
# Balance: 510.0 CPC (+10 CPC block reward)
```

## Monitoring Rewards

### Check Validator Rewards

```bash
# Get validator's reward_address
./cpc-cli query validators --node http://localhost:8000 | jq '.validators[0].reward_address'

# Check balance
./cpc-cli query balance <REWARD_ADDRESS> --node http://localhost:8000
```

### Check Delegator Rewards

**Query rewards for delegator:**

```bash
# Get reward history for delegator address
./cpc-cli query rewards <DELEGATOR_ADDRESS> --node http://localhost:8000
```

**Example output:**

```
Delegator: cpc1abc...
Current Epoch: 5
Total Rewards: 125.5 CPC

Epoch      Reward Amount
------------------------------
0          25.4
1          24.8
2          25.1
3          25.0
4          25.2
```

### Check Delegations

**View all delegations for address:**

```bash
./cpc-cli query delegations <ADDRESS> --node http://localhost:8000
```

**Example output:**

```
Delegator: cpc1abc...
Total Delegated: 100.0 CPC

Validator                                      Amount          Commission  Name
------------------------------------------------------------------------------------------
cpcvalcons1xyz...                              60.0            10.0%       Validator A
cpcvalcons1def...                              40.0            5.0%        Validator B
```

### Node Logs

**In node logs:**

```
Block 15 added. Hash: 0x1234... (Round 0)
Distributed 1000000000000000000 (commission 10.0%) to validator cpc1alice..., 9000000000000000000 to delegators
```

**Note:** In current implementation, reward logging may be disabled for performance.

## Current Features

### ✅ Implemented:

1. **Delegation & Rewards:**
   - Stakers can delegate tokens to validators
   - Proportional reward distribution to delegators
   - Reward history tracking per epoch

2. **Validator Commission:**
   - Validators can set commission rate (default 10%)
   - Commission is taken before distributing to delegators
   - Transparent commission model

### Future Improvements

**Planned:**

1. **Advanced Slashing:**
   - Additional penalties for incorrect behavior
   - Partial slashing of delegated stakes

2. **Compound Rewards:**
   - Auto-compounding of delegation rewards
   - Reinvestment strategies

## Next Steps

- **[Staking Basics](staking-basic.md)** — Staking basics
- **[Validator Lifecycle](validator-lifecycle.md)** — Validator lifecycle
- **[Node Setup](../node/run-local.md)** — Running validator node
