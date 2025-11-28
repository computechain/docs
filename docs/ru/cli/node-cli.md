# Node CLI (run_node.py)

Команды для управления нодой ComputeChain: инициализация, запуск, конфигурация.

## Команды

### Init — Инициализация ноды

```bash
./run_node.py --datadir <DIR> init
```

**Пример:**

```bash
./run_node.py --datadir .node_a init
```

**Что создаётся:**

- `genesis.json` — генезисный блок
- `validator_key.hex` — ключ валидатора (если не существует)
- `faucet_key.hex` — ключ faucet (детерминированный для devnet)
- `chain.db` — база данных блокчейна (SQLite)
- `peers.json` — список пиров (пустой)

**Вывод:**

```
Node initialized in .node_a
```

### Run — Запуск ноды

```bash
./run_node.py --datadir <DIR> run [OPTIONS]
```

**Пример:**

```bash
./run_node.py --datadir .node_a run
```

**Опции:**

- `--host <HOST>`: RPC хост (по умолчанию: `0.0.0.0`)
- `--port <PORT>`: RPC порт (по умолчанию: `8000`)
- `--p2p-host <HOST>`: P2P хост (по умолчанию: `0.0.0.0`)
- `--p2p-port <PORT>`: P2P порт (по умолчанию: `9000`)
- `--peers <PEERS>`: Список пиров через запятую (например: `127.0.0.1:9001,192.168.1.100:9000`)
- `--rebuild-state`: Пересобрать стейт из блоков при запуске

**Пример с опциями:**

```bash
./run_node.py --datadir .node_a run \
  --host 0.0.0.0 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers 127.0.0.1:9001
```

**Вывод:**

```
Starting ComputeChain node...
Data DB: .node_a/chain.db
RPC: 0.0.0.0:8000
P2P: 0.0.0.0:9000
Node initialized in .node_a
Starting P2P node...
P2P server started on 0.0.0.0:9000
RPC server started on 0.0.0.0:8000
Block 0 added. Hash: 0x1234... (Round 0)
Block 1 added. Hash: 0x5678... (Round 0)
...
```

## Примеры использования

### Пример 1: Локальная разработка (Node A)

```bash
./run_node.py --datadir .node_a init
./run_node.py --datadir .node_a run
```

### Пример 2: Второй валидатор (Node B)

```bash
# После настройки через start_node_b.sh
./run_node.py --datadir .node_b run \
  --port 8001 \
  --p2p-port 9001 \
  --peers 127.0.0.1:9000
```

### Пример 3: Подключение к тестнету

```bash
./run_node.py --datadir .testnet_node run \
  --peers testnet-peer-1:9000,testnet-peer-2:9000,testnet-peer-3:9000
```

### Пример 4: Пересборка стейта

```bash
./run_node.py --datadir .node_a run --rebuild-state
```

**Когда использовать:**

- Повреждение стейта
- Изменение логики стейта
- Отладка

## Структура данных

### Директория ноды

```
<datadir>/
├── genesis.json          # Генезисный блок
├── validator_key.hex     # Приватный ключ валидатора
├── faucet_key.hex        # Приватный ключ faucet (devnet)
├── chain.db              # База данных блокчейна (SQLite)
└── peers.json            # Список пиров
```

## Логи

### Вывод в консоль

**Типичные логи:**

- Инициализация компонентов
- Подключения к пирам
- Производство блоков
- Ошибки валидации

**Пример:**

```
Starting ComputeChain node...
Data DB: .node_a/chain.db
RPC: 0.0.0.0:8000
P2P: 0.0.0.0:9000
Node initialized in .node_a
Starting P2P node...
P2P server started on 0.0.0.0:9000
RPC server started on 0.0.0.0:8000
Connected to peer 127.0.0.1:9001
Handshake completed with 127.0.0.1:9001
Block 0 added. Hash: 0x1234... (Round 0)
Block 1 added. Hash: 0x5678... (Round 0)
```

### Конфигурация логирования

**Текущая реализация:** Логи выводятся в консоль

**Будущая реализация:** Конфигурация через файл конфигурации

## Устранение неполадок

### Ошибка: Port already in use

**Причина:** Порт занят

**Решение:**

```bash
# Использовать другой порт
./run_node.py --datadir .node_a run --port 8002
```

### Ошибка: Database locked

**Причина:** Другая нода использует ту же базу данных

**Решение:**

- Убедитесь, что только одна нода использует `--datadir .node_a`
- Используйте разные директории для разных нод

### Ошибка: Genesis mismatch

**Причина:** Разные genesis.json у нод

**Решение:**

```bash
# Скопировать genesis.json от первой ноды
cp .node_a/genesis.json .node_b/genesis.json
```

## Следующие шаги

- **[Запуск локально](../node/run-local.md)** — Подробное руководство по запуску
- **[Конфигурация](../node/config.md)** — Настройка параметров
- **[P2P синхронизация](../node/p2p-sync.md)** — Синхронизация с сетью
