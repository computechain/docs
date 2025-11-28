# Running Local Node

Guide for running a local ComputeChain node for development and testing.

## Quick Start

### Node A (Genesis Validator)

**Terminal 1:**

```bash
cd computechain
chmod +x start_node_a.sh
./start_node_a.sh
```

**What happens:**

1. Cleanup of previous data in `.node_a/`
2. Node initialization: `./run_node.py --datadir .node_a init`
3. Node startup: `./run_node.py --datadir .node_a run`

**Default parameters:**

- RPC: `http://0.0.0.0:8000`
- P2P: `0.0.0.0:9000`
- Data Dir: `.node_a/`

### Node B (Second Validator)

**Terminal 2:**

```bash
cd computechain
chmod +x start_node_b.sh
./start_node_b.sh
```

**What happens:**

1. Check for Node A
2. Import faucet key from Node A to CLI
3. Create Alice key
4. Fund Alice balance (2000 CPC)
5. Stake Alice (1500 CPC)
6. Export Alice key for Node B
7. Copy genesis.json
8. Start Node B connecting to Node A

**Parameters:**

- RPC: `http://0.0.0.0:8001`
- P2P: `0.0.0.0:9001`
- Peers: `127.0.0.1:9000` (Node A)
- Data Dir: `.node_b/`

## Manual Launch

### Node Initialization

```bash
./run_node.py --datadir .node_a init
```

**What is created during `init`:**

- `genesis.json` — initial allocation & validator list
- `validator_key.hex` — validator private key (created if missing)
- `faucet_key.hex` — faucet private key (deterministic for devnet)

**Will appear after the first `run`:**

- `chain.db` — blockchain database (SQLite)
- `peers.json` — peer list (written on shutdown)

### Starting Node

```bash
./run_node.py --datadir .node_a run
```

**Parameters:**

```bash
./run_node.py --datadir .node_a run \
  --host 0.0.0.0 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers 127.0.0.1:9001
```

**Options:**

- `--host`: RPC host (default: `0.0.0.0`)
- `--port`: RPC port (default: `8000`)
- `--p2p-host`: P2P host (default: `0.0.0.0`)
- `--p2p-port`: P2P port (default: `9000`)
- `--peers`: Comma-separated peer list (e.g., `127.0.0.1:9001,192.168.1.100:9000`)
- `--rebuild-state`: Rebuild state from blocks on startup

## Data Structure

### Node Directory

```
.node_a/
├── genesis.json          # Genesis allocations & validators
├── validator_key.hex     # Validator private key
├── faucet_key.hex        # Faucet private key (devnet)
├── chain.db              # Blockchain database (created after first run)
├── peers.json            # Peer list (saved on shutdown)
└── logs/                 # (optional) if file logging is configured
```

### Genesis.json

**Structure (current MVP):**

```json
{
  "alloc": {
    "cpc1faucet...": "1000000000000000000000000000"
  },
  "validators": [
    {
      "address": "cpcvalcons1...",
      "pq_pub_key": "02abcdef...",
      "power": "2000000000000000000000",
      "is_active": true,
      "reward_address": "cpc1..."
    }
  ]
}
```

Exact amounts depend on `CURRENT_NETWORK.genesis_premine` and `DECIMALS`.

## Logs and Monitoring

### Console Output

**Typical logs:**

```
Starting ComputeChain node...
Data DB: .node_a/chain.db
RPC: 0.0.0.0:8000
P2P: 0.0.0.0:9000
16:39:32 INFO: Chain initialized empty (waiting for genesis)
16:39:32 INFO: Applied genesis allocation to 1 accounts.
16:39:32 INFO: Loaded 1 genesis validators.
16:39:32 INFO: BlockProposer started. Address: cpcvalcons1...
INFO:     Started server process [1108038]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
16:39:32 INFO: P2P Server listening on 0.0.0.0:9000
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
16:39:32 INFO: Block 0 added. Hash: 024119db... (Round 0)
```

### Status Check

**Via RPC:**

```bash
curl http://localhost:8000/status
```

**Output:**

```json
{
  "height": 15,
  "last_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```

## Network Connection

### Adding Peers

**On startup:**

```bash
./run_node.py --datadir .node_a run --peers 192.168.1.100:9000,192.168.1.101:9000
```

**Automatically:**

- Peers saved to `peers.json`
- Automatically connected on next startup
- New peers added on handshake

### Checking Connections

**In logs:**

```
16:39:32 INFO: P2P Server listening on 0.0.0.0:9000
16:39:33 INFO: Connected to peer 127.0.0.1:9001
16:39:33 INFO: Peer registered: 127.0.0.1:9001 (Height: 42)
```

**Via peers.json:**

```bash
cat .node_a/peers.json
```

**Output:**

```json
[
  "127.0.0.1:9001",
  "192.168.1.100:9000"
]
```

## Troubleshooting

### Error: Port already in use

**Cause:** Port is occupied by another node or process

**Solution:**

```bash
# Find process on port
lsof -i :8000
# Or
netstat -tulpn | grep 8000

# Stop process or use different port
./run_node.py --datadir .node_a run --port 8002
```

### Error: Database locked

**Cause:** Another node is using the same database

**Solution:**

- Ensure only one node uses `--datadir .node_a`
- Use different directories for different nodes

### Error: Genesis mismatch

**Cause:** Different genesis.json between nodes

**Solution:**

```bash
# Copy genesis.json from first node
cp .node_a/genesis.json .node_b/genesis.json
```

### Error: Cannot connect to peers

**Cause:** Peers unavailable or firewall blocking

**Solution:**

```bash
# Check peer availability
telnet 192.168.1.100 9000

# Check firewall
sudo ufw status
# Allow port
sudo ufw allow 9000/tcp
```

## State Rebuild

### When Needed

**Cases:**

- State corruption
- State logic changes
- Debugging

### How to Perform

```bash
./run_node.py --datadir .node_a run --rebuild-state
```

**What happens:**

1. Node loads all blocks from database
2. Applies transactions again
3. Recalculates state (accounts, validators)
4. Saves new state

**Execution time:**

- Depends on number of blocks
- For devnet usually a few seconds
- For mainnet may take minutes/hours

## Next Steps

- **[Configuration](config.md)** — Network parameter configuration
- **[P2P Sync](p2p-sync.md)** — Network synchronization
- **[CLI Guide](../cli/cpc-cli.md)** — Using CLI
