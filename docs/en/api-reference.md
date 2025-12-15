# API Reference

RPC endpoint reference for ComputeChain nodes.

**Base URL:** `http://localhost:8000` (change with `--port` flag)

## Node Endpoints

### GET /status

Get node status and current blockchain state.

```bash
curl http://localhost:8000/status
```

**Response:**

```json
{
  "height": 15,
  "last_hash": "1234567890abcdef...",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```

### GET /block/{height}

Get block by height.

```bash
curl http://localhost:8000/block/10
```

**Response:**

```json
{
  "header": {
    "height": 10,
    "prev_hash": "abcd1234...",
    "timestamp": 1700000000,
    "proposer_address": "cpcvalcons1...",
    "compute_root": "7890abcd...",
    "tx_root": "4567efgh...",
    "state_root": "cdef1234...",
    "signature": "feedface...",
    "pub_key": "02..."
  },
  "txs": [...]
}
```

## Account Endpoints

### GET /balance/{address}

Get account balance and nonce.

```bash
curl http://localhost:8000/balance/cpc1a2b3...
```

**Response:**

```json
{
  "address": "cpc1a2b3...",
  "balance": "2000000000000000000000",
  "nonce": 1
}
```

**Note:** Balance is in wei (1 CPC = 10^18 wei)

## Validator Endpoints

### GET /validators

List all validators with their status.

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
      "reward_address": "cpc1alice...",
      "name": "Alice Validator",
      "commission_rate": 0.10
    }
  ]
}
```

**Fields:**
- `address`: Validator consensus address
- `power`: Validator stake in wei
- `is_active`: Whether validator is actively producing blocks
- `reward_address`: Where block rewards are sent
- `commission_rate`: Commission percentage (0.0-1.0)

## Delegation Endpoints

### GET /delegator/{address}/delegations

Get all delegations for an address.

```bash
curl http://localhost:8000/delegator/cpc1abc.../delegations
```

**Response:**

```json
{
  "delegator": "cpc1abc...",
  "total_delegated": 100000000,
  "delegations": [
    {
      "validator": "cpcvalcons1xyz...",
      "amount": 60000000,
      "created_height": 100,
      "validator_name": "Validator A",
      "validator_commission": 0.10
    }
  ]
}
```

### GET /delegator/{address}/rewards

Get reward history for delegator.

```bash
curl http://localhost:8000/delegator/cpc1abc.../rewards
```

**Response:**

```json
{
  "delegator": "cpc1abc...",
  "total_rewards": 125500000,
  "current_epoch": 5,
  "rewards_by_epoch": [
    {"epoch": 0, "amount": 25400000},
    {"epoch": 1, "amount": 24800000}
  ]
}
```

## Transaction Endpoints

### POST /tx/send

Submit signed transaction to mempool.

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

**Response (success):**

```json
{
  "tx_hash": "1234567890abcdef...",
  "status": "received"
}
```

**Response (rejected):**

```json
{
  "tx_hash": "1234567890abcdef...",
  "status": "rejected",
  "error": "Insufficient balance"
}
```

## Data Formats

### Addresses

**Format:** Bech32 encoding with prefix

- Regular accounts: `cpc1...`
- Validators: `cpcvalcons1...`

**Example:**
```
cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
cpcvalcons1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

### Amounts

**Format:** String representation in wei

**Conversion:** 1 CPC = 10^18 wei

**Examples:**
```
"100000000000000000000"   # 100 CPC
"1500000000000000000000"  # 1500 CPC
"21000000"                # 0.000000000021 CPC (fee)
```

### Hashes & Keys

**Format:** Hex string without `0x` prefix

**Examples:**
```
"1234567890abcdef..."
"02a1b2c3d4e5f6g7..."
```

## Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid transaction format |
| 404 | Not Found | Block not found |
| 503 | Service Unavailable | Node not initialized |

## Usage Examples

### Monitor Network

```bash
# Check node status
curl http://localhost:8000/status | jq

# Get latest block height
HEIGHT=$(curl -s http://localhost:8000/status | jq -r '.height')

# Get latest block
curl http://localhost:8000/block/$HEIGHT | jq
```

### Track Validator

```bash
# Get all validators
curl http://localhost:8000/validators | jq

# Get active validators only
curl http://localhost:8000/validators | jq '.validators[] | select(.is_active == true)'

# Get specific validator
curl http://localhost:8000/validators | jq '.validators[] | select(.address == "cpcvalcons1abc...")'
```

### Monitor Delegations

```bash
# Get all delegations for address
curl http://localhost:8000/delegator/cpc1abc.../delegations | jq

# Get total delegated amount
curl http://localhost:8000/delegator/cpc1abc.../delegations | jq '.total_delegated'

# Check rewards
curl http://localhost:8000/delegator/cpc1abc.../rewards | jq
```

### Track Balance Changes

```bash
# Monitor balance
ADDRESS="cpc1abc..."
watch -n 10 "curl -s http://localhost:8000/balance/$ADDRESS | jq"
```

## Integration Tips

### Python Example

```python
import requests

node_url = "http://localhost:8000"

# Get balance
def get_balance(address):
    resp = requests.get(f"{node_url}/balance/{address}")
    data = resp.json()
    balance_cpc = int(data["balance"]) / 10**18
    return balance_cpc

# Get validators
def get_active_validators():
    resp = requests.get(f"{node_url}/validators")
    data = resp.json()
    return [v for v in data["validators"] if v["is_active"]]

# Send transaction (use CLI for signing)
# Use cpc-cli for proper transaction signing
```

### JavaScript Example

```javascript
const nodeUrl = "http://localhost:8000";

// Get status
async function getStatus() {
  const resp = await fetch(`${nodeUrl}/status`);
  return await resp.json();
}

// Get balance in CPC
async function getBalance(address) {
  const resp = await fetch(`${nodeUrl}/balance/${address}`);
  const data = await resp.json();
  return parseInt(data.balance) / 1e18;
}
```

## Next Steps

- **[CLI Reference](cli-reference.md)** - CLI commands for transactions
- **[Staking Guide](staking-guide.md)** - Stake and delegate
- **[Advanced Topics](advanced.md)** - Architecture and PoC
