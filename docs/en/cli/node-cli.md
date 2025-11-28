# Node CLI (run_node.py)

Commands for managing ComputeChain node: initialization, running, configuration.

## Commands

### Init — Node Initialization

```bash
./run_node.py --datadir <DIR> init
```

**Example:**

```bash
./run_node.py --datadir .node_a init
```

**Init creates:**

- `genesis.json` — genesis block parameters
- `validator_key.hex` — validator private key (created if missing)
- `faucet_key.hex` — faucet private key (deterministic for devnet)

**Will appear after the first `run`:**

- `chain.db` — blockchain database (SQLite), created when the node starts
- `peers.json` — peer list, written on graceful shutdown

**Output:**

```
Node initialized in .node_a
```

### Run — Start Node

```bash
./run_node.py --datadir <DIR> run [OPTIONS]
```

**Example:**

```bash
./run_node.py --datadir .node_a run
```

**Options:**

- `--host <HOST>`: RPC host (default: `0.0.0.0`)
- `--port <PORT>`: RPC port (default: `8000`)
- `--p2p-host <HOST>`: P2P host (default: `0.0.0.0`)
- `--p2p-port <PORT>`: P2P port (default: `9000`)
- `--peers <PEERS>`: Comma-separated peer list (e.g., `127.0.0.1:9001,192.168.1.100:9000`)
- `--rebuild-state`: Rebuild state from blocks on startup

**Example with options:**

```bash
./run_node.py --datadir .node_a run \
  --host 0.0.0.0 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers 127.0.0.1:9001
```

**Sample output (matches real logs):**

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
...
```

## Usage Examples

### Example 1: Local Development (Node A)

```bash
./run_node.py --datadir .node_a init
./run_node.py --datadir .node_a run
```

### Example 2: Second Validator (Node B)

```bash
# After setup via start_node_b.sh
./run_node.py --datadir .node_b run \
  --port 8001 \
  --p2p-port 9001 \
  --peers 127.0.0.1:9000
```

### Example 3: Connecting to Testnet

```bash
./run_node.py --datadir .testnet_node run \
  --peers testnet-peer-1:9000,testnet-peer-2:9000,testnet-peer-3:9000
```

### Example 4: Rebuild State

```bash
./run_node.py --datadir .node_a run --rebuild-state
```

**When to use:**

- State corruption
- State logic changes
- Debugging

## Data Structure

### Node Directory

```
<datadir>/
├── genesis.json          # Genesis block
├── validator_key.hex     # Validator private key
├── faucet_key.hex        # Faucet private key (devnet)
├── chain.db              # Blockchain database (created after first run)
└── peers.json            # Peer list (written on shutdown)
```

## Logs

### Console Output

**Typical logs:**

- Component initialization
- Peer connections
- Block production
- Validation errors

**Example:**

```
Starting ComputeChain node...
Data DB: .node_a/chain.db
RPC: 0.0.0.0:8000
P2P: 0.0.0.0:9000
16:39:32 INFO: Chain initialized empty (waiting for genesis)
16:39:32 INFO: Applied genesis allocation to 1 accounts.
16:39:32 INFO: Loaded 1 genesis validators.
INFO:     Started server process [1108038]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
16:39:32 INFO: P2P Server listening on 0.0.0.0:9000
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
16:39:32 INFO: Block 0 added. Hash: 024119db... (Round 0)
16:39:33 INFO: Block 1 added. Hash: 640cbe5a... (Round 0)
```

### Logging Configuration

**Current Implementation:** Logs output to console

**Future Implementation:** Configuration via config file

## Troubleshooting

### Error: Port already in use

**Cause:** Port is occupied

**Solution:**

```bash
# Use different port
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

## Next Steps

- **[Run Local](../node/run-local.md)** — Detailed startup guide
- **[Configuration](../node/config.md)** — Parameter configuration
- **[P2P Sync](../node/p2p-sync.md)** — Network synchronization
