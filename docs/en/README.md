# ComputeChain Documentation

> Layer-1 blockchain with Proof-of-Compute (PoC) and validator staking

## Quick Start

### Install & Run Node

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize node
./run_node.py --datadir .node init

# Start node
./run_node.py --datadir .node start

# Open dashboard
open http://localhost:8000
```

### Create Wallet

```bash
# Create key
./cpc-cli keys add mykey

# Check balance
./cpc-cli query balance <YOUR_ADDRESS>
```

### Become Validator

```bash
# Stake 100 CPC (minimum)
./cpc-cli tx stake 100 --from mykey

# Check validator status
./cpc-cli query validators
```

### Delegate to Validator

```bash
# Delegate tokens to earn rewards
./cpc-cli tx delegate <VALIDATOR_ADDRESS> <AMOUNT> --from mykey

# Check your delegations
./cpc-cli query delegations <YOUR_ADDRESS>

# Check rewards
./cpc-cli query rewards <YOUR_ADDRESS>
```

## Documentation

- **[Staking Guide](staking-guide.md)** - Stake, delegate, earn rewards
- **[Validator Guide](validator-guide.md)** - Run validator, manage lifecycle
- **[CLI Reference](cli-reference.md)** - Complete CLI commands
- **[API Reference](api-reference.md)** - RPC endpoints
- **[Advanced Topics](advanced.md)** - PoC, tokenomics, architecture

## Key Features

✅ **Multi-Validator PoA** - Round-robin block production
✅ **Delegation & Rewards** - Delegate tokens, earn proportional rewards
✅ **Commission Model** - Validators earn 10% commission (configurable)
✅ **Performance Tracking** - Uptime scoring, automated jailing
✅ **Graduated Slashing** - Progressive penalties (5% → 10% → 100%)
✅ **Post-Quantum Ready** - PQ signature architecture

## Network Info

**Testnet:**
- Chain ID: `computechain-testnet-1`
- RPC: `https://rpc.testnet.computechain.space`
- Explorer: `https://explorer.testnet.computechain.space`

## Support

- **GitHub:** [github.com/computechain/computechain](https://github.com/computechain/computechain)
- **Issues:** Report bugs via GitHub Issues
- **Discord:** [discord.gg/computechain](https://discord.gg/computechain)
