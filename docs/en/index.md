# ComputeChain

ComputeChain is an experimental blockchain for a useful-compute market:
users pay for computation, GPU workers execute tasks, and verified results
should determine rewards in CPC.

**Today:** a local CometBFT devnet with signed transfers, stake/delegation and tested synchronization.
It is not a production network or a finished compute marketplace.
This guide describes the current v3 checkout, as of 7 October 2026.

## Participants

- **Users:** submit transfers now; purchasing compute is planned.
- **L1 validators:** agree on blocks and execute the same application rules.
- **Full nodes:** verify/synchronize the ledger without consensus voting.
- **Compute workers:** intended to perform GPU jobs off-chain.
- **Compute evaluators:** intended to verify useful work/results. This role is
  separate from L1 validation.
- **Stakers/delegators:** lock CPC to back validators. Protocol rewards are not
  enabled yet; consensus-key ownership and withdrawals are enforced.

Compute work is not classic hash-mining Proof-of-Work and does not replace BFT
finality. Stake drives voting power; validator changes take effect at H+2.
Genesis starts with four validators, but their set is no longer fixed.

## Working versus planned

Working: canonical signed transfers/staking, delayed unbonding, verified-evidence
slashing, atomic application storage, full/catch-up
sync, verified snapshot state sync, a multi-node fault harness, load testing,
Prometheus and Grafana.

Not enabled: rewards/emission, compute submissions
and payouts, genuine PoC/ZK verification, production wallet/explorer integration.
Legacy code is not evidence that these features work in v3.

Start with [the devnet guide](devnet.md). Read [architecture](architecture.md)
for the trust model and [development](development.md) for the next priorities.
