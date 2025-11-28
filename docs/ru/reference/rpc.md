# RPC API Reference

Справочник по RPC endpoints ComputeChain ноды.

## Базовый URL

**По умолчанию:** `http://localhost:8000`

**Изменить:** Используйте параметр `--port` при запуске ноды

## Endpoints

### GET /status

**Назначение:** Получить статус ноды

**Запрос:**

```bash
curl http://localhost:8000/status
```

**Ответ:**

```json
{
  "height": 15,
  "last_hash": "0x1234567890abcdef...",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```

**Поля:**

- `height`: Высота последнего блока
- `last_hash`: Хеш последнего блока (hex строка)
- `network`: ID сети ("devnet", "testnet", "mainnet")
- `mempool_size`: Количество транзакций в мемпуле
- `epoch`: Текущая эпоха

### GET /block/{height}

**Назначение:** Получить блок по высоте

**Запрос:**

```bash
curl http://localhost:8000/block/10
```

**Ответ:**

```json
{
  "header": {
    "height": 10,
    "prev_hash": "0x...",
    "timestamp": 1700000000,
    "proposer_address": "cpcvalcons1...",
    "compute_root": "0x...",
    "tx_root": "0x...",
    "state_root": "0x...",
    "pq_signature": "0x...",
    "pq_pub_key": "02..."
  },
  "txs": [
    {
      "tx_type": "TRANSFER",
      "from_address": "cpc1...",
      "to_address": "cpc1...",
      "amount": "100000000000000000000",
      ...
    }
  ]
}
```

**Ошибки:**

- `404`: Блок не найден
- `503`: Нода не инициализирована

### GET /balance/{address}

**Назначение:** Получить баланс и nonce аккаунта

**Запрос:**

```bash
curl http://localhost:8000/balance/cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

**Ответ:**

```json
{
  "address": "cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
  "balance": "2000000000000000000000",
  "nonce": 1
}
```

**Поля:**

- `address`: Адрес аккаунта
- `balance`: Баланс в wei (строка)
- `nonce`: Номер следующей транзакции

**Ошибки:**

- `503`: Нода не инициализирована

### GET /validators

**Назначение:** Получить список валидаторов

**Запрос:**

```bash
curl http://localhost:8000/validators
```

**Ответ:**

```json
{
  "epoch": 1,
  "validators": [
    {
      "address": "cpcvalcons1alice...",
      "pq_pub_key": "02a1b2c3...",
      "power": "1500000000000000000000",
      "is_active": true,
      "reward_address": "cpc1alice..."
    },
    {
      "address": "cpcvalcons1bob...",
      "pq_pub_key": "02b2c3d4...",
      "power": "1200000000000000000000",
      "is_active": true,
      "reward_address": "cpc1bob..."
    }
  ]
}
```

**Поля:**

- `epoch`: Текущая эпоха
- `validators`: Список валидаторов
  - `address`: Консенсус-адрес валидатора (cpcvalcons...)
  - `pq_pub_key`: Публичный ключ валидатора
  - `power`: Стейк валидатора (в wei, строка)
  - `is_active`: Активен ли валидатор
  - `reward_address`: Адрес для получения наград (cpc1...)

**Ошибки:**

- `503`: Нода не инициализирована

### POST /tx/send

**Назначение:** Отправить транзакцию в мемпул

**Запрос:**

```bash
curl -X POST http://localhost:8000/tx/send \
  -H "Content-Type: application/json" \
  -d '{
    "tx_type": "TRANSFER",
    "from_address": "cpc1sender...",
    "to_address": "cpc1recipient...",
    "amount": "100000000000000000000",
    "fee": "21000000",
    "nonce": 1,
    "gas_price": 1000,
    "gas_limit": 21000,
    "timestamp": 1700000000,
    "pub_key": "02a1b2c3...",
    "signature": "0xabcdef...",
    "payload": {}
  }'
```

**Ответ (успех):**

```json
{
  "tx_hash": "0x1234567890abcdef...",
  "status": "received"
}
```

**Ответ (отклонено):**

```json
{
  "tx_hash": "0x1234567890abcdef...",
  "status": "rejected",
  "error": "Insufficient balance"
}
```

**Поля ответа:**

- `tx_hash`: Хеш транзакции (hex строка)
- `status`: Статус ("received" или "rejected")
- `error`: Сообщение об ошибке (если отклонено)

**Ошибки:**

- `400`: Неверный формат транзакции
- `503`: Нода не инициализирована

## Форматы данных

### Адреса

**Формат:** Bech32 с префиксом

- Аккаунты: `cpc1...`
- Валидаторы: `cpcvalcons1...`

**Примеры:**

```
cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
cpcvalcons1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

### Суммы

**Формат:** Строка с числом в wei

**Примеры:**

```
"100000000000000000000"  # 100 CPC
"1500000000000000000000"  # 1500 CPC
```

### Хеши

**Формат:** Hex строка с префиксом "0x"

**Примеры:**

```
"0x1234567890abcdef..."
"0xabcdef1234567890..."
```

### Публичные ключи

**Формат:** Hex строка без префикса

**Примеры:**

```
"02a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
```

## Коды ошибок

### 200 OK

Успешный запрос

### 400 Bad Request

Неверный формат запроса или данных

**Пример:**

```json
{
  "detail": "Invalid transaction format"
}
```

### 404 Not Found

Ресурс не найден

**Пример:**

```json
{
  "detail": "Block not found"
}
```

### 503 Service Unavailable

Нода не инициализирована

**Пример:**

```json
{
  "detail": "Node not initialized"
}
```

## Примеры использования

### Пример 1: Проверка статуса

```bash
curl http://localhost:8000/status | jq
```

### Пример 2: Получение баланса

```bash
ADDRESS="cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t"
curl http://localhost:8000/balance/$ADDRESS | jq
```

### Пример 3: Получение блока

```bash
HEIGHT=10
curl http://localhost:8000/block/$HEIGHT | jq '.header'
```

### Пример 4: Получение валидаторов

```bash
curl http://localhost:8000/validators | jq '.validators[] | select(.is_active == true)'
```

### Пример 5: Отправка транзакции (через CLI)

```bash
./cpc-cli tx send cpc1recipient... 100 --from alice --node http://localhost:8000
```

## Следующие шаги

- **[Transaction Types](tx-types)** — Типы транзакций
- **[Glossary](glossary)** — Терминология
- **[CLI Guide](cli/cpc-cli)** — Использование CLI

