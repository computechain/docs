# Архитектура и доверие

## Два процесса на ноду

**CometBFT** отвечает за P2P, предложения блоков/голоса, BFT commits, синхронизацию
истории и light-client verification при state sync.

**CPC ABCI-приложение** проверяет транзакции, детерминированно исполняет изменения
и сохраняет balances, nonces, metadata и receipts в SQLite.
Движок обращается к нему через привилегированный локальный gRPC. ABCI — не публичный API.

Финализация требует **строго больше 2/3 voting power**.
Безопасность предполагает Byzantine power меньше 1/3; прогресс также требует
достаточной честной online-мощности и подходящих сетевых условий. При четырёх
равных валидаторах отключение одного допускает прогресс; partition 2+2 останавливает
обе половины.

GPU-работа относится к будущему off-chain compute-слою, не к consensus execution.

## Текущие правила токена и переводов

- Chain ID локального стенда: `cpc-comet-staking-devnet-1`.
- 1 CPC = 10^18 базовых единиц.
- Genesis: всего 1 000 000 тестовых CPC; 40 000 в stake, 4 000 на балансах
  владельцев и 956 000 у faucet. Реальные активы не мигрируются.
- Подписанные TRANSFER, STAKE/UNSTAKE, DELEGATE/UNDELEGATE, UPDATE_VALIDATOR.
- Gas перевода — 21 000; другие типы имеют фиксированный gas; minimum price — 1 000.
- Комиссии сжигаются; block rewards и новая эмиссия не включены.

Это devnet, не окончательная токеномика. Минимумы: self stake — 1 000 CPC,
делегация — 10 CPC. Power = floor(bonded CPC), если self stake достиг минимума.
Увеличения не могут превышать 20% общей мощности; genesis-доли 25% нельзя
увеличивать, пока они выше лимита. Вывод — только после H+2+100 блоков И 60 секунд.
Native evidence истекает после ОБОИХ сроков: 20 блоков и 30 секунд. Штраф — 5%
ответственных cohorts и постоянное исключение ключа. Комиссия: максимум 20%,
шаг +5 процентных пунктов, cooldown 100 блоков, объявление за 20 блоков.
Наград пока нет. Consensus key требует Ed25519 proof владения, связанного с
owner/chain ID. Короткие сроки — для локальных тестов, не production.
Полные правила: core `blockchain/comet/ECONOMICS.md`.

Подписи переводов — secp256k1 ECDSA; native consensus keys — Ed25519.
Подпись фиксирует canonical поля, версию, chain ID и signing domain.
Постквантовая защита и настоящая ZK-проверка не заявляются.

## Хранение и синхронизация

Application state включает balances, nonces, height, block hash, supply/burn и
fee policy, stake cohorts, unbonding, комиссии и историю validator sets. AppHash фиксирует всё canonical состояние. Header блока H+1 содержит
application hash после исполнения H.

Proposal/CheckTx-симуляции не меняют committed state. SQLite атомарно записывает
state, height, receipts и snapshots; writer lock исключает второго writer.
Это защита crash recovery, не разрешение откатывать signing state.

Full sync начинает от genesis. Catch-up догоняет историю после offline. State sync
проверяет native headers/AppHash от trusted checkpoint до приёма bounded snapshot.
Checksum файла сам по себе не создаёт доверия. Сейчас checkpoints выбираются
из собственных локальных нод; доверенный bootstrap публичной сети ещё не решён.
Локальный trust period — 30 секунд, меньше минимальных 60 секунд unbonding.

Native RPC на хосте по умолчанию — `127.0.0.1:28601` (`/status`, `/block`,
`/tx`, `/abci_query`). Application queries: `/state`, `/account/<address>`, `/validators`, `/unbondings/<address>`;
query Merkle proofs и historical state пока не реализованы.

## Граница legacy

Старые Python consensus, FastAPI API и staking CLI не являются
интеграцией v3. Непроверенные PoC submissions/payouts и несогласованные изменения
комиссии отключены. Legacy network запускается только с явным unsafe opt-in.

V1/v2-история, balances и ключи не импортируются в v3 автоматически. Для миграции и
production deployment нужны отдельная спецификация и проверка.
