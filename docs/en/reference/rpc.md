# RPC API Reference

Reference guide for ComputeChain node RPC endpoints.

## Base URL

**Default:** `http://localhost:8000`

**Change:** Use `--port` parameter when starting node

## Endpoints

### GET /status

**Purpose:** Get node status

**Request:**

```bash
curl http://localhost:8000/status
```

**Response:**

```json
{
  "height": 15,
  "last_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```
- PQ-specific header fields (e.g., `pq_signature`, `pq_pub_key`) are reserved for future versions and may be absent in the current MVP. Blocks are currently signed via ECDSA (`signature` + `pub_key`).

**Fields:**

- `height`: Last block height
- `last_hash`: Last block hash (hex string)
- `network`: Network ID ("devnet", "testnet", "mainnet")
- `mempool_size`: Number of transactions in mempool
- `epoch`: Current epoch

### GET /block/{height}

**Purpose:** Get block by height

**Request:**

```bash
curl http://localhost:8000/block/10
```

**Response:**

```json
{
  "header": {
    "height": 10,
    "prev_hash": "abcd1234ef...",
    "timestamp": 1700000000,
    "proposer_address": "cpcvalcons1...",
    "compute_root": "7890abcd...",
    "tx_root": "4567efgh...",
    "state_root": "cdef1234...",
    "signature": "feedfacecafebeef...",   // ECDSA in MVP
    "pub_key": "02..."
  },
  "txs": [
    {
      "tx_type": "TRANSFER",
      "from_address": "cpc1...",
      "to_address": "cpc1...",
      "amount": "100000000000000000000",
      ...
    }
  ]
}
```

**Errors:**

- `404`: Block not found
- `503`: Node not initialized

### GET /balance/{address}

**Purpose:** Get account balance and nonce

**Request:**

