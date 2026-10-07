# Development priorities

## What to do next

Completed: the full baseline is green, integer devnet economics are specified,
and staking/delegation drives native ABCI validator updates. Next:

1. **Test changing validator sets under faults.** Offline/catch-up, quorum loss,
   snapshot restore, crash/replay and long runs. Multi-host LAN nodes come next;
   the current five-node stand is still on one host.
2. **Build verified useful computation.** Define tasks, result verification,
   scoring and payout rules before enabling compute submissions. Then adapt
   wallet/explorer and evaluate production operations.

These are priorities, not release dates or completed features. BFT voting must
not depend on an operator's local opinion of GPU usefulness.

## Essential checks

From the blockchain repository:

```bash
./run_tests.sh -q
./run_tests.sh tests/test_security.py tests/test_comet.py tests/test_staking.py tests/test_devnet_tools.py ../monitoring/tests -q
```

Run both the full core suite and cross-repository tooling checks in scratch storage.

The fault harness must use a **new** directory:

```bash
../.tools/blockchain-venv/bin/python scripts/comet_devnet.py verify --dir /root/computechain/.runtime/comet-fault-new --base-port 30600
```

Reserve a free range and do not reuse that directory for a second verify run.
The harness tests full/catch-up/verified state sync, 3/4 progress, 2+2 halt/healing
and agreement of six nodes, then native H+2 joins, delegation, validator exit and
both unbond gates. It stops its processes without deleting data.
The report is `<devnet>/verification.json`.

## Repository responsibilities

- `computechain`: protocol/application, local launcher, load and fault tests.
- `monitoring`: collection, Prometheus, Grafana.
- `docs`: this compact English/Russian guide.
- `explorer`: read-only Comet v3 observer with its own SQLite index and Next.js UI;
  not a wallet or independent light client. `website`: EN/RU local overview.

Source is authoritative. Update both languages when behavior changes; keep
experimental numbers and disabled features clearly labelled. Old instructions
are recoverable from Git history, not presented as current functionality.
