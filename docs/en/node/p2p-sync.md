# P2P Synchronization

How P2P network and block synchronization works in ComputeChain.

## P2P Architecture

### Components

1. **P2P Node:** Manages peer connections
2. **Protocol:** Message format (handshake, blocks, transactions)
3. **Sync Engine:** Block synchronization logic
4. **Mempool:** Transaction propagation

## Message Protocol

### Message Types

```python
class P2PMessageType(str, Enum):
    HANDSHAKE = "handshake"
    NEW_BLOCK = "new_block"
    NEW_TX = "new_tx"
    GET_BLOCKS = "get_blocks"  # Sync request
    BLOCKS_RESPONSE = "blocks_response"  # Blocks response
```

### Handshake

**On Connection:**

```python
HandshakePayload(
    node_id="node-123",
    p2p_port=9000,
    protocol_version=1,
    network="devnet",
    best_height=15,
    best_hash="1234abcd...",
    genesis_hash="abcd9876..."
)
```

**Checks:**

- `network` must match
- `genesis_hash` must match
- `protocol_version` field is present but not yet used for compatibility checks (MVP)

### New Block

**Propagation:**

```python
NewBlockPayload(
    block={
        "header": {...},
        "txs": [...]
    }
)
```

**Process:**

1. Validator produces block
2. Block is signed
3. Block is broadcast to all peers
4. Peers verify and add block

### New Transaction

**Propagation:**

```python
NewTxPayload(
    tx={
        "tx_type": "TRANSFER",
        "from_address": "cpc1...",
        ...
    }
)
```

**Process:**

1. Transaction enters mempool
2. Broadcast to all peers
3. Peers add to their mempool
4. Validator includes in block

## Block Synchronization

### Sync Modes

**SYNCING:**

- Node is behind network
- Does not produce new blocks
- Requests blocks from peers

**SYNCED:**

- Node is synchronized
- Can produce blocks (if validator)
- Accepts new blocks from peers

### Synchronization Process

**Step 1: Determine Lag**

```python
local_height = chain.height
peer_best_height = handshake.best_height

if peer_best_height > local_height:
    # Need synchronization
    sync_state = SyncState.SYNCING
```

**Step 2: Request Blocks**

```python
GetBlocksPayload(
    from_height=local_height + 1,
    to_height=peer_best_height
)
```

**Step 3: Receive Blocks**

```python
BlocksResponsePayload(
    blocks=[
        {"header": {...}, "txs": [...]},
        {"header": {...}, "txs": [...]},
        ...
    ]
)
```

**Step 4: Apply Blocks**

```python
for block_data in blocks:
    block = Block.model_validate(block_data)
    if chain.add_block(block):
        # Block added successfully
        continue
    else:
        # Validation error
        break
```

### Batch Synchronization

**Optimization:**

- Blocks are requested in limited batches (current implementation caps responses at 500 blocks per message)
- Reduces number of messages
- Speeds up synchronization

## Fork Handling (MVP)

- When a block arrives during sync and its `prev_hash` does not match `last_hash`, the node rolls back the most recent local block and retries syncing from that height.
- Full fork resolution with competing branches / longest-chain selection is planned for future releases.

## Peer Management

### Adding Peers

**On Startup:**

```bash
./run_node.py --datadir .node_a run --peers 192.168.1.100:9000
```

**Automatically:**

- On handshake, new peer added to list
- Saved to `peers.json`

### Saving Peers

**File:** `peers.json`

**Format:**

```json
[
  "127.0.0.1:9001",
  "192.168.1.100:9000",
  "192.168.1.101:9000"
]
```

**Updates:**

- When new peer connects
- When peer disconnects (periodic cleanup)
- On node shutdown (save current list)

### Reconnection

- On startup, node tries to connect once to peers listed in `peers.json`.
- If connection fails, it is logged. Automatic periodic reconnection / exponential backoff is planned but not yet implemented.

## Examples

### Example 1: New Node Synchronization

```
1. Node starts with genesis
2. Connects to peer (best_height=100)
3. Determines lag: local=0, peer=100
4. Requests blocks 1-100 in batches of 50
5. Applies blocks sequentially
6. After sync, transitions to SYNCED mode
```

### Example 2: Fork Detection

```
1. Node receives block with prev_hash != last_hash
2. Requests chain from peer
3. Detects longer chain
4. Rollbacks local blocks
5. Loads correct branch
6. Continues synchronization
```

## Troubleshooting

### Problem: Node Not Synchronizing

**Causes:**

- No peer connections
- Peers unavailable
- Firewall blocking connections

**Solution:**

```bash
# Check connections
cat .node_a/peers.json

# Check peer availability
telnet 192.168.1.100 9000

# Add peers manually
./run_node.py --datadir .node_a run --peers 192.168.1.100:9000
```

### Problem: Constant Forks

**Causes:**

- Incorrect time (time drift)
- Different genesis
- Consensus bugs

**Solution:**

```bash
# Synchronize time
sudo ntpdate -s time.nist.gov

# Check genesis
cat .node_a/genesis.json | jq '.alloc'

# Rebuild state
./run_node.py --datadir .node_a run --rebuild-state
```

## Next Steps

- **[Run Local](run-local.md)** — Running local node
- **[Configuration](config.md)** — Parameter configuration
- **[CLI Guide](../cli/cpc-cli.md)** — Using CLI
