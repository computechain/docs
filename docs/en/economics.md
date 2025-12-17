# Economic Model & Tokenomics

ComputeChain uses a carefully designed economic model that balances security, decentralization, and sustainability.

## Overview

**Token:** CPC (ComputeChain Coin)
**Decimals:** 18
**Genesis Supply:** 1,000,000,000 CPC (devnet)
**Max Supply:** Infinite (with halving)
**Consensus:** Multi-validator PoA (transitioning to PoC)

---

## Emission Model

### Block Rewards

ComputeChain uses a **halving-based emission model** similar to Bitcoin:

```
Initial Block Reward: 10 CPC
Halving Period: Every 1,000,000 blocks
Formula: reward = initial_reward >> halvings
```

**Inflation Schedule (Devnet @ 10s block time):**

| Period | Blocks | Block Reward | Annual Inflation |
|--------|--------|--------------|------------------|
| Year 1 | 0 - 999,999 | 10 CPC | ~3.15% |
| Year 2+ | 1M - 1.99M | 5 CPC | ~1.58% |
| Year 4+ | 2M - 2.99M | 2.5 CPC | ~0.79% |
| ... | ... | ... | Decreasing |

**Total Supply (asymptotic):**
- Genesis: 1,000,000,000 CPC
- Total minted over time: ~42M CPC (asymptotic)
- Max theoretical supply: ~1,042,000,000 CPC

---

## Block Reward Distribution

Each block reward is split between different network participants:

```
Block Reward: 10 CPC (initial)
├─ 70% (7 CPC)   → Validator Pool
└─ 30% (3 CPC)   → Miner Pool (PoC Workers)
```

### Validator Pool (70%)

Distributed to the block producer (validator who created the block).

**If validator has delegations:**
- **Commission:** Validator takes commission % (max 20%)
- **Delegator Rewards:** Remaining amount distributed proportionally to delegators
- **Dust:** Any remainder from integer division is **burned**

**If no delegations:**
- Validator receives entire pool

**Example:**
```
Block reward: 10 CPC
Validator pool: 7 CPC
Validator commission: 10%

Commission: 0.7 CPC → Validator
Delegator pool: 6.3 CPC → Distributed proportionally
```

### Miner Pool (30%)

Distributed to PoC (Proof-of-Compute) workers who submit valid computation results.

**Distribution:**
- Proportional to **miner weight**
- Weight calculated off-chain: `weight = results * gpu_tier * uptime * difficulty * reputation`
- Verified on-chain via **ZK proof**

**Status:** Infrastructure ready, awaiting Phase 2A PoC implementation.
Until then, unused miner pool is **burned**.

---

## Transaction Fees

Transaction fees are distributed as follows:

```
Total Fees = gas_used * gas_price

├─ 90% → Block Producer (Validator)
├─ 10% → Treasury (Community Pool)
└─ Dust → Burned
```

**Fee Structure:**

| Transaction Type | Base Gas Cost |
|------------------|---------------|
| TRANSFER | 21,000 |
| STAKE | 40,000 |
| UNSTAKE | 40,000 |
| DELEGATE | 35,000 |
| UNDELEGATE | 35,000 |
| UNJAIL | 50,000 |
| UPDATE_VALIDATOR | 30,000 |
| SUBMIT_RESULT (PoC) | 80,000 |

---

## Burn Mechanisms

ComputeChain implements **selective burning** - tokens are only burned when truly necessary:

### What Gets Burned

1. **Slashing Penalties**
   - Validator misbehavior: 5% of total stake (self + delegations)
   - Miner incorrect results: 10% of worker stake
   - All slashed tokens → **BURNED**

2. **Unjail Fee**
   - Early exit from jail: 1,000 CPC → **BURNED**

3. **Unstake Penalty (if jailed)**
   - 10% of self_stake → **BURNED**

4. **Dust from Integer Division**
   - Remainder from reward distribution → **BURNED**

5. **Unused Miner Pool**
   - If no PoC activity in block → **BURNED** (until Phase 2A)

6. **Validator/Miner Cap Excess**
   - If reward exceeds caps → **BURNED**

### Annual Burn Estimate

**Devnet (best case):**
- Fee burn (20%): ~630k CPC/year
- Dust: ~50k CPC/year
- Unused miner pool: ~9.5M CPC/year (until PoC active)
- **Total: ~10M CPC/year**

**Net emission (Phase 1):**
- Minted: ~31.5M CPC/year
- Burned: ~10M CPC/year
- **Net: ~21.5M CPC/year** (~2.15% inflation)

---

## Staking & Delegation

### Validator Staking

**Minimum Stake:**
- Devnet: 1,000 CPC
- Mainnet: 100,000 CPC

**Unstaking:**
- **Unbonding period:** 100 blocks (devnet) / 21 days (mainnet)
- **Penalty if jailed:** 10% of stake burned
- **Automatic return:** Tokens returned after unbonding period

### Delegation

**Minimum Delegation:** 100 CPC

**Limits:**
- **Max validators per delegator:** 10
- **Max validator power:** 20% of total voting power

**Unbonding:**
- **Period:** Same as validators (21 days mainnet)
- **No penalty:** Delegators don't get penalized for undelegating
- **Slashing risk:** If validator is slashed, delegators lose 5% too

**How It Works:**
1. Delegate tokens to validator
2. Validator earns block rewards
3. Commission deducted (e.g., 10%)
4. Remaining rewards distributed proportionally
5. Rewards auto-credited to your balance

