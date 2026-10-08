# Запуск стенда

## Каталоги и зависимости

Репозитории должны лежать рядом в одном workspace, например:

```text
computechain/
  computechain/   # блокчейн
  monitoring/    # Prometheus + Grafana
  docs/          # эта документация
```

Для полного стека нужны Linux, Python 3.12, pip, работающий Docker Engine и Compose.
Локальные инструменты блокчейна устанавливаются один раз:

```bash
cd /root/computechain/computechain
python3 scripts/setup_comet.py
```

Установка идёт в `.tools/` родительского workspace, не глобально.
На текущем хосте разработки инструменты уже установлены.

## Запуск и остановка

```bash
./start_test.sh
./start_test.sh status
./cleanup.sh
```

Запускаются **4 валидатора равной мощности + 1 full node** и мониторинг.
Повторный запуск сохраняет исправный работающий стенд. Остановка сохраняет ключи,
историю, signing state, логи и monitoring volumes. При частичном старте сначала
проверьте состояние, затем выполните safe stop/start; чужие процессы не заменяются.

Данные по умолчанию: `/root/computechain/.runtime/comet-staking-devnet/`.
Для restart нельзя удалять или откатывать validator signing state.
Отдельный эксперимент создавайте с новым `--dir`.

Без Docker: `./start_test.sh up --no-monitoring --no-docs --no-web`.
Мониторинг можно добавить позже: `./start_test.sh monitoring-up`.

## Мониторинг по локальной сети

На текущем хосте:

