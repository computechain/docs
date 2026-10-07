# Приоритеты разработки

## Что делать дальше

Выполнено: полный baseline зелёный, целочисленная devnet-экономика описана,
staking/delegation управляет native ABCI validator updates. Дальше:

1. **Проверить динамические валидаторы под отказами.** Offline/catch-up, потеря
   quorum, snapshot restore, crash/replay и длительные прогоны. Затем — ноды на
   нескольких LAN-хостах; нынешние пять нод всё ещё работают на одном хосте.
2. **Реализовать проверяемые полезные вычисления.** Сначала tasks, result verification,
   scoring и payout rules; только потом включать compute submissions. После —
   адаптация wallet/explorer и проверка production-эксплуатации.

Это приоритеты, не даты релизов и не готовые функции. BFT-голосование не должно
зависеть от локального мнения оператора о полезности GPU-работы.

## Основные проверки

Из репозитория блокчейна:

```bash
./run_tests.sh -q
./run_tests.sh tests/test_security.py tests/test_comet.py tests/test_staking.py tests/test_devnet_tools.py ../monitoring/tests -q
```

Запускайте полный core suite и cross-repository tooling checks во временном storage.

Fault harness запускается в **новом** каталоге:

```bash
../.tools/blockchain-venv/bin/python scripts/comet_devnet.py verify --dir /root/computechain/.runtime/comet-fault-new --base-port 30600
```

Выберите свободный диапазон; этот каталог нельзя повторно использовать для verify.
Harness проверяет full/catch-up/verified state sync, прогресс при 3/4 мощности,
остановку/healing partition 2+2, согласие шести узлов, native H+2 вступления,
делегацию, выход валидатора и оба срока unbonding. Затем останавливает свои
процессы, не удаляя данные. Отчёт — `<devnet>/verification.json`.

## Ответственность репозиториев

- `computechain`: protocol/application, launcher, load и fault tests.
- `monitoring`: сбор метрик, Prometheus, Grafana.
- `docs`: эта компактная английская/русская документация.
- `explorer`: read-only Comet v3 observer, собственный SQLite index и Next.js UI;
  не wallet и не независимый light client. `website`: локальный EN/RU обзор.

Исходники — источник истины. При изменении поведения обновляйте оба языка;
экспериментальные цифры и отключённые функции явно отмечайте. Старые инструкции
доступны в истории Git, а не выдаются за актуальную функциональность.
