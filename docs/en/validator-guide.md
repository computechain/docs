# Validator Guide

## Setup Validator Node

### 1. Install

```bash
git clone https://github.com/computechain/computechain
cd computechain
pip install -r requirements.txt
```

### 2. Initialize Node

```bash
./run_node.py --datadir .validator init
```

### 3. Configure (Optional)

Edit `.validator/config.json`:

```json
{
  "listen_addr": "0.0.0.0",
  "listen_port": 8000,
  "p2p_port": 26656,
  "seeds": ["seed1.computechain.space:26656"]
}
```

### 4. Start Node

```bash
./run_node.py --datadir .validator start
```

**Dashboard:** `http://localhost:8000`

## Become Validator

### 1. Create Key

```bash
./cpc-cli keys add validator
```

### 2. Fund Account

Get testnet tokens from faucet or transfer from another account.

### 3. Stake

```bash
# Minimum 100 CPC
./cpc-cli tx stake 500 --from validator
```

### 4. Wait for Activation

Validators activate after 100 blocks (~16 minutes).

```bash
# Check status
./cpc-cli query validators
```

## Validator Lifecycle

### States

1. **INACTIVE** - Just staked, waiting for activation
2. **ACTIVE** - Producing blocks, earning rewards
3. **JAILED** - Poor performance, temporarily disabled
4. **EJECTED** - Slashed 100%, permanently removed

### Activation

**Trigger:** Epoch transition (every 100 blocks)

**Requirements:**
- Minimum stake (100 CPC)
- Minimum power relative to others
- Not jailed

### Performance Tracking

**Uptime Score:** `blocks_signed / total_expected_blocks`

**Monitoring:**

```bash
curl http://localhost:8000/validators | jq '.validators[] | {address, uptime_score}'
```

**Minimum:** 75% uptime required

## Jailing & Slashing

### Jailing

**Triggered when:**
- Uptime < 75%
- Missing too many blocks

**Penalty:** Validator temporarily disabled

**Recovery:**

```bash
# Option 1: Wait 1000 blocks
# Automatically unjailed if performance improves

# Option 2: Pay 1000 CPC to unjail immediately
./cpc-cli tx unjail --from validator
```

### Graduated Slashing

Progressive penalties for repeated jailing:

| Jail Count | Penalty | Action |
|------------|---------|--------|
| 1st time | 5% | Slash 5% of stake |
| 2nd time | 10% | Slash 10% of stake |
| 3rd time | 100% | **EJECTED** - stake burned |

**Prevention:**
- Monitor uptime constantly
- Set up alerts for missed blocks
- Have backup infrastructure

## Validator Metadata

### Update Info

```bash
./cpc-cli tx update-validator \
  --name "My Validator" \
  --website "https://myvalidator.com" \
  --description "Professional validator service" \
  --commission 0.10 \
  --from validator
```

### View Metadata

```bash
curl http://localhost:8000/validators | jq '.validators[0]'
```

## Monitoring

### Dashboard

Built-in web dashboard: `http://localhost:8000`

Shows:
- Current height, epoch
- Validator list with uptime scores
- Recent blocks

### Logs

```bash
tail -f .validator/node.log
```

### Metrics

```bash
# Validator status
curl http://localhost:8000/validators

# Block height
curl http://localhost:8000/status | jq '.height'

# Balance
curl http://localhost:8000/balance/<VALIDATOR_ADDRESS>
```

## Best Practices

### Infrastructure

- ✅ **Redundancy** - Multiple servers, failover
- ✅ **Monitoring** - Alerts for downtime
- ✅ **Security** - Firewall, DDoS protection
- ✅ **Backups** - Regular key backups

### Operations

- ✅ **Uptime** - Maintain >95% uptime
- ✅ **Updates** - Keep node software updated
- ✅ **Commission** - Set fair rate (5-15%)
- ✅ **Communication** - Announce maintenance windows

### Security

- ✅ **Key Management** - Secure private keys
- ✅ **Access Control** - Limit SSH access
- ✅ **Monitoring** - Alert on unusual activity
- ✅ **Backup** - Secure key backups

## Troubleshooting

### Node Not Syncing

```bash
# Check peer count
curl http://localhost:8000/status | jq '.peers'

# Add seeds in config.json
```

### Validator Not Active

```bash
# Check epoch
curl http://localhost:8000/validators | jq '.epoch'

# Wait for next epoch transition (every 100 blocks)
```

### Missed Blocks

```bash
# Check validator status
curl http://localhost:8000/validators | jq '.validators[] | select(.address=="cpcvalcons1...")'

# Monitor logs
tail -f .validator/node.log | grep "Block.*added"
```

## Next Steps

- **[Staking Guide](staking-guide.md)** - Stake, delegate, rewards
- **[CLI Reference](cli-reference.md)** - Complete commands
- **[Advanced Topics](advanced.md)** - Architecture, PoC
