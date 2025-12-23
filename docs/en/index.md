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

- ✅ **Tendermint BFT Consensus** - Byzantine Fault Tolerant, instant finality
- ✅ **Delegation & Rewards** - Delegate tokens, earn proportional rewards
- ✅ **Commission Model** - Validators earn commission (max 20%, configurable)
- ✅ **Validator Management** - Automated jailing for downtime
- ✅ **Slashing Protection** - Economic penalties for misbehavior (5% base rate)
- ✅ **Post-Quantum Ready** - Dilithium3 (PQ) signature scheme

## Network Info

**Devnet (Local):**
- Chain ID: `cpc-devnet-1`
- RPC: `http://localhost:8000`
- Metrics: `http://localhost:8000/metrics`

**Testnet (Coming Soon):**
- Chain ID: `cpc-testnet-1`
- RPC: TBA
- Explorer: TBA

## Support

- **GitHub:** [github.com/computechain/computechain](https://github.com/computechain/computechain)
- **Issues:** Report bugs via GitHub Issues
- **Discord:** [discord.gg/computechain](https://discord.gg/computechain)
