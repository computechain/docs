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

| Transaction Type | Base Gas Used |
|---------------|-----------|
| TRANSFER | 21,000 |
| STAKE | 40,000 |
| SUBMIT_RESULT | 80,000 |

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