- [Grafana — WAN fleet](http://192.168.0.100:3000/d/computechain-fleet)
- [Prometheus](http://192.168.0.100:9090)

SSH-туннель не нужен. Launcher определяет и сохраняет private LAN IPv4;
можно указать его явно: `--monitoring-host 192.168.0.100`.
Логин Grafana — `admin`; случайный пароль хранится в
`/root/computechain/.runtime/comet-staking-devnet/monitoring/monitoring.env` (0600).
С прежней учётной записью/volumes теперь наблюдается `cpc-multisite-devnet-1`, все
семь узлов. Remote observations идут через pinned TLS readers; native metrics/ABCI
измеряются только локально. TPS/supply не суммируются по репликам. Alerts видны
в Grafana/Prometheus, внешние уведомления не настроены. Explorer/website тоже
наблюдают WAN chain через full-a1 с отдельным genesis-bound индексом; старая история
сохранена. Команды load ниже всё ещё нагружают старую локальную цепь, не WAN fleet.

Grafana/Prometheus привязаны к выбранному LAN-адресу для доверенной локальной сети.
Grafana требует входа; у Prometheus нет LAN-аутентификации. Не пробрасывайте эти
HTTP-сервисы в Интернет. NAT не делает клиентов локальной сети доверенными.
Native ABCI/RPC и exporters остаются loopback; WAN P2P имеет отдельные scoped ACL.

## Нагрузка подписанными переводами

```bash
./start_test.sh load --mode medium --duration 60
./start_test.sh load-stop
```

Цели low/medium/high — 3/25/100 TPS. Свой режим:
`./start_test.sh load --tps 50 --duration 600 --accounts 16 --window 8`.
Цель не гарантирует throughput: короткий локальный high-прогон показал около
36 confirmed TPS; это не тест предельной мощности или 24-часовой стабильности.

Генератор отправляет только TRANSFER. Отдельные кошельки — в `<devnet>/load-wallets/`;
личный keystore не используется. Funding идёт до sending duration; при остановке
даётся до 30 секунд на drain. Одновременно разрешён один generator/faucet writer.
После завершения нагрузки ноды продолжают работать.

## Состояние и диагностика

```bash
./start_test.sh status
./start_test.sh monitoring-status
tail -f ../.runtime/comet-staking-devnet/load.log
```

В `load-latest.json` отдельно считаются отправленные, подтверждённые, отклонённые,
ошибки исполнения/RPC и unresolved. Приём в mempool не считается успехом.
Логи: `appN.log`, `engineN.log`, `exporter.log`, `load.log`.
В мониторинге должно быть 7 healthy targets: 5 Comet-нод, exporter, Prometheus.

Другой стенд настраивается через `--dir`, `--base-port`, `--grafana-port`,
`--prometheus-port`; нужен свободный диапазон блокчейна от base до base+145.
Существующий каталог использует сохранённые network/monitoring settings.
Подробности реализации — в `COMETBFT.md` репозитория блокчейна.

## Локальные интерфейсы

- [Сайт](http://192.168.0.100:8080/): EN/RU обзор и наблюдаемый статус сети.
- [Explorer](http://192.168.0.100:4000/): native blocks/TX, аккаунты, валидаторы и поиск.
- [Документация](http://192.168.0.100:8008/) / [русская версия](http://192.168.0.100:8008/ru/).

Обычный `up` включает все три. Команды: `docs-up`, `website-up`, `explorer-up`
и варианты `-down`, `-status`, `-logs`; они не перезапускают цепь. После правки
Markdown повторите `docs-up`. `cleanup.sh` останавливает интерфейсы, сохраняя
данные. `--no-docs` / `--no-web` пропускают запуск; `--docs-port`, `--website-port`,
`--explorer-port` выбирают UI-порты. В LAN открыты только read-only UI gateways;
explorer backend/frontend и native RPC остаются loopback.
Explorer — наблюдатель, не независимое доказательство: высота индекса и текущего
account state могут различаться и явно показаны в интерфейсе.

## Новый follower через state sync

Отдельный multisite devnet из семи узлов работает на трёх хостах; прежний стенд/UI
не изменён. Управление на каждом хосте: `sudo ~/computechain-node/node.sh status`
(`up`, `down`, `logs`; можно добавить имя узла). Данные/ключи остаются в этом каталоге.
Межлокационный P2P теперь идёт по белым WAN-адресам; WG остаётся для администрирования.
Проверены full sync, mesh всех6узлов, переводы и рестарты; genesis, keys и история
сохранены. Проброшены P2P и ограниченные TLS readers27626/27636, никогда native
RPC/ABCI/мониторинг. Новый full-a3 восстановил snapshot через WAN примерно за14s;
block/AppHash, балансы и nonce совпали у всех семи узлов. Рестарт после expiry
checkpoint прошёл без нового доверия или замены ключей/данных. Работают четыре
валидатора и три full nodes. Физические отказы и длительную стабильность ещё
предстоит проверить. Это не production.
Checkpoint действует30s; validator/history reset и публикации native RPC нет.
Подробности: core `MULTISITE.md`.

Из core repository, при работающей собственной локальной сети:

```bash
./start_test.sh checkpoint --checkpoint ../.runtime/comet-staking-devnet/checkpoint-01.json --witnesses 0 1 2
./start_test.sh state-sync --node 5 --checkpoint ../.runtime/comet-staking-devnet/checkpoint-01.json --witnesses 0 1 2
```

Выбирайте новое имя: export не перезаписывает anchor. Тестовый trust window —
всего 30 секунд; после expiry нужен свежий доверенный файл, не увеличение срока.
Допускаются только свежие non-genesis followers; история/signing state сохраняются.
Неудачный partial bootstrap требует инспекции, не автоматического reset.
Обычные offline-ноды используют restart/catch-up. Отчёт —
`<devnet>/state-sync-nodeN.json`; совпадение RPC-ответов не удостоверяет checkpoint.

## Stake и делегирование тестовых средств

```bash
./start_test.sh stake --validator-node 4 --amount 6000000000000000000000
./start_test.sh delegate --validator-node 4 --amount 100000000000000000000
./start_test.sh undelegate --validator-node 4 --amount 100000000000000000000
./start_test.sh unstake --validator-node 4 --amount 6000000000000000000000
```

Суммы — базовые единицы: здесь 6 000 и 100 CPC. Stake подписывается локальным
owner-ключом ноды, funding автоматически идёт из devnet faucet. Делегирует faucet.
Перед командами остановите load. Native updates действуют с H+2; вывод требует
H+2+100 блоков И 60 секунд. V2 не мигрируется: перед v3 на тех же портах
остановите старый стенд явно:
`./cleanup.sh --dir /root/computechain/.runtime/comet-devnet`.
Ключи, данные и старые monitoring volumes сохраняются.