---

## Treasury

**Address:** `cpc1treasury000000000000000000000000000000000000000000`

**Funding Sources:**
- 10% of all transaction fees
- Governance proposals can allocate funds

**Purpose:**
- Ecosystem grants
- Development funding
- Marketing & partnerships
- Community initiatives

**Governance:** Initially controlled by core team, transitioning to on-chain governance.

---

## Economic Invariants

The blockchain enforces strict economic invariants:

### 1. Supply Conservation

```
genesis_supply + total_minted - total_burned
= sum(account_balances) + sum(validator_stakes) + sum(delegations) + unbonding_queue + treasury
```

Checked after every block.

### 2. Non-Negative Balances

All account balances must be ≥ 0 at all times.

### 3. Validator Power Cap

No validator can control >20% of total voting power.

### 4. Delegation Consistency

```
validator.total_delegated = sum(validator.delegations)
```

### 5. Reward Distribution Accuracy

```
distributed_rewards ≤ block_reward + fees
dust = (block_reward + fees) - distributed_rewards
dust → burned
```

---

## Miner Weight System (Phase 2A)

ComputeChain uses a sophisticated **ZK-based weight calculation** for PoC workers:

### Weight Formula

```
weight = results_count × gpu_tier × uptime_score × task_difficulty × reputation
```

**Components:**

| Component | Range | Description |
|-----------|-------|-------------|
| `results_count` | 0+ | Number of valid results submitted |
| `gpu_tier` | 0.5 - 4.5x | GPU multiplier (RTX 4080: 1.3x, H100: 4.0x, H200: 4.5x) |
| `uptime_score` | 0.0 - 1.0 | Reliability score (tasks completed / assigned) |
| `task_difficulty` | 1.0 - 6.0 | Task complexity multiplier |
| `reputation` | 0.0 - 1.0 | Historical performance score |

### GPU Tier Multipliers

| GPU | Tier | Description |
|-----|------|-------------|
| RTX 4070 | 1.0x | Baseline consumer GPU |
| RTX 4080 | 1.3x | +30% |
| RTX 4090 | 1.6x | +60% |
| RTX A6000 | 2.0x | Professional GPU |
| A100 40GB | 2.5x | Data center |
| A100 80GB | 3.0x | High-memory |
| H100 | 4.0x | Latest gen |
| H200 | 4.5x | Highest tier |

### ZK Proof Architecture

**Off-chain (Miner):**
1. Calculate weight using formula
2. Generate ZK proof of honest calculation
3. Sign (weight + proof) with private key
4. Submit to blockchain

**On-chain (Blockchain):**
1. Verify signature (authenticity)
2. Verify ZK proof (honest calculation)
3. Check bounds (min/max weight)
4. Distribute rewards proportionally

**Benefits:**
- ✅ Privacy-preserving (GPU specs not revealed)
- ✅ Cryptographically secure (cannot fake weight)
- ✅ Fast verification (no formula execution on-chain)
- ✅ Upgradable (formula can change without hard fork)

---

## Commission & Validator Economics

### Commission Rates

**Range:** 0% - 20%

**Change Rules:**
- **Cooldown:** 7 days between changes
- **Announce period:** 4 hours before effective
- **Max increase:** +5 percentage points per change

**Example:**
```
Day 0: Commission 5%
Day 7: Announce change to 10% → Effective in 4 hours
Day 14: Can change again (cooldown passed)
```

**Delegator Protection:**
During announce period, delegators can undelegate without penalty (just 21-day unbonding).

---

## Economic Parameters

All economic parameters are centralized in `protocol/config/economic_model.py`:

```python
DEVNET = EconomicConfig(
    initial_block_reward=10 * DECIMALS,
    halving_period_blocks=1_000_000,

    validator_reward_share=0.70,  # 70%
    miner_reward_share=0.30,      # 30%

    validator_fee_share=0.90,     # 90%
    treasury_fee_share=0.10,      # 10%

    max_validator_power_share=0.20,  # 20%
    max_commission_rate=0.20,        # 20%

    validator_slashing_rate=0.05,    # 5%
    miner_slashing_rate=0.10,        # 10%

    unjail_fee=1_000 * DECIMALS,     # 1000 CPC
    unstake_penalty_rate=0.10,       # 10%

    ...
)
```

**Networks:** DEVNET, TESTNET, MAINNET

---

## Summary

**ComputeChain Economic Model:**

✅ **Sustainable:** Halving-based emission with selective burning
✅ **Decentralized:** 20% power cap, max 10 validators per delegator
✅ **Secure:** Slashing for misbehavior, delegators at risk too
✅ **Fair:** ZK-based miner weights, GPU-tier adjusted rewards
✅ **Transparent:** All parameters in one config file
✅ **Verifiable:** Economic invariants checked every block

**Status:**
- Phase 1.2: Economic Model ✅ **COMPLETE**
- Phase 2A: PoC Integration ⏳ Ready to implement

---

## Further Reading

- [Staking Guide](staking-guide.md) - How to stake and delegate
- [Validator Guide](validator-guide.md) - Running a validator node
- [API Reference](api-reference.md) - Query economic metrics
- [Advanced Topics](advanced.md) - Deep dive into consensus

---

**Last Updated:** December 17, 2025
**Economic Model Version:** v2.0
**Implementation:** Phase 1.2 Complete
