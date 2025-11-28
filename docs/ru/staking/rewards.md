# Награды валидаторов

Валидаторы получают награды за производство блоков и комиссии за транзакции.

## Источники наград

### 1. Block Reward

**Начальная награда:** 10 CPC

**Формула:**

```python
def calculate_block_reward(height: int) -> int:
    initial_reward = 10 * 10**18  # 10 CPC
    halvings = height // 1_000_000
    reward = initial_reward >> halvings
    return reward
```

**Халвинг:**

- Каждые 1,000,000 блоков
- Награда уменьшается вдвое

**Примеры:**

| Высота блока | Награда |
|-------------|---------|
| 0 - 999,999 | 10 CPC |
| 1,000,000 - 1,999,999 | 5 CPC |
| 2,000,000 - 2,999,999 | 2.5 CPC |

### 2. Transaction Fees

**Источник:** Комиссии всех транзакций в блоке

**Расчёт:**

```python
fees_total = 0
for tx in block.txs:
    base_gas = GAS_PER_TYPE.get(tx.tx_type, 0)
    fees_total += base_gas * tx.gas_price
```

**Gas Costs:**

| Тип транзакции | Gas Cost |
|---------------|----------|
| TRANSFER | 21,000 |
| STAKE | 40,000 |
| SUBMIT_RESULT | 80,000 |

**Пример:**

```
Блок содержит:
- 5 TRANSFER транзакций (gas_price=1000)
- 1 STAKE транзакция (gas_price=1000)

Fees = (5 * 21_000 * 1000) + (1 * 40_000 * 1000)
     = 105_000_000 + 40_000_000
     = 145_000_000 wei
     = 0.000145 CPC
```

## Распределение наград

### Процесс распределения

**Триггер:** При добавлении блока

**Код:**

```python
def _distribute_rewards(self, block: Block, state: AccountState):
    proposer_addr = block.header.proposer_address
    val = state.get_validator(proposer_addr)
    
    if not val or not val.is_active:
        return  # Валидатор не активен
    
    # Определение адреса для награды
    target_addr = val.reward_address
    if not target_addr:
        # Fallback: derive from pub_key
        target_addr = address_from_pubkey(
            bytes.fromhex(val.pq_pub_key), 
            prefix="cpc"
        )
    
    acc = state.get_account(target_addr)
    
    # Расчёт награды
    block_reward = calculate_block_reward(block.header.height)
    fees_total = sum(tx.gas_limit * tx.gas_price for tx in block.txs)
    total_amount = block_reward + fees_total
    
    # Начисление
    acc.balance += total_amount
    state.set_account(acc)
```

### Адрес награды

**Приоритет:**

1. `val.reward_address` (если установлен)
2. Адрес, вычисленный из `val.pq_pub_key` с префиксом `cpc`
3. Если не удалось определить — награда не начисляется (логируется предупреждение)

**По умолчанию:**

При создании валидатора через `STAKE`:
```python
val.reward_address = tx.from_address  # Адрес отправителя
```

## Частота получения наград

### Round-Robin механизм

**Распределение блоков:**

Если в сети N активных валидаторов, каждый валидатор производит блок каждые N блоков.

**Пример (3 валидатора):**

```
Block 10: Validator A → получает награду
Block 11: Validator B → получает награду
Block 12: Validator C → получает награду
Block 13: Validator A → получает награду
...
```

**Частота:**

- Devnet (5 валидаторов): каждый 5-й блок
- Testnet (21 валидатор): каждый 21-й блок
- Mainnet (100 валидаторов): каждый 100-й блок

### Расчёт доходности

**Годовая доходность (пример для Devnet):**

```
Block Reward = 10 CPC
Block Time = 10 сек
Blocks per Year ≈ 3,153,600
Blocks per Validator per Year ≈ 3,153,600 / 5 = 630,720

Годовая награда ≈ 630,720 * 10 CPC = 6,307,200 CPC
+ Transaction Fees (зависит от активности сети)
```

**Важно:** Это упрощённый расчёт. Реальная доходность зависит от:
- Количества активных валидаторов
- Активности сети (комиссии)
- Халвинга (награда уменьшается)

## Примеры

### Пример 1: Простой блок

**Блок 15:**

```
Proposer: Validator A
Block Reward: 10 CPC
Transactions: 0
Fees: 0

Total Reward: 10 CPC → reward_address валидатора A
```

### Пример 2: Блок с транзакциями

**Блок 20:**

```
Proposer: Validator B
Block Reward: 10 CPC
Transactions:
  - TRANSFER (gas_price=1000): fee = 21_000 * 1000 = 21_000_000 wei
  - TRANSFER (gas_price=1000): fee = 21_000 * 1000 = 21_000_000 wei
  - STAKE (gas_price=1000): fee = 40_000 * 1000 = 40_000_000 wei

Fees Total: 82_000_000 wei = 0.000082 CPC

Total Reward: 10.000082 CPC → reward_address валидатора B
```

### Пример 3: Проверка баланса

**До блока:**

```bash
./cpc-cli query balance cpc1alice... --node http://localhost:8000
# Balance: 500.0 CPC
```

**После блока (Validator A произвёл блок):**

```bash
./cpc-cli query balance cpc1alice... --node http://localhost:8000
# Balance: 510.0 CPC (+10 CPC block reward)
```

## Мониторинг наград

### Проверка баланса reward_address

```bash
# Получить reward_address валидатора
./cpc-cli query validators --node http://localhost:8000 | jq '.validators[0].reward_address'

# Проверить баланс
./cpc-cli query balance <REWARD_ADDRESS> --node http://localhost:8000
```

### Логи ноды

**В логах ноды:**

```
Block 15 added. Hash: 0x1234... (Round 0)
Distributed 10000000000000000000 (Reward: 10000000000000000000, Fees: 0) to cpc1alice...
```

**Примечание:** В текущей реализации логирование наград может быть отключено для производительности.

## Будущие улучшения

### Планируется:

1. **Delegation:**
   - Стейкеры смогут делегировать токены валидаторам
   - Награды распределяются между валидатором и делегаторами

2. **Slashing:**
   - Штрафы за некорректное поведение
   - Часть стейка может быть слэшнута

3. **Комиссия валидатора:**
   - Валидатор может установить комиссию (например, 10%)
   - Остальная часть наград идёт делегаторам

## Следующие шаги

- **[Staking Basics](staking-basic)** — Основы стейкинга
- **[Validator Lifecycle](validator-lifecycle)** — Жизненный цикл валидатора
- **[Node Setup](node/run-local)** — Запуск ноды валидатора

