# Node Configuration

Network parameters and ComputeChain node configuration.

## Network Parameters

### NetworkConfig

**Location:** `protocol/config/params.py`

**Structure:**

```python
class NetworkConfig:
    network_id: str              # "devnet", "testnet", "mainnet"
    chain_id: str               # "cpc-devnet-1", etc.
    block_time_sec: int         # Time between blocks (seconds)
    min_gas_price: int          # Minimum gas price (wei)
    block_gas_limit: int        # Maximum gas per block
    max_tx_per_block: int       # Maximum number of transactions
    genesis_premine: int        # Premine in genesis (wei)
    bech32_prefix_acc: str      # Account address prefix
    bech32_prefix_val: str      # Validator address prefix (future)
    bech32_prefix_cons: str     # Consensus address prefix
    epoch_length_blocks: int    # Epoch length (blocks)
    min_validator_stake: int    # Minimum stake (wei)
    max_validators: int         # Maximum validators
```

*Note: additional internal fields (e.g., `DECIMALS`, deterministic `faucet_priv_key`) are defined in `protocol/config/params.py`. See the source file for the complete dataclass.*

## Networks

### Devnet (example config)

```python
NetworkConfig(
    network_id="devnet",
    chain_id="cpc-devnet-1",
    block_time_sec=10,
    min_gas_price=1000,
    block_gas_limit=10_000_000,
    max_tx_per_block=100,
    genesis_premine=1_000_000_000 * 10**18,  # 1B CPC
    epoch_length_blocks=10,
    min_validator_stake=1000 * 10**18,  # 1,000 CPC
    max_validators=5
)
```

**Usage:**
- Local development
- Testing
- Deterministic faucet key

> Actual parameter values may change between builds. Always verify `protocol/config/params.py` in the version you are running.

### Testnet (planned config)

```python
NetworkConfig(
    network_id="testnet",
    chain_id="cpc-testnet-1",
    block_time_sec=30,
    min_gas_price=5000,
    block_gas_limit=15_000_000,
    max_tx_per_block=1000,
    genesis_premine=100_000_000 * 10**18,  # 100M CPC
    epoch_length_blocks=100,
    min_validator_stake=100_000 * 10**18,  # 100,000 CPC
    max_validators=21
)
```

**Usage:**
- Public testnet
- Integration testing
- Mainnet preparation

### Mainnet (planned config)

```python
NetworkConfig(
    network_id="mainnet",
    chain_id="cpc-mainnet-1",
    block_time_sec=60,
    min_gas_price=1_000_000_000,  # 1 Gwei
    block_gas_limit=30_000_000,
    max_tx_per_block=5000,
    genesis_premine=0,  # Fair launch
    epoch_length_blocks=72,  # ~72 minutes
    min_validator_stake=100_000 * 10**18,  # 100,000 CPC
    max_validators=100
)
```

**Usage:**
- Production network
- Real transactions and tokens

> These mainnet/testnet parameter lists are illustrative. Check `protocol/config/params.py` in your build for the authoritative values.

## Gas Costs

### Base Costs

**Location:** `protocol/config/params.py`

```python
GAS_PER_TYPE = {
    TxType.TRANSFER:      21_000,
    TxType.STAKE:         40_000,
    TxType.SUBMIT_RESULT: 80_000,
}
```

**Fee calculation:**

```python
fee = gas_used * gas_price
```

**Examples:**

| Transaction Type | Gas Used | Gas Price (Devnet) | Fee (wei) | Fee (CPC) |
|-----------------|----------|-------------------|-----------|-----------|
| TRANSFER | 21,000 | 1,000 | 21,000,000 | 0.000021 |
| STAKE | 40,000 | 1,000 | 40,000,000 | 0.00004 |
| SUBMIT_RESULT | 80,000 | 1,000 | 80,000,000 | 0.00008 |

## Network Switching

### Current Network

**Default:** Devnet

```python
# protocol/config/params.py
CURRENT_NETWORK = NETWORKS["devnet"]
```

### Changing Network

**In code (conceptual example):**

```python
from computechain.protocol.config.params import NETWORKS, CURRENT_NETWORK

# Switch to testnet (must be done before importing modules that read CURRENT_NETWORK)
CURRENT_NETWORK = NETWORKS["testnet"]
```

*In the current MVP the network is chosen at process startup via `CURRENT_NETWORK`. Reassigning it at runtime in a single module will not automatically update other components.*

**Via environment variable (Future):**

```bash
export CPC_NETWORK=testnet
./run_node.py --datadir .node_a run
```

## Node Parameters

### RPC Server

**Launch parameters:**

```bash
./run_node.py --datadir .node_a run \
  --host 0.0.0.0 \
  --port 8000
```

**Default:**
- Host: `0.0.0.0` (all interfaces)
- Port: `8000`

**Security:**
- In production use `127.0.0.1` or firewall
- Configure HTTPS via reverse proxy (nginx)

### P2P Server

**Launch parameters:**

```bash
./run_node.py --datadir .node_a run \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000
```

**Default:**
- Host: `0.0.0.0`
- Port: `9000`

**Firewall:**
- Open port for incoming connections
- Recommended to use static IP

### Peers

**On startup:**

```bash
./run_node.py --datadir .node_a run \
  --peers 192.168.1.100:9000,192.168.1.101:9000
```

**Automatic saving:**

- Peers saved to `peers.json`
- Automatically connected on next startup

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

**Process:**

1. Load all blocks from database
2. Apply transactions again
3. Recalculate state
4. Save new state

## Environment Variables

### CPC_NODE

**Usage:** Node URL for CLI

```bash
export CPC_NODE=http://localhost:8000
./cpc-cli query balance cpc1...
```

### CPC_NETWORK (Future)

**Usage:** Network selection

```bash
export CPC_NETWORK=testnet
./run_node.py --datadir .node_a run
```

## Configuration Examples

### Local Development

```bash
# Node A
./run_node.py --datadir .node_a run \
  --port 8000 \
  --p2p-port 9000

# Node B
./run_node.py --datadir .node_b run \
  --port 8001 \
  --p2p-port 9001 \
  --peers 127.0.0.1:9000
```

### Testnet Validator

```bash
./run_node.py --datadir .testnet_node run \
  --host 0.0.0.0 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers testnet-peer-1:9000,testnet-peer-2:9000
```

### Production Node

```bash
./run_node.py --datadir .mainnet_node run \
  --host 127.0.0.1 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers mainnet-peer-1:9000,mainnet-peer-2:9000
```

**Recommendations:**

- Use reverse proxy (nginx) for HTTPS
- Configure monitoring (Prometheus, Grafana)
- Configure file logging
- Use systemd for autostart

## Next Steps

- **[Run Local](run-local.md)** — Running local node
- **[P2P Sync](p2p-sync.md)** — Network synchronization
- **[CLI Guide](../cli/cpc-cli.md)** — Using CLI
