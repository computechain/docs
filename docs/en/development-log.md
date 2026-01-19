# Development Log

> ComputeChain development timeline

---

## January 19, 2026 — Sync reliability and receipt indexing

Improved P2P sync (header range + snapshot chunks), added tx index fallback for receipts, and tightened state/tx determinism (tx hash fields + state_root coverage).

---

## January 12, 2026 — Final pending state fix

Fixed pending_state synchronization after local block creation. Proposer now calls `update_pending_state()` immediately after adding block to chain. This ensures correct pending nonce for subsequent transactions.

---

## January 10, 2026 — Gap-filling algorithm for nonce

Rewrote `get_pending_nonce()` using gap-filling algorithm. Now returns first missing nonce in sequence, not max+1. This prevents nonce gap accumulation and mempool deadlock.

---

## January 9, 2026 — Include queued TX in pending nonce

Fixed pending nonce calculation — now includes transactions from pending_queue, not just main pool. Without this fix `/nonce` returned 0 while 50+ TX were queued.

---

## January 8, 2026 — Ethereum-style pending state

Architectural change: mempool now manages pending state. Added `/nonce/{address}` endpoint for pending nonce. Simplified tx_generator — removed client-side NonceManager, throttling, account locks. Limit 64 queued TX per account (like Ethereum).

---

## January 6, 2026 — Proposer promotion fix

Fixed promotion logic in proposer: transactions with future nonce no longer removed from pending_queue prematurely. Promotion now correctly moves TX to main pool when blockchain nonce catches up.

---

## January 4, 2026 — Timeout settings for high load

Increased timeouts for high load mode. Smart timeout now adapts to current TPS. Raised throttling limit to prevent artificial throughput restriction.

---

## January 3, 2026 — TPS degradation fix

Fixed TPS degradation during long-running tests. Added account locks to prevent race conditions. Improved broadcast validation and balance checks. Test now holds stable 50+ TPS.

---

## December 27, 2025 — Pending queue deadlock

Fixed critical bug: promotion was called only for addresses from processed TX. With empty mempool, pending_queue was never processed → deadlock. Now promotion is called for ALL addresses in pending_queue.

---

## December 26, 2025 — Test infrastructure simplification

Removed SSE dependency from tx_generator. SSE queue increased to 10000. NonceManager switched to periodic sync instead of event-driven. Removed 167 lines of code, system became more reliable.

---

## December 25, 2025 — Cross-process EventBus

Fixed event delivery between processes. EventBus imported at module level (singleton). Added JSON serialization for SSE. Mempool now emits `tx_failed` on TTL expiry.

---

## December 23, 2025 — TX TTL and events

Implemented TTL system for transactions (1 hour). SSE endpoint `/events/stream` for real-time events. Types: `tx_confirmed`, `tx_failed`, `block_created`. Sustained TPS: ~10-30.

---

## December 22, 2025 — Prometheus metrics

Fixed metric duplication due to multiple imports. Added metrics: `accounts_total`, TX counters. Improved Grafana formatting. Created `cleanup.sh` and `start_test.sh`.

---

## December 19, 2025 — NonceManager

Implemented NonceManager class for thread-safe nonce management. Pending TX tracking, automatic recovery on confirmation, timeout handling.

---

## December 17, 2025 — Phases 1.2-1.3

**Phase 1.2:** Economic model v2 — centralized config, burn/mint tracking, 21-day unbonding period, validator commissions 0-20%.

**Phase 1.3:** State snapshots — auto-creation, gzip compression, SHA256 verification. CLI: `cpc-cli snapshot create/list`.

---

## December 17, 2025 — Phase 1.1: Delegation

Proportional reward distribution to delegators. Formula: `(stake / total) × (reward × (1 - commission))`. API `/delegator/{address}/rewards`.

---

## December 12, 2025 — Phases 1-3: Validators

**Phase 1:** Validator metadata (name, website, commission). TX `UPDATE_VALIDATOR`.

**Phase 2:** Delegation. TX `DELEGATE`/`UNDELEGATE`. Tracking `total_delegated`.

**Phase 3:** Graduated slashing (5% → 10% → 100%). `UNJAIL` mechanism (50k gas + 1000 CPC). Uptime filter 75%.

---

## December 12, 2025 — UNSTAKE mechanism

Validators can withdraw stake. 10% penalty for unstake while jailed. Auto-deactivation at power=0. TX `UNSTAKE` (40k gas).

---

## December 11, 2025 — Phase 0: Validator performance

Uptime and missed block tracking. Auto-jail after 10 missed blocks. 5% slash on jail. Performance score = 60% uptime + 20% stake + 20% penalties. Dashboard with real-time metrics.

---

## November 28, 2025 — Genesis

First ComputeChain commit. Core: blocks, TX (TRANSFER/STAKE), ECDSA signatures, nonce, gas. Consensus: multi-validator PoA, round-robin. P2P network, CLI wallet, RPC API.

---

## Statistics

- **Period:** November 2025 — January 2026
- **Current TPS:** 50-60 (stable)
- **Block time:** 5 sec
- **Tests:** 25+ (all passing)

**Last updated:** January 12, 2026
