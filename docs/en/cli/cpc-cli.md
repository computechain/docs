# CLI Wallet (cpc-cli)

Command-line interface for working with ComputeChain: key management, sending transactions, querying nodes.

## Installation

**Current Version:** Executable script in repository root

```bash
chmod +x cpc-cli
./cpc-cli --help
```

## Commands

### Keys — Key Management

#### Create Key

```bash
./cpc-cli keys add <NAME>
```

**Example:**

```bash
./cpc-cli keys add alice
```

**Output:**

```
Key 'alice' created.
Address: cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v
Pubkey:  030c9ae768a358e7924d2a27fd0708549902e17af8e81cf7a545e0f319d2e177bd
Important: Private key saved unencrypted (MVP). Do not share!
```

#### Import Key

```bash
./cpc-cli keys import <NAME> --private-key <HEX_PRIVATE_KEY>
```

**Example:**

```bash
./cpc-cli keys import faucet --private-key 4f3edf982522b4e51b7e8b5f2f9c4d1d7a9e5f8c2b6d4e1a3c5b7d9e0f1a2b3c
```

#### List Keys

```bash
./cpc-cli keys list
```

**Output:**

```
Name            Address                                          
------------------------------------------------------------
alice           cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v
faucet          cpc1q02sr0n4kw84qfsy7q9ntp7mv6rhs5p4k9zyf6
```

#### Show Key

```bash
./cpc-cli keys show <NAME>
```

**Example:**

```bash
./cpc-cli keys show alice
```

**Output:**

```json
{
  "name": "alice",
  "address": "cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v",
  "public_key": "030c9ae768a358e7924d2a27fd0708549902e17af8e81cf7a545e0f319d2e177bd"
}
```

### Query — Node Queries

#### Balance

```bash
./cpc-cli query balance <ADDRESS> [--node <URL>]
```

**Example:**

```bash
./cpc-cli query balance cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v --node http://localhost:8000
```

**Output:**

```
Balance: 2000.0 CPC
Nonce: 1
```

#### Block

```bash
./cpc-cli query block <HEIGHT> [--node <URL>]
```

**Example:**

```bash
./cpc-cli query block 10 --node http://localhost:8000
```

**Output:** JSON with full block

#### Validators

```bash
./cpc-cli query validators [--node <URL>]
```

**Example:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

**Output:**

```
Epoch: 1
Address                                         Power       Active
----------------------------------------------------------------------
cpcvalcons1alice...                            1500        True
cpcvalcons1bob...                               1200        True
```

#### Delegations

Get all delegations for a specific address.

```bash
./cpc-cli query delegations <ADDRESS> [--node <URL>]
```

**Example:**

```bash
./cpc-cli query delegations cpc1abc... --node http://localhost:8000
```

**Output:**

```
Delegator: cpc1abc...
Total Delegated: 100.0 CPC

Validator                                      Amount          Commission  Name
------------------------------------------------------------------------------------------
cpcvalcons1xyz...                              60.0            10.0%       Validator A
cpcvalcons1def...                              40.0            5.0%        Validator B
```

#### Rewards

Get reward history for a delegator address.

```bash
./cpc-cli query rewards <ADDRESS> [--node <URL>]
```

**Example:**

```bash
./cpc-cli query rewards cpc1abc... --node http://localhost:8000
```

**Output:**

```
Delegator: cpc1abc...
Current Epoch: 5
Total Rewards: 125.5 CPC

Epoch      Reward Amount
------------------------------
0          25.4
1          24.8
2          25.1
3          25.0
4          25.2
```

### Tx — Transactions

#### Send Coins

```bash
./cpc-cli tx send <TO_ADDRESS> <AMOUNT> --from <KEY_NAME> [--node <URL>] [--gas-price <PRICE>] [--gas-limit <LIMIT>]
```

**Example:**

```bash
./cpc-cli tx send cpc1q9u5zga8d6jtx0g7hkk4upckw7t2k38cd8n4fy 100 --from alice --node http://localhost:8000
```

**Parameters:**

- `--gas-price`: Gas price (default: 1000 for devnet)
- `--gas-limit`: Gas limit (default: 21,000 for TRANSFER)

**Output:**

```
Sending 100.0 CPC to cpc1q9u5zga8d6jtx0g7hkk4upckw7t2k38cd8n4fy...
Success! TxHash: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd
```

#### Staking

```bash
./cpc-cli tx stake <AMOUNT> --from <KEY_NAME> [--node <URL>] [--gas-price <PRICE>] [--gas-limit <LIMIT>]
```

**Example:**

```bash
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000
```

**Parameters:**

- `--gas-price`: Gas price (default: 1000)
- `--gas-limit`: Gas limit (CLI default: 100,000 — minimal value from `GAS_PER_TYPE[STAKE]`)

**Output:**

```
Staking 1500.0 CPC from cpc1alice...
Success! TxHash: abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678
```

**Important:** Public key is automatically taken from keystore.

#### Unstaking

```bash
./cpc-cli tx unstake <AMOUNT> --from <KEY_NAME> [--node <URL>] [--gas-price <PRICE>] [--gas-limit <LIMIT>]
```

**Example:**

```bash
./cpc-cli tx unstake 500 --from alice --node http://localhost:8000
```

**Parameters:**

- `--gas-price`: Gas price (default: 1,000)
- `--gas-limit`: Gas limit (default: 40,000)

**Output:**

```
Unstaking 500.0 CPC from cpc1alice...
Success! TxHash: fedcba0987654321fedcba0987654321fedcba0987654321fedcba09876543
```

**Penalty:** If validator is jailed, 10% of unstaked amount is burned.

#### Update Validator Metadata

