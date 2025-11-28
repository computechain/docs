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

**Code:**

```python
def _distribute_rewards(self, block: Block, state: AccountState):
    proposer_addr = block.header.proposer_address
    val = state.get_validator(proposer_addr)
    
    if not val or not val.is_active:
        return  # Validator not active
    
    # Determine reward address
    target_addr = val.reward_address
    if not target_addr:
        # Fallback: derive from pub_key
        target_addr = address_from_pubkey(
            bytes.fromhex(val.pq_pub_key), 
            prefix="cpc"
        )
    
    acc = state.get_account(target_addr)
    
    # Calculate reward
    block_reward = calculate_block_reward(block.header.height)
    fees_total = sum(GAS_PER_TYPE.get(tx.tx_type, 0) * tx.gas_price for tx in block.txs)
    total_amount = block_reward + fees_total
    
    # Credit
    acc.balance += total_amount
    state.set_account(acc)
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

### Check reward_address Balance

```bash
# Get validator's reward_address
./cpc-cli query validators --node http://localhost:8000 | jq '.validators[0].reward_address'

# Check balance
./cpc-cli query balance <REWARD_ADDRESS> --node http://localhost:8000
```

### Node Logs

**In node logs:**

```
Block 15 added. Hash: 0x1234... (Round 0)
Distributed 10000000000000000000 (Reward: 10000000000000000000, Fees: 0) to cpc1alice...
```

**Note:** In current implementation, reward logging may be disabled for performance.

## Future Improvements

### Planned:

1. **Delegation:**
   - Stakers can delegate tokens to validators
   - Rewards distributed between validator and delegates

2. **Slashing:**
   - Penalties for incorrect behavior
   - Part of stake may be slashed

3. **Validator Commission:**
   - Validator can set commission (e.g., 10%)
   - Remaining rewards go to delegates

## Next Steps

- **[Staking Basics](staking-basic.md)** — Staking basics
- **[Validator Lifecycle](validator-lifecycle.md)** — Validator lifecycle
- **[Node Setup](../node/run-local.md)** — Running validator node