```bash
curl http://localhost:8000/balance/cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

**Response:**

```json
{
  "address": "cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
  "balance": "2000000000000000000000",
  "nonce": 1
}
```

**Fields:**

- `address`: Account address
- `balance`: Balance in wei (string)
- `nonce`: Next transaction number

**Errors:**

- `503`: Node not initialized

### GET /validators

**Purpose:** Get validator list

**Request:**

```bash
curl http://localhost:8000/validators
```

**Response:**

```json
{
  "epoch": 1,
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

**Fields:**

- `epoch`: Current epoch
- `validators`: Validator list
  - `address`: Validator consensus address (cpcvalcons...)
  - `pq_pub_key`: Validator public key (currently contains ECDSA key; named for future PQ migration)
  - `power`: Validator stake (in wei, string)
  - `is_active`: Whether validator is active
  - `reward_address`: Address for receiving rewards (cpc1...)

**Errors:**

- `503`: Node not initialized

### GET /delegator/{address}/delegations

**Purpose:** Get all delegations for a delegator address

**Request:**

```bash
curl http://localhost:8000/delegator/cpc1abc.../delegations
```

**Response:**

```json
{
  "delegator": "cpc1abc...",
  "delegations": [
    {
      "validator": "cpcvalcons1xyz...",
      "amount": 60000000,
      "created_height": 100,
      "validator_name": "Validator A",
      "validator_commission": 0.10
    },
    {
      "validator": "cpcvalcons1def...",
      "amount": 40000000,
      "created_height": 150,
      "validator_name": "Validator B",
      "validator_commission": 0.05
    }
  ],
  "total_delegated": 100000000
}
```

**Fields:**

- `delegator`: Delegator address
- `delegations`: Array of delegations
  - `validator`: Validator consensus address
  - `amount`: Delegated amount (in base units)
  - `created_height`: Block height when delegation was created
  - `validator_name`: Validator name (if set)
  - `validator_commission`: Validator commission rate (0.0-1.0)
- `total_delegated`: Total amount delegated

**Errors:**

- `503`: Node not initialized

### GET /delegator/{address}/rewards

**Purpose:** Get reward history for a delegator address

**Request:**

```bash
curl http://localhost:8000/delegator/cpc1abc.../rewards
```

**Response:**

```json
{
  "delegator": "cpc1abc...",
  "total_rewards": 125500000,
  "rewards_by_epoch": [
    {
      "epoch": 0,
      "amount": 25400000
    },
    {
      "epoch": 1,
      "amount": 24800000
    },
    {
      "epoch": 2,
      "amount": 25100000
    },
    {
      "epoch": 3,
      "amount": 25000000
    },
    {
      "epoch": 4,
      "amount": 25200000
    }
  ],
  "current_epoch": 5
}
```

**Fields:**

- `delegator`: Delegator address
- `total_rewards`: Total rewards earned (in base units)
- `rewards_by_epoch`: Array of rewards per epoch
  - `epoch`: Epoch number
  - `amount`: Reward amount for that epoch (in base units)
- `current_epoch`: Current epoch number

**Errors:**

- `503`: Node not initialized

### POST /tx/send

**Purpose:** Send transaction to mempool

**Request:**

```bash
curl -X POST http://localhost:8000/tx/send \
  -H "Content-Type: application/json" \
  -d '{
    "tx_type": "TRANSFER",
    "from_address": "cpc1sender...",
    "to_address": "cpc1recipient...",
    "amount": "100000000000000000000",
    "fee": "21000000",
    "nonce": 1,
    "gas_price": 1000,
    "gas_limit": 21000,
    "timestamp": 1700000000,
    "pub_key": "02a1b2c3...",
    "signature": "abcdef1234...",
    "payload": {}
  }'
```
`amount` and `fee` must be decimal strings in wei. `gas_price`, `gas_limit`, `nonce`, and `timestamp` are integers.

**Response (success):**

```json
{
  "tx_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
  "status": "received"
}
```

**Response (rejected):**

```json
{
  "tx_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
  "status": "rejected",
  "error": "Insufficient balance"
}
```

**Response Fields:**

- `tx_hash`: Transaction hash (hex string)
- `status`: Status ("received" or "rejected")
- `error`: Error message (if rejected)

**Errors:**

- `400`: Invalid transaction format
- `503`: Node not initialized

## Data Formats

### Addresses

**Format:** Bech32 with prefix

- Accounts: `cpc1...`
- Validators: `cpcvalcons1...`

**Examples:**

```
cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
cpcvalcons1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

### Amounts

**Format:** String with number in wei (used in RPC to avoid float precision issues)

**Examples:**

```
"100000000000000000000"  # 100 CPC
"1500000000000000000000"  # 1500 CPC
```

### Hashes

**Format:** Hex string without prefix

**Examples:**

```
"1234567890abcdef..."
"abcdef1234567890..."
```

### Public Keys

**Format:** Hex string without prefix

**Examples:**

```
"02a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
```

## Error Codes

### 200 OK

Successful request

### 400 Bad Request

Invalid request format or data

**Example:**

```json
{
  "detail": "Invalid transaction format"
}
```

### 404 Not Found

Resource not found

**Example:**

```json
{
  "detail": "Block not found"
}
```

### 503 Service Unavailable

Node not initialized

**Example:**

```json
{
  "detail": "Node not initialized"
}
```

## Usage Examples

### Example 1: Check Status

```bash
curl http://localhost:8000/status | jq
```

### Example 2: Get Balance

```bash
ADDRESS="cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t"
curl http://localhost:8000/balance/$ADDRESS | jq
```

### Example 3: Get Block

```bash
HEIGHT=10
curl http://localhost:8000/block/$HEIGHT | jq '.header'
```

### Example 4: Get Validators

```bash
curl http://localhost:8000/validators | jq '.validators[] | select(.is_active == true)'
```

### Example 5: Send Transaction (via CLI)

```bash
./cpc-cli tx send cpc1recipient... 100 --from alice --node http://localhost:8000
```

## Next Steps

- **[Transaction Types](tx-types.md)** — Transaction types
- **[Glossary](glossary.md)** — Terminology
- **[CLI Guide](../cli/cpc-cli.md)** — Using CLI
