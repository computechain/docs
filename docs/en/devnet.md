# Run the devnet

## Layout and prerequisites

Clone sibling repositories under one workspace, for example:

```text
computechain/
  computechain/   # blockchain
  monitoring/    # Prometheus + Grafana
  docs/          # this guide
```

Linux, Python 3.12, pip, and a running Docker Engine with Compose are required
for the complete stack. Install local chain tools once:

```bash
cd /root/computechain/computechain
python3 scripts/setup_comet.py
```

The setup installs into the parent workspace's `.tools/`, not globally.
The toolchain is already installed on the current development host.

## Start and stop

```bash
./start_test.sh
./start_test.sh status
./cleanup.sh
```

Start runs **4 equal-power validators + 1 full node** and monitoring.
Repeated start preserves a healthy running stand. Stop preserves keys, chain
data, signing state, logs and monitoring volumes. A partial startup requires
inspection, then safe stop/start; the script does not replace arbitrary processes.

Default data directory: `/root/computechain/.runtime/comet-staking-devnet/`.
Never delete or roll back validator signing state to restart.
For an independent experiment, choose a new `--dir`.

Without Docker: `./start_test.sh up --no-monitoring --no-docs --no-web`.
Add monitoring later with `./start_test.sh monitoring-up`.

## Open monitoring over LAN

On the current host:

- [Grafana — WAN fleet](http://192.168.0.100:3000/d/computechain-fleet)
- [Prometheus](http://192.168.0.100:9090)

No SSH tunnel is needed. The launcher detects/saves the private LAN IPv4 address;
override it with `--monitoring-host 192.168.0.100`.
Grafana login is `admin`; its generated password is in
`/root/computechain/.runtime/comet-staking-devnet/monitoring/monitoring.env` (0600).
The existing account/volumes now monitor `cpc-multisite-devnet-1`, all seven nodes.
Remote observations use pinned TLS readers; native metrics/ABCI are local only.
TPS/supply are not summed across replicas. Alerts are visible in Grafana/Prometheus;
external notifications are not configured. Explorer/website now also observe the
WAN chain through full-a1, with a separate genesis-bound index; old history remains.
Local load commands below still target the old local chain, not the WAN fleet.

Grafana/Prometheus are available to the trusted LAN only by binding that address.
Grafana requires login; Prometheus has no LAN authentication. Do not port-forward
these HTTP services to the Internet. NAT does not make LAN clients trusted.
Native ABCI/RPC and metrics exporters stay loopback; WAN P2P uses separate scoped ACLs.

## Generate signed transfers

```bash
./start_test.sh load --mode medium --duration 60
./start_test.sh load-stop
```

Modes target 3/25/100 TPS for low/medium/high. Custom:
`./start_test.sh load --tps 50 --duration 600 --accounts 16 --window 8`.
Target is not guaranteed throughput: a short local high run observed about
36 confirmed TPS, not a capacity or 24-hour stability benchmark.

The load generator sends TRANSFER only. Separate wallets live in `<devnet>/load-wallets/`;
the personal keystore is untouched. Funding precedes the sending duration;
shutdown drains pending transactions for up to 30 seconds. One generator/faucet
writer is allowed at a time. Nodes remain running after load finishes.

## Status and troubleshooting

```bash
./start_test.sh status
./start_test.sh monitoring-status
tail -f ../.runtime/comet-staking-devnet/load.log
```

`load-latest.json` separates submitted, confirmed, rejected, execution failures,
RPC uncertainty and unresolved transactions. Admission to mempool is not success.
Logs are `appN.log`, `engineN.log`, `exporter.log` and `load.log`.
Monitoring should show 7 healthy targets: 5 Comet nodes, exporter, Prometheus.

For another stand use `--dir`, `--base-port`, `--grafana-port` and
`--prometheus-port`; reserve the whole blockchain range, base through base+145.
Existing directories use their saved network/monitoring settings.
For implementation details see the blockchain repository's `COMETBFT.md`.

## Local interfaces

- [Website](http://192.168.0.100:8080/): EN/RU overview and observed network status.
- [Explorer](http://192.168.0.100:4000/): native blocks/transactions, accounts, validators and search.
- [Docs](http://192.168.0.100:8008/) / [Russian docs](http://192.168.0.100:8008/ru/).

Normal `up` starts all three. Each has `docs-up`, `website-up`, `explorer-up`
and matching `-down`, `-status`, `-logs` commands; these do not restart the chain.
Run `docs-up` to rebuild after editing Markdown. `cleanup.sh` stops all interfaces
and preserves data. `--no-docs` / `--no-web` skip startup; `--docs-port`,
`--website-port`, `--explorer-port` select UI ports. Only read-only UI gateways
bind LAN; explorer processes and native RPC remain loopback.
Explorer is an observer, not independent proof: indexed-history totals and
account state may have different heights, clearly shown in its banner.

## Bootstrap a fresh state-sync follower

A separate seven-node multisite devnet runs across three hosts; the original local
stand/UI is unchanged. Per-host controls: `sudo ~/computechain-node/node.sh status`
(`up`, `down`, `logs`; optional node name). Data/keys stay in that home directory.
Cross-location P2P now uses public WAN endpoints; WG remains for administration.
Full sync, six-node peer mesh, transfers and validator restarts passed; genesis,
keys and history are preserved. P2P and restricted TLS readers27626/27636 are
forwarded, never native RPC/ABCI or monitoring. New full-a3 restored a snapshot
over WAN in about14s; block/AppHash, balances and nonces matched all seven nodes.
It restarted after checkpoint expiry without new trust or replacing keys/data.
Four validators and three full nodes remain running. Physical outage tests and
long-duration stability remain pending.
Checkpoints expire after30s; no validator/history reset or native RPC exposure.
This is not production readiness. Details: core `MULTISITE.md`.

From the core repository, while the controlled local network is running:

```bash
./start_test.sh checkpoint --checkpoint ../.runtime/comet-staking-devnet/checkpoint-01.json --witnesses 0 1 2
./start_test.sh state-sync --node 5 --checkpoint ../.runtime/comet-staking-devnet/checkpoint-01.json --witnesses 0 1 2
```

Use a new filename: export never overwrites an anchor. The 30-second test trust
window is intentionally short; expired anchors require a fresh trusted file,
not a larger trust period. Only fresh non-genesis followers are accepted; existing
history/signing state is preserved. Failed partial bootstrap requires inspection,
not automatic reset. Normal offline nodes use restart/catch-up. State-sync reports
are `<devnet>/state-sync-nodeN.json`; agreement alone is not checkpoint authenticity.

## Stake and delegate (local test funds)

```bash
./start_test.sh stake --validator-node 4 --amount 6000000000000000000000
./start_test.sh delegate --validator-node 4 --amount 100000000000000000000
./start_test.sh undelegate --validator-node 4 --amount 100000000000000000000
./start_test.sh unstake --validator-node 4 --amount 6000000000000000000000
```

Amounts are base units: these examples use 6,000 and 100 CPC. Stake uses the
node's local owner key and automatically funds it from the devnet faucet;
delegation uses the faucet. Stop load before these commands. Native updates
activate at H+2. Withdrawals return only after H+2+100 blocks AND 60 seconds.
Old v2 data is not migrated: stop the old stand explicitly with
`./cleanup.sh --dir /root/computechain/.runtime/comet-devnet` before starting v3
on the same ports. Keys, data and old monitoring volumes remain intact.
