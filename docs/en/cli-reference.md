# CLI Reference

Complete command reference for `cpc-cli` - the ComputeChain command-line interface.

## Installation

```bash
chmod +x cpc-cli
./cpc-cli --help
```

## Key Management

### Create Key

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

**Storage:** Keys saved in `~/.computechain/keys/` as JSON files

⚠️ **Security:** Keys are currently stored unencrypted. Backup securely and restrict permissions:

```bash
chmod 700 ~/.computechain/keys/
```

### Import Key

```bash
./cpc-cli keys import <NAME> --private-key <HEX_PRIVATE_KEY>
```

**Example:**

```bash
./cpc-cli keys import faucet --private-key 4f3edf982522b4e51b7e8b5f2f9c4d1d...
```

### List Keys

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

### Show Key

```bash
./cpc-cli keys show <NAME>
```

**Output:**

```json
{
  "name": "alice",
  "address": "cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v",
  "public_key": "030c9ae768a358e7924d2a27fd0708549902e17af8e81cf7a545e0f319d2e177bd"
}
```

## Query Commands

### Balance

```bash
./cpc-cli query balance <ADDRESS> [--node <URL>]
```

**Example:**

```bash
./cpc-cli query balance cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v
```

**Output:**

```
Balance: 2000.0 CPC
Nonce: 1
```

### Validators

```bash
./cpc-cli query validators [--node <URL>]
```

**Output:**

```
Epoch: 1
Address                                         Power       Active
----------------------------------------------------------------------
cpcvalcons1alice...                            1500        True
cpcvalcons1bob...                               1200        True
```

### Delegations

```bash
./cpc-cli query delegations <ADDRESS> [--node <URL>]
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

### Rewards

```bash
./cpc-cli query rewards <ADDRESS> [--node <URL>]
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
```

### Unbonding

```bash
./cpc-cli query unbonding <ADDRESS> [--node <URL>]
```

**Output:**

```
Delegator: cpc1abc...
Unbonding Entries: 1

Validator                                      Amount    Creation    Completion  Remaining
------------------------------------------------------------------------------------------------
cpcvalcons1xyz...                              50.0      1000        1100        45 blocks
```

**Fields:**
- `Creation`: Block height when unbonding started
- `Completion`: Block height when tokens will be returned
- `Remaining`: How many blocks until automatic return

### Snapshots

```bash
./cpc-cli snapshot list [--node <URL>]
```

**Output:**

```
Available Snapshots:

Height    Timestamp             Size        Hash
---------------------------------------------------------------------------------
5000      2025-12-23 10:15:30   1.0 MB      abc123def456...
4000      2025-12-23 09:30:15   0.98 MB     def789ghi012...
```

```bash
./cpc-cli snapshot info <HEIGHT> [--node <URL>]
```

**Output:**

```
Snapshot Information:
  Height: 5000
  Timestamp: 2025-12-23 10:15:30
  Size: 1.0 MB
  Hash: abc123def456...
  Compressed: true
  Epoch: 50
  Validators: 5
  Accounts: 103
```

### Block

```bash
./cpc-cli query block <HEIGHT> [--node <URL>]
```

Returns full block JSON for specified height.

## Transaction Commands

### Transfer

```bash
./cpc-cli tx send <TO_ADDRESS> <AMOUNT> --from <KEY_NAME> [--node <URL>] [--gas-price <PRICE>]
```

**Example:**

```bash
./cpc-cli tx send cpc1q9u5zga8d6jtx0g7hkk4upckw7t2k38cd8n4fy 100 --from alice
```

**Parameters:**
- `--gas-price`: Gas price (default: 1000)
- `--gas-limit`: Gas limit (default: 21,000)

### Stake

```bash
./cpc-cli tx stake <AMOUNT> --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx stake 1500 --from alice
```

**Requirements:**
- Minimum: 100 CPC
- Creates validator with `cpcvalcons` address
- Activates in next epoch (after 100 blocks)

### Unstake

```bash
./cpc-cli tx unstake <AMOUNT> --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx unstake 500 --from alice
```

⚠️ **Penalty:** 10% slashed if unstaking while jailed

### Delegate

```bash
./cpc-cli tx delegate <VALIDATOR_ADDRESS> <AMOUNT> --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx delegate cpcvalcons1abc... 500 --from delegator
```

**Requirements:**
- Validator must be active
- Earn proportional rewards based on delegation amount

### Undelegate

```bash
./cpc-cli tx undelegate <VALIDATOR_ADDRESS> <AMOUNT> --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx undelegate cpcvalcons1abc... 200 --from delegator
```

### Update Validator

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
  --from alice
```

**Parameters:**
- `--name`: Validator name (max 64 chars)
- `--website`: Website URL (max 128 chars)
- `--description`: Description (max 256 chars)
- `--commission`: Commission rate (0.0-1.0, max 20%)

### Unjail

```bash
./cpc-cli tx unjail --from <KEY_NAME> [--node <URL>]
```

**Example:**

```bash
./cpc-cli tx unjail --from alice
```

**Cost:**
- Unjail fee: 1000 CPC (burned)
- Gas fee: ~50,000 gas
- Only works if validator is jailed

## Environment Variables

### CPC_NODE

Set default node URL:

```bash
export CPC_NODE=http://localhost:8000
./cpc-cli query balance cpc1...
```

**Priority:**
1. `--node` flag
2. `CPC_NODE` environment variable
3. `http://localhost:8000` (default)

## Complete Examples

### Create & Fund Validator

```bash
# 1. Create key
./cpc-cli keys add alice

# 2. Get address
ALICE=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 3. Fund account
./cpc-cli tx send $ALICE 2000 --from faucet

# 4. Check balance
./cpc-cli query balance $ALICE

# 5. Stake
./cpc-cli tx stake 1500 --from alice

# 6. Wait for epoch transition (~100 blocks)

# 7. Verify validator active
./cpc-cli query validators
```

### Delegate & Earn Rewards

```bash
# 1. Create delegator key
./cpc-cli keys add delegator

# 2. Fund delegator
./cpc-cli tx send <DELEGATOR_ADDR> 500 --from faucet

# 3. Find validator
./cpc-cli query validators

# 4. Delegate
./cpc-cli tx delegate cpcvalcons1abc... 400 --from delegator

# 5. Check delegations
./cpc-cli query delegations <DELEGATOR_ADDR>

# 6. Check rewards (after a few epochs)
./cpc-cli query rewards <DELEGATOR_ADDR>
```

## Troubleshooting

### Key not found

```bash
# Check available keys
./cpc-cli keys list

# Create key if needed
./cpc-cli keys add <NAME>
```

### Connection refused

```bash
# Check node status
curl http://localhost:8000/status

# Or specify node URL
./cpc-cli query balance cpc1... --node http://192.168.1.100:8000
```

### Insufficient balance

```bash
# Check balance
./cpc-cli query balance <ADDRESS>

# Fund from faucet
./cpc-cli tx send <ADDRESS> <AMOUNT> --from faucet
```

## Next Steps

- **[Staking Guide](staking-guide.md)** - Stake, delegate, earn rewards
- **[Validator Guide](validator-guide.md)** - Run validator node
- **[API Reference](api-reference.md)** - RPC endpoints