```bash
./cpc-cli tx update-validator --from <KEY_NAME> [--name <NAME>] [--website <URL>] [--description <TEXT>] [--commission <RATE>] [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx update-validator \
  --name "MyPool" \
  --website "https://pool.com" \
  --description "Best validator pool" \
  --commission 0.15 \
  --from alice \
  --node http://localhost:8000
```

**Parameters:**

- `--name`: Validator name (max 64 chars)
- `--website`: Website URL (max 128 chars)
- `--description`: Description (max 256 chars)
- `--commission`: Commission rate (0.0-1.0, max 0.20 = 20%)
- At least one metadata field required

**Output:**

```
Updating validator metadata...
Success! TxHash: 1122334455667788990011223344556677889900112233445566778899001122
```

#### Delegate to Validator

```bash
./cpc-cli tx delegate <VALIDATOR_ADDRESS> <AMOUNT> --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx delegate cpcvalcons1abc123... 500 --from delegator --node http://localhost:8000
```

**Parameters:**

- `VALIDATOR_ADDRESS`: Validator consensus address (cpcvalcons...)
- `AMOUNT`: Delegation amount (minimum 100 CPC)

**Output:**

```
Delegating 500.0 CPC to cpcvalcons1abc123...
Success! TxHash: aabbccdd112233445566778899aabbccdd112233445566778899aabbccdd1122
```

#### Undelegate from Validator

```bash
./cpc-cli tx undelegate <VALIDATOR_ADDRESS> <AMOUNT> --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx undelegate cpcvalcons1abc123... 200 --from delegator --node http://localhost:8000
```

**Parameters:**

- `VALIDATOR_ADDRESS`: Validator consensus address (cpcvalcons...)
- `AMOUNT`: Amount to undelegate

**Output:**

```
Undelegating 200.0 CPC from cpcvalcons1abc123...
Success! TxHash: 99887766554433221100998877665544332211009988776655443322110099
```

#### Unjail Validator

```bash
./cpc-cli tx unjail --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx unjail --from alice --node http://localhost:8000
```

**Cost:**

- Unjail fee: 1,000 CPC (burned)
- Gas fee: ~50,000 gas
- Total: ~1,000.00005 CPC

**Output:**

```
Unjailing validator (cost: 1000 CPC + gas)...
Success! TxHash: 5544332211009988776655443322110099887766554433221100998877665544
```

**Note:** Validator must be jailed to use this command.

#### Submit PoC Result

```bash
./cpc-cli tx submit-result --task-id <UUID> --result-hash <HEX> --from <KEY_NAME> [--node <URL>] [--proof <PROOF>] [--nonce <NONCE>]
```

**Example:**

```bash
./cpc-cli tx submit-result \
  --task-id "550e8400-e29b-41d4-a716-446655440000" \
  --result-hash "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd" \
  --from worker \
  --node http://localhost:8000
```

**Parameters:**

- `--task-id`: Task UUID (required)
- `--result-hash`: Result hash (required)
- `--proof`: Proof (optional)
- `--nonce`: Nonce for synthetic tasks (optional)
- Gas price & limit: CLI currently uses `gas_price=1000` and `gas_limit=100,000` for all PoC result submissions.

**Output:**

```
Submitting result for task 550e8400-e29b-41d4-a716-446655440000...
Success! TxHash: 9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedc
```

## Environment Variables

### CPC_NODE

**Usage:** Default node URL

```bash
export CPC_NODE=http://localhost:8000
./cpc-cli query balance cpc1...
```

**Priority:**

1. `--node` command parameter
2. `CPC_NODE` environment variable
3. `http://localhost:8000` (default)

## Usage Examples

### Example 1: Full Validator Creation Scenario

```bash
# 1. Create key
./cpc-cli keys add alice

# 2. Get address
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 3. Fund account
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000

# 4. Check balance
./cpc-cli query balance $ALICE_ADDR --node http://localhost:8000

# 5. Stake
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000

# 6. Check validators
./cpc-cli query validators --node http://localhost:8000
```

### Example 2: Sending Transactions with Custom Gas

```bash
# High gas price for fast inclusion
./cpc-cli tx send cpc1q9u5zga8d6jtx0g7hkk4upckw7t2k38cd8n4fy 100 \
  --from alice \
  --node http://localhost:8000 \
  --gas-price 5000 \
  --gas-limit 21000
```

### Example 3: Working with Multiple Nodes

```bash
# Node A
./cpc-cli query balance cpc1alice... --node http://localhost:8000

# Node B
./cpc-cli query balance cpc1alice... --node http://localhost:8001
```

## Troubleshooting

### Error: Key not found

**Cause:** Key doesn't exist in keystore

**Solution:**

```bash
# Check key list
./cpc-cli keys list

# Create key
./cpc-cli keys add <NAME>
```

### Error: Connection refused

**Cause:** Node not running or unavailable

**Solution:**

```bash
# Check node status
curl http://localhost:8000/status

# Specify correct URL
./cpc-cli query balance cpc1... --node http://192.168.1.100:8000
```

### Error: Insufficient balance

**Cause:** Insufficient balance for transaction

**Solution:**

```bash
# Check balance
./cpc-cli query balance cpc1... --node http://localhost:8000

# Fund account
./cpc-cli tx send <ADDRESS> <AMOUNT> --from faucet
```

### Error: Invalid nonce

**Cause:** Nonce doesn't match expected

**Solution:**

- CLI automatically gets nonce from node
- If error repeats, check that transaction wasn't sent twice

## Next Steps

- **[Node CLI](node-cli.md)** — Commands for node management
- **[Wallets](../wallets/keystore.md)** — Key management
- **[Staking](../staking/staking-basic.md)** — How to become a validator
