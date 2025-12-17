# Staking Guide

## Overview

Staking in ComputeChain allows you to:
- **Become a validator** - produce blocks, earn rewards
- **Delegate to validators** - earn passive income
- **Participate in consensus** - secure the network

## Staking (Become Validator)

### Requirements

- **Minimum stake:**
  - Devnet: 1,000 CPC
  - Mainnet: 100,000 CPC
- **Node:** Must run a validator node
- **Uptime:** 75% minimum to stay active

### Stake Tokens

```bash
./cpc-cli tx stake <AMOUNT> --from <KEY_NAME>
```

**Example:**

```bash
# Stake 500 CPC
./cpc-cli tx stake 500 --from mykey
```

**What happens:**
1. Tokens locked from your balance
2. Validator created with `cpcvalcons1...` address
3. Activated in next epoch (after 100 blocks)

### Unstake Tokens

```bash
./cpc-cli tx unstake <AMOUNT> --from <KEY_NAME>
```

**Important:**
- Can unstake partially or fully
- **Unbonding period:**
  - Devnet: 100 blocks (~16 minutes)
  - Mainnet: 21 days
- **Penalty if jailed:** 10% slashed when unstaking while jailed
- Full unstake → validator deactivated
- Tokens automatically returned after unbonding period

## Delegation

### Delegate to Validator

Earn passive rewards by delegating to validators.

**Limits:**
- **Minimum delegation:** 100 CPC
- **Max validators per delegator:** 10
- **Max validator power:** 20% of total voting power

```bash
./cpc-cli tx delegate <VALIDATOR_ADDRESS> <AMOUNT> --from <KEY_NAME>
```

**Example:**

```bash
# Delegate 100 CPC to validator
./cpc-cli tx delegate cpcvalcons1abc... 100 --from mykey
```

### Check Delegations

```bash
./cpc-cli query delegations <YOUR_ADDRESS>
```

**Output:**

```
Delegator: cpc1abc...
Total Delegated: 100.0 CPC

Validator                Amount    Commission  Name
------------------------------------------------------
cpcvalcons1xyz...        60.0      10.0%       Validator A
cpcvalcons1def...        40.0      5.0%        Validator B
```

### Undelegate

```bash
./cpc-cli tx undelegate <VALIDATOR_ADDRESS> <AMOUNT> --from <KEY_NAME>
```

**Important:**
- **Unbonding period:** Same as validators (21 days mainnet / 100 blocks devnet)
- **No penalty:** Delegators are not penalized for undelegating
- **Slashing risk:** If validator is slashed, delegators lose 5% too
- Tokens automatically returned after unbonding period

## Rewards

### How Rewards Work

**Block Reward:** 10 CPC per block (halves every 1M blocks)

**Block Reward Split:**
- **70%** → Validator Pool (block producer)
- **30%** → Miner Pool (PoC workers, currently burned until Phase 2A)

**Transaction Fees Split:**
- **90%** → Validator (block producer)
- **10%** → Treasury (community pool)

**Validator Reward Distribution:**
1. **Validator has delegations:**
   - Validator receives commission (0-20%, configurable)
   - Delegators share remaining amount proportionally
   - Any dust from integer division is burned

2. **No delegations:**
   - Validator receives 100% of their pool

**Example:**

```
Block Reward: 10 CPC
Validator Pool (70%): 7 CPC
Validator Commission: 10%
Total Delegated: 100 CPC

→ Validator: 0.7 CPC (commission)
→ Delegator A (60 CPC): 3.78 CPC
→ Delegator B (40 CPC): 2.52 CPC
```

### Check Rewards

```bash
./cpc-cli query rewards <YOUR_ADDRESS>
```

**Output:**

```
Delegator: cpc1abc...
Total Rewards: 125.5 CPC

Epoch    Reward
------------------
0        25.4 CPC
1        24.8 CPC
2        25.1 CPC
```

### Claim Rewards

Rewards are **auto-credited** to your balance - no manual claim needed!

## Commission

### For Validators

Set your commission rate (0-20%):

```bash
./cpc-cli tx update-validator --commission 0.15 --from mykey
```

**Rules:**
- **Range:** 0% - 20% maximum
- **Cooldown:** 7 days between changes
- **Announce period:** 4 hours before change takes effect
- **Max increase:** +5 percentage points per change

**Example:**
```
Day 0: Commission 5%
Day 7: Announce change to 10% → Effective in 4 hours
Day 14: Can change again (cooldown passed)
```

**Default:** 10%
**Recommended:** 5-15%

### For Delegators

Choose validators with:
- ✅ Low commission (more rewards for you)
- ✅ High uptime (consistent rewards)
- ✅ Good reputation

**Protection:** During the 4-hour announce period, delegators can undelegate without penalty (just the normal 21-day unbonding period).

## Tips

**For Validators:**
- Keep uptime >75% to avoid jailing
- Set reasonable commission (5-15%)
- Update metadata (name, website) for visibility

**For Delegators:**
- Diversify across multiple validators
- Check validator uptime and commission
- Monitor rewards regularly

## Next Steps

- **[Economics](economics.md)** - Complete economic model, tokenomics, and reward distribution
- **[Validator Guide](validator-guide.md)** - Run validator node, manage lifecycle
- **[CLI Reference](cli-reference.md)** - Complete command list
- **[API Reference](api-reference.md)** - Query via RPC
