# Запуск локальной ноды

Руководство по запуску локальной ноды ComputeChain для разработки и тестирования.

## Быстрый старт

### Node A (Genesis Validator)

**Терминал 1:**

```bash
cd computechain
chmod +x start_node_a.sh
./start_node_a.sh
```

**Что происходит:**

1. Очистка предыдущих данных в `.node_a/`
2. Инициализация ноды: `./run_node.py --datadir .node_a init`
3. Запуск ноды: `./run_node.py --datadir .node_a run`

**Параметры по умолчанию:**

- RPC: `http://0.0.0.0:8000`
- P2P: `0.0.0.0:9000`
- Data Dir: `.node_a/`

### Node B (Второй Валидатор)

**Терминал 2:**

```bash
cd computechain
chmod +x start_node_b.sh
./start_node_b.sh
```

**Что происходит:**

1. Проверка наличия Node A
2. Импорт ключа faucet из Node A в CLI
3. Создание ключа Alice
4. Пополнение баланса Alice (2000 CPC)
5. Стейкинг Alice (1500 CPC)
6. Экспорт ключа Alice для Node B
7. Копирование genesis.json
8. Запуск Node B с подключением к Node A

**Параметры:**

- RPC: `http://0.0.0.0:8001`
- P2P: `0.0.0.0:9001`
- Peers: `127.0.0.1:9000` (Node A)
- Data Dir: `.node_b/`

## Ручной запуск

### Инициализация ноды

```bash
./run_node.py --datadir .node_a init
```

**Что создается:**

- `genesis.json` — генезисный блок
- `validator_key.hex` — ключ валидатора (если не существует)
- `faucet_key.hex` — ключ faucet (детерминированный для devnet)
- `chain.db` — база данных блокчейна (SQLite)
- `peers.json` — список пиров (пустой при инициализации)

### Запуск ноды

```bash
./run_node.py --datadir .node_a run
```

**Параметры:**

```bash
./run_node.py --datadir .node_a run \
  --host 0.0.0.0 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers 127.0.0.1:9001
```

**Опции:**

- `--host`: RPC хост (по умолчанию: `0.0.0.0`)
- `--port`: RPC порт (по умолчанию: `8000`)
- `--p2p-host`: P2P хост (по умолчанию: `0.0.0.0`)
- `--p2p-port`: P2P порт (по умолчанию: `9000`)
- `--peers`: Список пиров через запятую (например, `127.0.0.1:9001,192.168.1.100:9000`)
- `--rebuild-state`: Пересобрать стейт из блоков при запуске

## Структура данных

### Директория ноды

```
.node_a/
├── genesis.json          # Генезисный блок
├── validator_key.hex     # Приватный ключ валидатора
├── faucet_key.hex        # Приватный ключ faucet (devnet)
├── chain.db              # База данных блокчейна (SQLite)
├── peers.json            # Список пиров (обновляется автоматически)
└── logs/                 # Логи (если настроено)
```

### Genesis.json

**Структура:**

```json
{
  "header": {
    "height": 0,
    "prev_hash": "",
    "timestamp": 1700000000,
    "proposer_address": "cpcvalcons1...",
    "compute_root": "",
    "tx_root": "",
    "state_root": ""
  },
  "txs": [
    {
      "tx_type": "TRANSFER",
      "from_address": "cpc1faucet...",
      "to_address": "cpc1faucet...",
      "amount": "1000000000000000000000000",
      ...
    }
  ]
}
```

## Логи и Мониторинг

### Вывод в консоль

**Типичные логи:**

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

### Проверка статуса

**Через RPC:**

```bash
curl http://localhost:8000/status
```

**Вывод:**

```json
{
  "height": 15,
  "last_hash": "0x1234567890abcdef...",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```

## Сетевое подключение

### Добавление пиров

**При запуске:**

```bash
./run_node.py --datadir .node_a run --peers 192.168.1.100:9000,192.168.1.101:9000
```

**Автоматически:**

- Пиры сохраняются в `peers.json`
- Автоматически подключаются при следующем запуске
- Новые пиры добавляются при рукопожатии (handshake)

### Проверка подключений

**В логах:**

```
P2P server started on 0.0.0.0:9000
Connected to peer 127.0.0.1:9001
Handshake completed with 127.0.0.1:9001
```

**Через peers.json:**

```bash
cat .node_a/peers.json
```

**Вывод:**

```json
[
  "127.0.0.1:9001",
  "192.168.1.100:9000"
]
```

## Устранение неполадок

### Ошибка: Port already in use

**Причина:** Порт занят другой нодой или процессом

**Решение:**

```bash
# Найти процесс на порту
lsof -i :8000
# Или
netstat -tulpn | grep 8000

# Остановить процесс или использовать другой порт
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

### Ошибка: Cannot connect to peers

**Причина:** Пиры недоступны или файрвол блокирует

**Решение:**

```bash
# Проверить доступность пира
telnet 192.168.1.100 9000

# Проверить файрвол
sudo ufw status
# Разрешить порт
sudo ufw allow 9000/tcp
```

## Пересборка стейта (Rebuild State)

### Когда нужно

**Случаи:**

- Повреждение стейта
- Изменение логики стейта
- Отладка

### Как выполнить

```bash
./run_node.py --datadir .node_a run --rebuild-state
```

**Что происходит:**

1. Нода загружает все блоки из базы данных
2. Применяет транзакции заново
3. Пересчитывает стейт (аккаунты, валидаторы)
4. Сохраняет новый стейт

**Время выполнения:**

- Зависит от количества блоков
- Для devnet обычно несколько секунд
- Для mainnet может занять минуты/часы

## Следующие шаги

- **[Конфигурация](config.md)** — Настройка параметров сети
- **[P2P синхронизация](p2p-sync.md)** — Синхронизация сети
- **[Руководство CLI](../cli/cpc-cli.md)** — Использование CLI

