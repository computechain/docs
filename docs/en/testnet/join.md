# Joining Testnet

Guide for connecting to the public ComputeChain testnet.

## Testnet Status

**Current version:** 🚧 In development

**Planned launch:** After Stage 4 completion

**Testnet parameters:**

- Network ID: `testnet`
- Chain ID: `cpc-testnet-1`
- Block Time: 30 seconds
- Epoch Length: 100 blocks (~50 minutes)
- Min Validator Stake: 100,000 CPC
- Max Validators: 21

## Preparation

### Requirements

- Python 3.12+
- ComputeChain node (latest version)
- Minimum 100,000 CPC (testnet tokens) for validator (regular full nodes can run without staking)
- Stable internet connection
- Open port 9000 (for P2P)

### Installation

```bash
git clone https://github.com/computechain/computechain.git
cd computechain
pip install -r requirements.txt
chmod +x cpc-cli run_node.py
```

## Getting genesis.json

### From Official Source (after launch)

```bash
# Download genesis.json
curl https://testnet.computechain.ru/genesis.json > genesis.json

# Or via GitHub
wget https://raw.githubusercontent.com/computechain/testnet/main/genesis.json
```

**Verification:**

```bash
cat genesis.json | jq '.header.height'  # Should be 0
cat genesis.json | jq '.header.chain_id'  # Should be "cpc-testnet-1"
```

## Getting Peer List

### From Official Source (after launch)

```bash
# Get peer list
curl https://testnet.computechain.ru/peers.json

# Or via GitHub
wget https://raw.githubusercontent.com/computechain/testnet/main/peers.json
```

**Format:**

```json
[
  "testnet-peer-1.computechain.ru:9000",
  "testnet-peer-2.computechain.ru:9000",
  "192.168.1.100:9000"
]
```

## Starting Node

### Initialization

```bash
./run_node.py --datadir .testnet_node init
```

**Important:** Replace `genesis.json` with testnet version:

```bash
cp genesis.json .testnet_node/genesis.json
```

### Starting with Peers

```bash
./run_node.py --datadir .testnet_node run \
  --peers testnet-peer-1.computechain.ru:9000,testnet-peer-2.computechain.ru:9000
```

### Connection Check

**Via status:**

```bash
curl http://localhost:8000/status
```

**Output:**

```json
{
  "height": 12345,
  "last_hash": "0x...",
  "network": "testnet",
  "mempool_size": 5,
  "epoch": 123
}
```

**Synchronization check:**

- `height` should increase
- `network` should be `"testnet"`
- Logs show peer connections

## Becoming a Validator (optional)

### Getting Tokens

**Faucet (planned):**

```bash
# Request tokens via faucet
curl -X POST https://testnet.computechain.ru/faucet \
  -H "Content-Type: application/json" \
  -d '{"address": "cpc1your_address..."}'
```

**Or request from other participants / mock exchange**

### Staking

```bash
# Create key
./cpc-cli keys add validator

# Get address
VALIDATOR_ADDR=$(./cpc-cli keys show validator | grep address | awk '{print $2}' | tr -d '",')

# Fund balance (minimum 100,000 CPC + fees)
# ... (via faucet or exchange)

# Stake
# Stake (requires ~100,000 CPC testnet tokens)
./cpc-cli tx stake 100000 --from validator --node http://localhost:8000
```

### Waiting for Activation

**Epoch:** 100 blocks (~50 minutes)

**Check:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

**After epoch:**

- Validator should appear in list
- `is_active` should be `true`
- Validator will start producing blocks in Round-Robin
- Running a non-validating full node is still useful: it verifies blocks, participates in P2P sync, and allows you to send/receive transactions without staking.

## Monitoring

### Check Node Status

```bash
curl http://localhost:8000/status
```

### Check Validators

```bash
./cpc-cli query validators --node http://localhost:8000
```

### Check Balance

```bash
./cpc-cli query balance <ADDRESS> --node http://localhost:8000
```

### Node Logs

**Typical logs:**

```
Starting ComputeChain node...
Data DB: .testnet_node/chain.db
RPC: 0.0.0.0:8000
P2P: 0.0.0.0:9000
Connected to peer testnet-peer-1.computechain.ru:9000
Handshake completed with testnet-peer-1.computechain.ru:9000
Syncing blocks: 0 -> 12345
Block 12345 added. Hash: 0x... (Round 0)
```

## Troubleshooting

### Problem: Cannot connect to peers

**Causes:**

- Peers unavailable
- Firewall blocking connections
- Incorrect genesis.json

**Solution:**

```bash
# Check peer availability
telnet testnet-peer-1.computechain.ru 9000

# Check firewall
sudo ufw status
sudo ufw allow 9000/tcp

# Check genesis.json
cat .testnet_node/genesis.json | jq '.header.chain_id'
```

### Problem: Node not synchronizing

**Causes:**

- No peer connections
- Lag too large
- Network issues

**Solution:**

```bash
# Add more peers
./run_node.py --datadir .testnet_node run \
  --peers peer1:9000,peer2:9000,peer3:9000

# Check connections
cat .testnet_node/peers.json
```

### Problem: Genesis mismatch

**Cause:** Incorrect genesis.json

**Solution:**

```bash
# Download correct genesis.json
curl https://testnet.computechain.ru/genesis.json > .testnet_node/genesis.json

# Restart node
./run_node.py --datadir .testnet_node run
```

## Useful Links

- **Explorer:** https://explorer.testnet.computechain.ru (planned)
- **Faucet:** https://faucet.testnet.computechain.ru (planned)
- **Discord/Telegram:** (links will be added after launch)

## Next Steps

- **[Known Issues](known-issues.md)** — Known issues
- **[Bug Bounty](bug-bounty.md)** — Report a bug
- **[Node Setup](../node/run-local.md)** — Node configuration
