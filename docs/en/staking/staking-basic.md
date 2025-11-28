# Staking Basics

Staking allows you to become a validator in the ComputeChain network and participate in consensus.

## Requirements

### Minimum Stake

**By Network:**

| Network | Minimum Initial Stake |
|---------|---------------|
| Devnet | 1,000 CPC |
| Testnet | 100,000 CPC |
| Mainnet | 100,000 CPC |

### Maximum Validators

| Network | Maximum Validators |
|---------|-------------------|
| Devnet | 5 |
| Testnet | 21 |
| Mainnet | 100 |

## STAKE Transaction

### Transaction Structure

**Type:** `TxType.STAKE`

**Fields:**

```python
Transaction(
    tx_type=TxType.STAKE,
    from_address="cpc1...",  # Sender address
    to_address=None,  # Not used for staking
    amount=1500 * 10**18,  # Stake amount (in wei)
    fee=gas_limit * gas_price,
    nonce=...,
    gas_price=1000,
    gas_limit=40000,  # GAS_PER_TYPE[STAKE]
    payload={
        "pub_key": "02a1b2c3..."  # Validator public key (required!)
    }
)
```

### Required Fields

**`pub_key` in payload:**

- Validator public key (hex string)
- Used to generate consensus address (`cpcvalcons...`)
- Transaction will be rejected without `pub_key`

**Automatic Filling:**

CLI automatically takes public key from keystore:

```python
# In cmd_tx_stake
pub_key_hex = sender_key['public_key']
tx.payload = {"pub_key": pub_key_hex}
```

## Staking Process

### Step 1: Create Key

```bash
./cpc-cli keys add alice
```

### Step 2: Fund Account

```bash
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000
```

**Important:** Balance must cover:
- Stake amount (minimum 1,000 CPC for devnet when creating a new validator)
- Transaction fee (~40,000 gas * gas_price)

### Step 3: Send STAKE Transaction

```bash
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000
```

**What happens:**

1. CLI creates `STAKE` transaction
2. Automatically adds `pub_key` from keystore
3. Calculates `gas_limit` (40,000) and `fee`
4. Signs transaction
5. Sends to mempool via RPC `/tx/send`

### Step 4: Wait for Block Inclusion

**Wait Time:**

- Devnet: ~10 seconds (1 block)
- After inclusion, validator is created but not yet active

### Step 5: Validator Activation

**Epoch:**

- Devnet: every 10 blocks (~100 seconds)
- Testnet: every 100 blocks (~50 minutes)
- Mainnet: every 72 blocks (~72 minutes)

**What happens in epoch:**

1. Validator set recalculation
2. Sort by stake (descending)
3. Select top-N validators (N = max_validators)
4. Activate validators (`is_active = True`)
5. Deactivate validators outside top-N

**Check Status:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

## Increasing Stake

### Adding to Existing Stake

**Simply send another STAKE transaction:**

```bash
./cpc-cli tx stake 500 --from alice --node http://localhost:8000
```

**What happens:**

- If validator with such `pub_key` already exists, stake is added
- `val.power += tx.amount`
- Validator remains in set (if was active)

**Note:** `min_validator_stake` applies only to the first STAKE (validator creation). Subsequent STAKE transactions can use any positive amount to increase existing stake.
## Reward Address

### Setting Reward Address

**By Default:**

- `reward_address` is set to `tx.from_address` (sender address)
- Block rewards go to this address

**Change (Future):**

Planned ability to change `reward_address` via separate transaction.

## Gas Costs

### STAKE Fee

**Gas Cost:** 40,000 gas

**Calculation Example:**

```python
gas_limit = 40_000
gas_price = 1_000  # Devnet
fee = 40_000 * 1_000 = 40_000_000 wei = 0.00004 CPC
```

**Minimum Balance for Staking:**

```
Minimum Stake + Fee + Buffer
= 1,000 CPC + 0.00004 CPC + ~1 CPC
≈ 1,001 CPC
```

## Examples

### Full Scenario (Node B)

```bash
# 1. Import faucet key from Node A
./cpc-cli keys import faucet --private-key $(cat .node_a/faucet_key.hex)

# 2. Create Alice
./cpc-cli keys add alice

# 3. Get Alice address
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 4. Fund account
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000

# 5. Stake
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000

# 6. Wait for epoch (10 blocks)
sleep 120

# 7. Check status
./cpc-cli query validators --node http://localhost:8000
```

## Next Steps

- **[Validator Lifecycle](validator-lifecycle.md)** — Validator lifecycle
- **[Rewards](rewards.md)** — Validation rewards
- **[Node Setup](../node/run-local.md)** — Running validator node
