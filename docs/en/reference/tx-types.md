# Transaction Types

Reference guide for transaction types in ComputeChain.

## TRANSFER

**Type:** `TxType.TRANSFER`

**Purpose:** Transfer CPC tokens between accounts

**Gas Cost:** 21,000 gas

**Structure:**

```python
Transaction(
    tx_type=TxType.TRANSFER,
    from_address="cpc1sender...",
    to_address="cpc1recipient...",
    amount=100 * 10**18,  # 100 CPC (in wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=21000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Required Fields:**

- `from_address`: Sender address (cpc1...)
- `to_address`: Recipient address (cpc1...)
- `amount`: Transfer amount (in wei, minimum 0)
- `nonce`: Sender transaction number
- `pub_key`: Sender public key

**Validation:**

- Sender balance >= amount + fee
- Nonce must be next in sequence
- Signature must be valid
- `to_address` must not be empty

**Example:**

```bash
./cpc-cli tx send cpc1recipient... 100 --from alice
```

## STAKE

**Type:** `TxType.STAKE`

**Purpose:** Become validator or increase stake

**Gas Cost:** 40,000 gas

**Structure:**

```python
Transaction(
    tx_type=TxType.STAKE,
    from_address="cpc1sender...",
    to_address=None,
    amount=1500 * 10**18,  # 1500 CPC (in wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=40000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={
        "pub_key": "02a1b2c3..."  # Validator public key (required!)
    }
)
```

**Required Fields:**

- `from_address`: Sender address (cpc1...)
- `amount`: Stake amount (in wei). For a new validator it must be at least `min_validator_stake`.
- `payload.pub_key`: Validator public key (hex string)

**Validation:**

- Sender balance >= amount + fee
- For new validators: `amount >= min_validator_stake`
- For existing validators: `amount > 0`
- `pub_key` must be present in payload
- Signature must be valid

**Result:**

- Creates or updates validator with address `cpcvalcons...` (calculated from `pub_key`)
- Stake added to existing (if validator already exists)
- `reward_address` set to `from_address` (if new validator)

**Example:**

```bash
./cpc-cli tx stake 1500 --from alice
```

## UNSTAKE

**Type:** `TxType.UNSTAKE`

**Purpose:** Withdraw staked tokens from validator

**Gas Cost:** 40,000 gas

**Structure:**

```python
Transaction(
    tx_type=TxType.UNSTAKE,
    from_address="cpc1sender...",
    to_address=None,
    amount=500 * 10**18,  # Amount to unstake (in wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=40000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Required Fields:**

- `from_address`: Validator owner address (cpc1...)
- `amount`: Amount to unstake (in wei, must be > 0)
- `nonce`: Sender transaction number
- `pub_key`: Sender public key

**Validation:**

- Validator must exist
- Validator power >= amount
- Sender balance >= fee
- Signature must be valid

**Penalty:**

- Normal unstake: 0% penalty
- Unstake while jailed: **10% penalty** (burned)

**Result:**

- Tokens returned to sender (minus penalty if jailed)
- Validator power reduced by amount
- If power becomes 0: validator deactivated (`is_active = False`)

**Example:**

```bash
python3 -m cli.main tx unstake 500 --from validator1
```

## UPDATE_VALIDATOR

**Type:** `TxType.UPDATE_VALIDATOR`

**Purpose:** Update validator metadata (name, website, commission)

**Gas Cost:** 30,000 gas

**Structure:**

```python
Transaction(
    tx_type=TxType.UPDATE_VALIDATOR,
    from_address="cpc1owner...",
    to_address=None,
    amount=0,
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=30000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={
        "name": "MyPool",  # Optional, max 64 chars
        "website": "https://pool.com",  # Optional, max 128 chars
        "description": "Best validator pool",  # Optional, max 256 chars
        "commission_rate": 0.15  # Optional, 0.0-1.0 (15%)
    }
)
```

**Required Fields:**

- `from_address`: Validator owner address (cpc1...)
- At least one metadata field in payload

**Optional Payload Fields:**

- `name`: Human-readable name (max 64 characters)
- `website`: Website URL (max 128 characters)
- `description`: Description (max 256 characters)
- `commission_rate`: Commission rate (0.0-1.0, max 0.20 = 20%)

**Validation:**

- Validator must exist
- Only validator owner can update
- Field length limits enforced
- commission_rate must be 0.0-1.0
- Signature must be valid

**Result:**

- Validator metadata updated in state
- Visible in dashboard and RPC queries

**Example:**

```bash
python3 -m cli.main tx update-validator \
  --name "MyPool" \
  --website "https://pool.com" \
  --commission 0.15 \
  --from validator1
```

## DELEGATE

**Type:** `TxType.DELEGATE`

**Purpose:** Delegate tokens to a validator

**Gas Cost:** 35,000 gas

**Structure:**

```python
Transaction(
    tx_type=TxType.DELEGATE,
    from_address="cpc1delegator...",
    to_address="cpcvalcons1validator...",  # Validator consensus address
    amount=500 * 10**18,  # Delegation amount (in wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=35000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Required Fields:**

- `from_address`: Delegator address (cpc1...)
- `to_address`: Validator consensus address (cpcvalcons...)
- `amount`: Delegation amount (in wei, minimum 100 CPC)
- `nonce`: Sender transaction number
- `pub_key`: Sender public key

**Validation:**

- Validator must exist and be active
- amount >= min_delegation (100 CPC)
- Delegator balance >= amount + fee
- Signature must be valid

**Result:**

- Tokens transferred from delegator to validator
- Validator `total_delegated` increased
- Validator `power` increased
- Delegator eligible for commission-based rewards

**Example:**

```bash
python3 -m cli.main tx delegate cpcvalcons1abc... 500 --from delegator
```

## UNDELEGATE

**Type:** `TxType.UNDELEGATE`

**Purpose:** Withdraw delegated tokens from validator

**Gas Cost:** 35,000 gas

**Structure:**

```python
Transaction(
    tx_type=TxType.UNDELEGATE,
    from_address="cpc1delegator...",
    to_address="cpcvalcons1validator...",  # Validator consensus address
    amount=200 * 10**18,  # Amount to undelegate (in wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=35000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Required Fields:**

- `from_address`: Delegator address (cpc1...)
- `to_address`: Validator consensus address (cpcvalcons...)
- `amount`: Amount to undelegate (in wei, must be > 0)
- `nonce`: Sender transaction number
- `pub_key`: Sender public key

**Validation:**

- Validator must exist
- Validator total_delegated >= amount
- Delegator balance >= fee
- Signature must be valid

**Result:**

- Tokens returned to delegator
- Validator `total_delegated` decreased
- Validator `power` decreased

**Example:**

```bash
python3 -m cli.main tx undelegate cpcvalcons1abc... 200 --from delegator
```

## UNJAIL

**Type:** `TxType.UNJAIL`

**Purpose:** Early release from jail (pay fee to exit jail before scheduled release)

**Gas Cost:** 50,000 gas

**Fee:** 1,000 CPC (burned) + gas fee

**Structure:**

```python
Transaction(
    tx_type=TxType.UNJAIL,
    from_address="cpc1validator...",
    to_address=None,
    amount=1000 * 10**18,  # Unjail fee: 1000 CPC (burned)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=50000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Required Fields:**

- `from_address`: Validator owner address (cpc1...)
- `amount`: Must be exactly 1,000 CPC (unjail fee)
- `nonce`: Sender transaction number
- `pub_key`: Sender public key

**Validation:**

- Validator must exist
- Validator must be jailed (`jailed_until_height > 0`)
- amount must be exactly 1,000 CPC
- Sender balance >= 1,000 CPC + gas fee
- Signature must be valid

**Result:**

- 1,000 CPC burned (removed from circulation)
- Validator released from jail:
  - `jailed_until_height = 0`
  - `missed_blocks = 0`
  - `is_active = True`
- Validator can participate in next epoch

**Example:**

```bash
python3 -m cli.main tx unjail --from validator1
```

**Cost Breakdown:**

```
Unjail Fee: 1,000 CPC (burned)
Gas Fee: 50,000 * 1,000 wei = 0.00005 CPC
Total: ~1,000.00005 CPC
```

## SUBMIT_RESULT

**Type:** `TxType.SUBMIT_RESULT`

**Purpose:** Submit compute task execution result

**Gas Cost:** 80,000 gas

**Structure:**

```python
Transaction(
    tx_type=TxType.SUBMIT_RESULT,
    from_address="cpc1worker...",
    to_address=None,
    amount=0,  # Reward not yet integrated in L1
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=80000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={
        "task_id": "550e8400-e29b-41d4-a716-446655440000",
        "worker_address": "cpc1worker...",
        "result_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
        "proof": None,  # Optional (future: ZK-proof)
        "nonce": 12345,  # Optional (for synthetic tasks)
        "signature": ""  # Optional
    }
)
```

**Required Fields:**

- `from_address`: Worker address (cpc1...)
- `payload.task_id`: Task UUID
- `payload.worker_address`: Worker address (must match `from_address`)
- `payload.result_hash`: Computation result hash (hex string)

**Optional Fields:**

- `payload.proof`: Correctness proof (future: ZK-proof)
- `payload.nonce`: Nonce for synthetic tasks
- `payload.signature`: Worker-level signature (currently informational)

**Validation:**

- `ComputeResult` structure must be valid
- `worker_address` must match `tx.from_address`
- Proof verification and `payload.signature` checks are planned for future releases

**Result:**

- Result included in block
- `compute_root` updated in block header
- Reward not yet integrated in L1 (planned)

**Example:**

```bash
./cpc-cli tx submit-result \
  --task-id "550e8400-e29b-41d4-a716-446655440000" \
  --result-hash "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd" \
  --from worker
```

## Common Transaction Fields

### Required Fields

- `tx_type`: Transaction type (enum)
- `from_address`: Sender address (cpc1...)
- `amount`: Amount (in wei)
- `fee`: Fee (gas_used * gas_price)
- `nonce`: Sender transaction number
- `gas_price`: Gas price (wei per gas)
- `gas_limit`: Gas limit
- `timestamp`: Timestamp (Unix timestamp)
- `pub_key`: Sender public key (hex string)
- `signature`: Transaction signature (hex string)

### Optional Fields

- `to_address`: Recipient address (for TRANSFER)
- `payload`: Additional data (dict)

## Limits

### Base Gas per Transaction Type

| Transaction Type | Base Gas Used | Additional Fees |
|---------------|-----------|-----------------|
| TRANSFER | 21,000 | - |
| STAKE | 40,000 | - |
| UNSTAKE | 40,000 | 10% penalty if jailed |
| UPDATE_VALIDATOR | 30,000 | - |
| DELEGATE | 35,000 | - |
| UNDELEGATE | 35,000 | - |
| UNJAIL | 50,000 | +1,000 CPC (burned) |
| SUBMIT_RESULT | 80,000 | - |

`gas_limit` supplied in a transaction must be at least the base value for its type.

**Block:**

- Devnet: 10,000,000 gas
- Testnet: 15,000,000 gas
- Mainnet: 30,000,000 gas

*(Network-level limits above are part of planned configurations; always check `protocol/config/params.py` in your build for authoritative values.)*

### Minimum Values

**Gas Price:**

- Devnet: 1,000 wei
- Testnet: 5,000 wei
- Mainnet: 1,000,000,000 wei (1 Gwei)

**Amount:**

- Minimum: 0 wei
- For STAKE: minimum `min_validator_stake`

## Invariants

### Nonce

- Nonce must be sequential
- Starts at 0 for new account
- Increases by 1 for each transaction

### Balance

- Sender balance >= amount + fee
- Balance cannot be negative

### Signature

- Signature must be valid for `from_address`
- Uses ECDSA (secp256k1) in MVP
- Planned transition to Post-Quantum signatures

## Next Steps

- **[RPC API](rpc.md)** — RPC endpoints
- **[Glossary](glossary.md)** — Terminology
- **[Staking](../staking/staking-basic.md)** — How to become a validator
