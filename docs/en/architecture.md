# Architecture and trust

## Two processes per node

**CometBFT** handles P2P, block proposals/votes, BFT commits, block synchronization
and light-client verification for state sync.

**The CPC ABCI application** verifies transactions, executes deterministic state
transitions and commits balances, nonces, metadata and receipts to SQLite.
The engine talks to it over privileged local gRPC. ABCI is not a public API.

Finalization requires **strictly more than 2/3 of voting power**.
The safety model assumes Byzantine power below 1/3; progress also needs sufficient
honest online power and suitable network conditions. With four equal validators,
one offline node permits progress; a 2+2 partition stops both halves.

GPU work belongs to the future off-chain compute layer, not consensus execution.

## Current token/transaction rules

- Chain ID: `cpc-comet-staking-devnet-1` for this local harness.
- 1 CPC = 10^18 base units.
- Genesis: 1,000,000 test CPC total; 40,000 bonded, 4,000 liquid owner funds,
  956,000 faucet funds. No real asset migration.
- Signed TRANSFER, STAKE/UNSTAKE, DELEGATE/UNDELEGATE, UPDATE_VALIDATOR.
- Transfer gas is 21,000; other types have fixed gas; minimum price is 1,000.
- Fees are burned; no block rewards or new minting are active.

These are devnet rules, not approved final tokenomics. Self-stake minimum: 1,000
CPC; delegation minimum: 10 CPC. Voting power = floor(bonded CPC), provided self
stake meets the minimum. New increases cannot exceed 20% of total power; genesis
25% shares cannot be increased while above this cap. Unbond releases only after
H+2+100 blocks AND 60 seconds. Native evidence expires after both 20 blocks and
30 seconds; 5% of liable cohorts is burned and the key permanently tombstoned.
Commission changes: max 20%, +5 percentage points, 100-block cooldown and
20-block announcement. No rewards are paid yet. Consensus keys require an
owner/chain-bound Ed25519 possession proof. These short timings are local tests,
not production settings. Full rules: core `blockchain/comet/ECONOMICS.md`.

Transfer signatures use secp256k1 ECDSA; native consensus keys use Ed25519.
The signature commits canonical fields, version, chain ID and signing domain.
No post-quantum security or genuine ZK verification is claimed.

## Storage and synchronization

Application state includes balances, nonces, height, block hash, supply/burn and
fee policy, stake cohorts, unbonding, commissions and historical validator sets.
Its AppHash commits the entire canonical state. The block header at
H+1 contains the application hash after execution of H.

Proposal/CheckTx simulations do not change committed state. SQLite commits state,
height, receipts and snapshots atomically; a writer lock excludes a second writer.
This protects crash recovery, not an arbitrary rollback of signing state.

Full sync starts from genesis. Catch-up restores an offline node. State sync uses
a trusted checkpoint and native verified headers/AppHash before accepting a
bounded snapshot. A file checksum alone is not trust. Current checkpoints are
chosen from locally controlled nodes; public bootstrap trust is not solved.
Local trust period is 30 seconds, below the 60-second unbonding floor.

Native RPC is on the host at `127.0.0.1:28601` by default (`/status`, `/block`,
`/tx`, `/abci_query`). Current application query paths are `/state` and
`/account/<address>`, `/validators`, `/unbondings/<address>`; query Merkle proofs/historical state are not implemented.

## Legacy boundary

The old Python consensus, FastAPI API and staking CLI are not the v3
integration. Unverified PoC submissions/payouts and unscheduled commission changes
are disabled. Legacy network startup requires an explicit unsafe opt-in.

Do not silently import v1/v2 history, balances or keys into v3. Migration and
production deployment need a separate specification and review.
