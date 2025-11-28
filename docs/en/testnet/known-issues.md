# Known Issues

List of known issues and workarounds for testnet and devnet.

## Critical Issues

### No Critical Issues

**Status:** ✅ No known critical issues as of version 0.4.0

If you discover a critical issue, please report via [Bug Bounty](bug-bounty.md).

## High Priority

### Issue: Node Not Synchronizing After Long Disconnect

**Description:** After long disconnect, node may not synchronize automatically.

**Workaround:**

```bash
# Rebuild state
./run_node.py --datadir <DATADIR> run --rebuild-state

# Or add more peers
./run_node.py --datadir <DATADIR> run --peers peer1:9000,peer2:9000,peer3:9000
```

**Status:** 🚧 In progress

### Issue: Validator Not Activating After Staking

**Description:** Validator may not activate immediately after staking, even if stake is sufficient.

**Workaround:**

```bash
# Wait for next epoch (10 blocks for devnet, 100 for testnet)
# Check status
./cpc-cli query validators --node http://localhost:8000
```

**Status:** 🚧 In progress

## Medium Priority

### Issue: Gas Price Not Considered in Fee Calculation

**Description:** In ComputeChain 0.4.x, gas price may be ignored due to a fee calculation bug.

**Workaround:**

```bash
# Specify gas price explicitly
./cpc-cli tx send <TO> <AMOUNT> --from <FROM> --gas-price 1000
```

**Status:** 🚧 In progress

### Issue: peers.json Not Updated Automatically

**Description:** In the current MVP implementation, `peers.json` may not update when peers disconnect.

**Workaround:**

```bash
# Manually edit peers.json
nano <DATADIR>/peers.json

# Or clear and restart
rm <DATADIR>/peers.json
./run_node.py --datadir <DATADIR> run --peers peer1:9000
```

**Status:** 🚧 In progress

## Low Priority

### Issue: Logs Too Verbose

**Description:** Logs may be too detailed for production.

**Workaround:**

```bash
# Redirect logs to file
./run_node.py --datadir <DATADIR> run > node.log 2>&1

# Or use systemd with logging configuration
```

**Status:** 🚧 In progress

### Issue: Automatic Peer Reconnection Unreliable

**Description:** Automatic reconnection/backoff is still being stabilized; node may fail to reconnect after peers drop.

**Workaround:**

```bash
# Restart node
# Or add peers manually
./run_node.py --datadir <DATADIR> run --peers peer1:9000
```

**Status:** 🚧 In progress

## Fixed Issues

### Issue: Genesis Mismatch When Connecting to Network

**Status:** ✅ Fixed

**Solution:** Added `genesis_hash` check during handshake.

### Issue: Incorrect Nonce Calculation

**Status:** ✅ Fixed

**Solution:** Nonce now retrieved from node before sending transaction.

## Report Issue

If you discover a new issue, please report via [Bug Bounty](bug-bounty.md).

## Next Steps

- **[Bug Bounty](bug-bounty.md)** — Report bug
- **[Join Testnet](join.md)** — Connect to testnet
- **[Node Setup](../node/run-local.md)** — Node configuration
