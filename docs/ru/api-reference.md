# Справочник API

Справочник RPC эндпоинтов для нод ComputeChain.

**Базовый URL:** `http://localhost:8000` (изменяется флагом `--port`)

## Эндпоинты ноды

### GET /status

Получить статус ноды и текущее состояние блокчейна.

```bash
curl http://localhost:8000/status
```

**Ответ:**

```json
{
  "height": 15,
  "last_hash": "1234567890abcdef...",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```

### GET /block/{height}

Получить блок по высоте.

```bash
curl http://localhost:8000/block/10
```

**Ответ:**

```json
{
  "header": {
    "height": 10,
    "prev_hash": "abcd1234...",
    "timestamp": 1700000000,
    "proposer_address": "cpcvalcons1...",
    "compute_root": "7890abcd...",
    "tx_root": "4567efgh...",
    "state_root": "cdef1234...",
    "signature": "feedface...",
    "pub_key": "02..."
  },
  "txs": [...]
}
```

## Эндпоинты аккаунтов

### GET /balance/{address}

Получить баланс и nonce аккаунта.

```bash
curl http://localhost:8000/balance/cpc1a2b3...
```

**Ответ:**

```json
{
  "address": "cpc1a2b3...",
  "balance": "2000000000000000000000",
  "nonce": 1
}
```

**Примечание:** Баланс в wei (1 CPC = 10^18 wei)

## Эндпоинты валидаторов

### GET /validators

Список всех валидаторов с их статусом.

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
      "reward_address": "cpc1alice...",
      "name": "Alice Validator",
      "commission_rate": 0.10
    }
  ]
}
```

**Поля:**
- `address`: Консенсус адрес валидатора
- `power`: Стейк валидатора в wei
- `is_active`: Активно ли производство блоков
- `reward_address`: Куда отправляются награды за блоки
- `commission_rate`: Процент комиссии (0.0-1.0)

## Эндпоинты делегирования

### GET /delegator/{address}/delegations

Получить все делегации для адреса.

```bash
curl http://localhost:8000/delegator/cpc1abc.../delegations
```

**Ответ:**

```json
{
  "delegator": "cpc1abc...",
  "total_delegated": 100000000,
  "delegations": [
    {
      "validator": "cpcvalcons1xyz...",
      "amount": 60000000,
      "created_height": 100,
      "validator_name": "Validator A",
      "validator_commission": 0.10
    }
  ]
}
```

### GET /delegator/{address}/rewards

Получить историю наград для делегатора.

```bash
curl http://localhost:8000/delegator/cpc1abc.../rewards
```

**Ответ:**

```json
{
  "delegator": "cpc1abc...",
  "total_rewards": 125500000,
  "current_epoch": 5,
  "rewards_by_epoch": [
    {"epoch": 0, "amount": 25400000},
    {"epoch": 1, "amount": 24800000}
  ]
}
```

## Эндпоинты транзакций

### POST /tx/send

Отправить подписанную транзакцию в mempool.

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
    "signature": "abcdef1234...",
    "payload": {}
  }'
```

**Ответ (успех):**

```json
{
  "tx_hash": "1234567890abcdef...",
  "status": "received"
}
```

**Ответ (отклонено):**

```json
{
  "tx_hash": "1234567890abcdef...",
  "status": "rejected",
  "error": "Insufficient balance"
}
```

## Форматы данных

### Адреса

**Формат:** Кодировка Bech32 с префиксом

- Обычные аккаунты: `cpc1...`
- Валидаторы: `cpcvalcons1...`

**Пример:**
```
cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
cpcvalcons1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

### Суммы

**Формат:** Строковое представление в wei

**Конверсия:** 1 CPC = 10^18 wei

**Примеры:**
```
"100000000000000000000"   # 100 CPC
"1500000000000000000000"  # 1500 CPC
"21000000"                # 0.000000000021 CPC (комиссия)
```

### Хэши и ключи

**Формат:** Hex строка без префикса `0x`

**Примеры:**
```
"1234567890abcdef..."
"02a1b2c3d4e5f6g7..."
```

## Коды ошибок

| Код | Значение | Пример |
|-----|----------|--------|
| 200 | Успех | Запрос обработан успешно |
| 400 | Неверный запрос | Неверный формат транзакции |
| 404 | Не найдено | Блок не найден |
| 503 | Сервис недоступен | Нода не инициализирована |

## Примеры использования

### Мониторинг сети

```bash
# Проверить статус ноды
curl http://localhost:8000/status | jq

# Получить последнюю высоту блока
HEIGHT=$(curl -s http://localhost:8000/status | jq -r '.height')

# Получить последний блок
curl http://localhost:8000/block/$HEIGHT | jq
```

### Отслеживание валидатора

```bash
# Получить всех валидаторов
curl http://localhost:8000/validators | jq

# Получить только активных валидаторов
curl http://localhost:8000/validators | jq '.validators[] | select(.is_active == true)'

# Получить конкретного валидатора
curl http://localhost:8000/validators | jq '.validators[] | select(.address == "cpcvalcons1abc...")'
```

### Мониторинг делегаций

```bash
# Получить все делегации для адреса
curl http://localhost:8000/delegator/cpc1abc.../delegations | jq

# Получить общую сумму делегирования
curl http://localhost:8000/delegator/cpc1abc.../delegations | jq '.total_delegated'

# Проверить награды
curl http://localhost:8000/delegator/cpc1abc.../rewards | jq
```

### Отслеживание изменений баланса

```bash
# Мониторить баланс
ADDRESS="cpc1abc..."
watch -n 10 "curl -s http://localhost:8000/balance/$ADDRESS | jq"
```

## Советы по интеграции

### Пример на Python

```python
import requests

node_url = "http://localhost:8000"

# Получить баланс
def get_balance(address):
    resp = requests.get(f"{node_url}/balance/{address}")
    data = resp.json()
    balance_cpc = int(data["balance"]) / 10**18
    return balance_cpc

# Получить валидаторов
def get_active_validators():
    resp = requests.get(f"{node_url}/validators")
    data = resp.json()
    return [v for v in data["validators"] if v["is_active"]]

# Отправить транзакцию (используйте CLI для подписи)
# Используйте cpc-cli для правильной подписи транзакций
```

### Пример на JavaScript

```javascript
const nodeUrl = "http://localhost:8000";

// Получить статус
async function getStatus() {
  const resp = await fetch(`${nodeUrl}/status`);
  return await resp.json();
}

// Получить баланс в CPC
async function getBalance(address) {
  const resp = await fetch(`${nodeUrl}/balance/${address}`);
  const data = await resp.json();
  return parseInt(data.balance) / 1e18;
}
```

## Следующие шаги

- **[Справочник CLI](cli-reference.md)** - CLI команды для транзакций
- **[Гид по стейкингу](staking-guide.md)** - Стейк и делегирование
- **[Продвинутые темы](advanced.md)** - Архитектура и PoC
