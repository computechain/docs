# Staking Guide

## Overview

Staking in ComputeChain allows you to:
- **Become a validator** - produce blocks, earn rewards
- **Delegate to validators** - earn passive income
- **Participate in consensus** - secure the network

## Staking (Become Validator)

### Requirements

- **Minimum stake:** 100 CPC
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
- **Penalty if jailed:** 10% slashed when unstaking while jailed
- Full unstake → validator deactivated

## Delegation

### Delegate to Validator

Earn passive rewards by delegating to validators.

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

## Rewards

### How Rewards Work

**Block Reward:** 10 CPC per block (halves every 1M blocks)

**Distribution:**
1. **Validator has delegations:**
   - Validator receives commission (default 10%)
   - Delegators share remaining 90% proportionally

2. **No delegations:**
   - Validator receives 100%

**Example:**

```
Block Reward: 10 CPC
Validator Commission: 10%
Total Delegated: 100 CPC

→ Validator: 1 CPC (commission)
→ Delegator A (60 CPC): 5.4 CPC
→ Delegator B (40 CPC): 3.6 CPC
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

Set your commission rate (0-100%):

```bash
./cpc-cli tx update-validator --commission 0.15 --from mykey
```

**Default:** 10%
**Recommended:** 5-15%

### For Delegators

Choose validators with:
- ✅ Low commission (more rewards for you)
- ✅ High uptime (consistent rewards)
- ✅ Good reputation

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

- **[Validator Guide](validator-guide.md)** - Run validator node, manage lifecycle
- **[CLI Reference](cli-reference.md)** - Complete command list
- **[API Reference](api-reference.md)** - Query via RPC
