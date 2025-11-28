# Validator Lifecycle

## Validator Life Stages

### 1. Creation

**Trigger:** `STAKE` transaction with sufficient amount

**Conditions:**

- `tx.amount >= min_validator_stake`
- `pub_key` present in payload
- Sender balance is sufficient

**What happens:**

```python
# In State.apply_transaction
val_addr = address_from_pubkey(pub_key_bytes, prefix="cpcvalcons")
val = Validator(
    address=val_addr,
    pq_pub_key=pub_key_hex,
    power=tx.amount,
    is_active=False,  # Not active yet!
    reward_address=tx.from_address
)
```

**Status:** `is_active = False`

### 2. Pending

**Period:** Until next epoch

**What happens:**

- Validator created but not participating in consensus
- Cannot produce blocks
- Does not receive rewards

**Check:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

**Output:**

```json
{
  "epoch": 1,
  "validators": [
    {
      "address": "cpcvalcons1...",
      "power": "1500000000000000000000",
      "is_active": false,  // ← Not active yet
      "reward_address": "cpc1..."
    }
  ]
}
```

### 3. Activation

**Trigger:** Epoch transition (every N blocks)

**Process:**

1. **Collect all validators:**
   ```python
   all_validators = state.get_all_validators()
   ```

2. **Filter by minimum stake:**
   ```python
   active_candidates = [v for v in all_validators if v.power >= min_validator_stake]
   ```

3. **Sort by stake (descending):**
   ```python
   sorted_validators = sorted(active_candidates, key=lambda v: v.power, reverse=True)
   ```

4. **Select top-N:**
   ```python
   top_validators = sorted_validators[:max_validators]
   ```

5. **Activate:**
   ```python
   for val in top_validators:
       val.is_active = True
   ```

6. **Deactivate others:**
   ```python
   for val in all_validators:
       if val not in top_validators:
           val.is_active = False
   ```

**Status:** `is_active = True`

### 4. Active Validation

**Period:** While validator is in top-N

**What happens:**

- Participates in consensus (Round-Robin)
- Can produce blocks in its slot
- Receives block rewards and fees

**Round-Robin:**

```python
def get_proposer(height: int) -> Validator:
    active_validators = [v for v in validators if v.is_active]
    index = height % len(active_validators)
    return active_validators[index]
```

**Example:**

```
Block 10: Validator A (index 0)
Block 11: Validator B (index 1)
Block 12: Validator C (index 2)
Block 13: Validator A (index 0)  # Cycle repeats
```

### 5. Deactivation

**Reasons:**

1. **Insufficient stake:**
   - Validator fell below `min_validator_stake`
   - Or other validators overtook by stake

2. **Displacement from top-N:**
   - Validators with larger stake appeared
   - Validator dropped out of top-N

**What happens:**

```python
val.is_active = False
```

**Consequences:**

- Stops producing blocks
- Does not receive rewards
- Can be reactivated in next epoch (if returns to top-N)

### 6. Re-staking

**Trigger:** New `STAKE` transaction with same `pub_key`

**What happens:**

```python
val = get_validator(val_addr)
if val:
    val.power += tx.amount  # Added to existing stake
```

**Result:**

- Increased position in ranking
- Better chance to stay in top-N
- More rewards (if active)

## Epoch

### Definition

**Epoch** — period between validator set recalculations.

**Length:**

| Network | Blocks | Time (approx.) |
|---------|--------|----------------|
| Devnet | 10 | ~100 sec |
| Testnet | 100 | ~50 min |
| Mainnet | 72 | ~72 min |

### Epoch Transition

**Trigger:**

```python
if (block.header.height + 1) % config.epoch_length_blocks == 0:
    _update_consensus_from_state()
```

**What happens:**

1. Validator set recalculation
2. Activation/deactivation
3. Update `ConsensusEngine.validator_set`

## Example Scenarios

### Scenario 1: Becoming a Validator

```
Block 0:  Alice sends STAKE(1500 CPC)
Block 1:  Transaction included, validator created (is_active=False)
Block 2-9: Waiting for epoch
Block 10: Epoch! Alice activates (is_active=True)
Block 11: Alice produces first block (Round-Robin)
```

### Scenario 2: Displacement from Top-N

```
Epoch 1: Top-5: [A:2000, B:1800, C:1500, D:1200, E:1000]
         Alice (1500) — active

Epoch 2: Top-5: [A:2000, B:1800, C:1500, F:1400, D:1200]
         Alice (1500) — still active

Epoch 3: Top-5: [A:2000, B:1800, G:1600, C:1500, F:1400]
         Alice (1500) — deactivated (displaced by G)
```

### Scenario 3: Return to Top-N

```
Epoch 1: Alice deactivated (6th by stake)
Epoch 1: Alice sends STAKE(+500 CPC)
Epoch 2: Alice returns to top-5, activates
```

## Monitoring

### Check Validator Status

```bash
./cpc-cli query validators --node http://localhost:8000
```

**Output:**

```json
{
  "epoch": 2,
  "validators": [
    {
      "address": "cpcvalcons1alice...",
      "pq_pub_key": "02a1b2c3...",
      "power": "1500000000000000000000",
      "is_active": true,
      "reward_address": "cpc1alice..."
    },
    {
      "address": "cpcvalcons1bob...",
      "pq_pub_key": "02b2c3d4...",
      "power": "1200000000000000000000",
      "is_active": true,
      "reward_address": "cpc1bob..."
    }
  ]
}
```

### Check Current Proposer

```bash
# Via node status
curl http://localhost:8000/status
```

**Output:**

```json
{
  "height": 15,
  "last_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```

**Proposer calculation:**

```python
height = 15
epoch = height // 10  # = 1
active_validators = get_active_validators()
proposer_index = height % len(active_validators)
proposer = active_validators[proposer_index]
```

## Next Steps

- **[Staking Basics](staking-basic.md)** — Staking basics
- **[Rewards](rewards.md)** — Validation rewards
- **[Node Setup](../node/run-local.md)** — Running validator node
