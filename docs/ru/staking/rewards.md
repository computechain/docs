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

**Логика распределения:**

1. **Расчёт общей награды:** `total_reward = block_reward + transaction_fees`
2. **Проверка делегаций:**
   - Если у валидатора есть делегации → применяется комиссия
   - Если делегаций нет → валидатор получает 100%

### Без делегаций

Валидатор получает полную награду:

```python
total_reward = block_reward + fees_total
validator_account.balance += total_reward
```

### С делегациями и комиссией

**Модель комиссии (по умолчанию: 10%):**

```python
# У валидатора есть делегации
commission_amount = int(total_reward * validator.commission_rate)  # 10%
delegators_share = total_reward - commission_amount  # 90%

# Валидатор получает комиссию
validator_account.balance += commission_amount

# Делегаторы получают пропорциональную долю
for delegation in validator.delegations:
    delegator_reward = (delegators_share * delegation.amount) // validator.total_delegated
    delegator_account.balance += delegator_reward
    delegator_account.reward_history[epoch] += delegator_reward  # Отслеживание наград
```

**Пример:**

```
Общая награда: 10 CPC
Комиссия валидатора: 10%
Всего делегировано: 100 CPC

Комиссия валидатору: 1 CPC
Доля делегаторов: 9 CPC

Делегатор A (60 CPC делегировано): 5.4 CPC
Делегатор B (40 CPC делегировано): 3.6 CPC
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

### Проверка наград валидатора

```bash
# Получить reward_address валидатора
./cpc-cli query validators --node http://localhost:8000 | jq '.validators[0].reward_address'

# Проверить баланс
./cpc-cli query balance <REWARD_ADDRESS> --node http://localhost:8000
```

### Проверка наград делегатора

**Запрос истории наград делегатора:**

```bash
# Получить историю наград для адреса делегатора
./cpc-cli query rewards <DELEGATOR_ADDRESS> --node http://localhost:8000
```

**Пример вывода:**

```
Delegator: cpc1abc...
Current Epoch: 5
Total Rewards: 125.5 CPC

Epoch      Reward Amount
------------------------------
0          25.4
1          24.8
2          25.1
3          25.0
4          25.2
```

### Проверка делегаций

**Просмотр всех делегаций для адреса:**

```bash
./cpc-cli query delegations <ADDRESS> --node http://localhost:8000
```

**Пример вывода:**

```
Delegator: cpc1abc...
Total Delegated: 100.0 CPC

Validator                                      Amount          Commission  Name
------------------------------------------------------------------------------------------
cpcvalcons1xyz...                              60.0            10.0%       Validator A
cpcvalcons1def...                              40.0            5.0%        Validator B
```

### Логи ноды

**В логах ноды:**

```
Block 15 added. Hash: 0x1234... (Round 0)
Distributed 1000000000000000000 (commission 10.0%) to validator cpc1alice..., 9000000000000000000 to delegators
```

**Примечание:** В текущей реализации логирование наград может быть отключено для производительности.

## Текущие возможности

### ✅ Реализовано:

1. **Делегирование и награды:**
   - Стейкеры могут делегировать токены валидаторам
   - Пропорциональное распределение наград делегаторам
   - Отслеживание истории наград по эпохам

2. **Комиссия валидатора:**
   - Валидаторы могут устанавливать комиссию (по умолчанию 10%)
   - Комиссия вычитается перед распределением делегаторам
   - Прозрачная модель комиссии

### Будущие улучшения

**Планируется:**

1. **Расширенный слэшинг:**
   - Дополнительные штрафы за некорректное поведение
   - Частичный слэшинг делегированных стейков

2. **Автоматическое реинвестирование:**
   - Автоматическое реинвестирование наград от делегирования
   - Стратегии реинвестирования

## Следующие шаги

- **[Staking Basics](staking-basic)** — Основы стейкинга
- **[Validator Lifecycle](validator-lifecycle)** — Жизненный цикл валидатора
- **[Node Setup](node/run-local)** — Запуск ноды валидатора

