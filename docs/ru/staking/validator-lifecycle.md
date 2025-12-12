# Жизненный цикл Валидатора

## Этапы жизни валидатора

### 1. Создание

**Триггер:** Транзакция `STAKE` с достаточной суммой

**Условия:**

- `tx.amount >= min_validator_stake`
- `pub_key` присутствует в payload
- Баланс отправителя достаточен

**Что происходит:**

```python
# В State.apply_transaction
val_addr = address_from_pubkey(pub_key_bytes, prefix="cpcvalcons")
val = Validator(
    address=val_addr,
    pq_pub_key=pub_key_hex,
    power=tx.amount,
    is_active=False,  # Еще не активен!
    reward_address=tx.from_address
)
```

**Статус:** `is_active = False`

### 2. Ожидание (Pending)

**Период:** До следующей эпохи

**Что происходит:**

- Валидатор создан, но не участвует в консенсусе
- Не может производить блоки
- Не получает награды

**Проверка:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

**Вывод:**

```json
{
  "epoch": 1,
  "validators": [
    {
      "address": "cpcvalcons1...",
      "power": "1500000000000000000000",
      "is_active": false,  // ← Еще не активен
      "reward_address": "cpc1..."
    }
  ]
}
```

### 3. Активация

**Триггер:** Переход эпохи (каждые N блоков)

**Процесс:**

1. **Собрать всех валидаторов:**
   ```python
   all_validators = state.get_all_validators()
   ```

2. **Отфильтровать по минимальному стейку:**
   ```python
   active_candidates = [v for v in all_validators if v.power >= min_validator_stake]
   ```

3. **Сортировать по стейку (по убыванию):**
   ```python
   sorted_validators = sorted(active_candidates, key=lambda v: v.power, reverse=True)
   ```

4. **Выбрать топ-N:**
   ```python
   top_validators = sorted_validators[:max_validators]
   ```

5. **Активировать:**
   ```python
   for val in top_validators:
       val.is_active = True
   ```

6. **Деактивировать остальных:**
   ```python
   for val in all_validators:
       if val not in top_validators:
           val.is_active = False
   ```

**Статус:** `is_active = True`

### 4. Активная валидация

**Период:** Пока валидатор в топ-N

**Что происходит:**

- Участвует в консенсусе (Round-Robin)
- Может производить блоки в свой слот
- Получает награды за блоки и комиссии

**Round-Robin:**

```python
def get_proposer(height: int) -> Validator:
    active_validators = [v for v in validators if v.is_active]
    index = height % len(active_validators)
    return active_validators[index]
```

**Пример:**

```
Блок 10: Валидатор A (index 0)
Блок 11: Валидатор B (index 1)
Блок 12: Валидатор C (index 2)
Блок 13: Валидатор A (index 0)  # Цикл повторяется
```

### 5. Деактивация

**Причины:**

1. **Недостаточный стейк:**
   - Валидатор упал ниже `min_validator_stake`
   - Или другие валидаторы обогнали по стейку

2. **Вытеснение из топ-N:**
   - Появились валидаторы с большим стейком
   - Валидатор выпал из топ-N

**Что происходит:**

```python
val.is_active = False
```

**Последствия:**

- Перестает производить блоки
- Не получает награды
- Может быть реактивирован в следующей эпохе (если вернется в топ-N)

### 6. Jailing (Заключение в тюрьму)

**Триггер:** Пропуск слишком большого количества блоков

**Условия:**

- Валидатор пропускает `max_missed_blocks_sequential` блоков (по умолчанию: 10)
- Производительность падает ниже допустимого порога

**Что происходит:**

```python
def _jail_validator(val, state, current_height):
    # Прогрессивные штрафы
    if val.jail_count == 0:
        penalty_rate = 0.05  # 5% в первый раз
    elif val.jail_count == 1:
        penalty_rate = 0.10  # 10% во второй раз
    else:
        penalty_rate = 1.0   # 100% в третий раз (исключение)

    penalty = int(val.power * penalty_rate)
    val.power = max(0, val.power - penalty)
    val.total_penalties += penalty
    val.jail_count += 1
    val.jailed_until_height = current_height + jail_duration  # +100 блоков
    val.missed_blocks = 0
    val.is_active = False
```

**Прогрессивные штрафы:**

| Количество jail | Штраф | Длительность | Результат |
|-----------------|-------|--------------|-----------|
| 1-й | 5% | 100 блоков | Заключен |
| 2-й | 10% | 100 блоков | Заключен |
| 3-й | 100% | Навсегда | Исключен |

**Статус:** `jailed_until_height > 0`, `is_active = False`

**Последствия:**

- Валидатор немедленно прекращает производство блоков
- Не может участвовать в консенсусе
- Стейк уменьшается на сумму штрафа
- Остается в jail на 100 блоков (или до транзакции unjail)

### 7. Unjailing (Досрочное освобождение)

**Триггер:** Транзакция `UNJAIL`

**Стоимость:** 1,000 CPC (сжигается) + gas комиссия

**Пример:**

```bash
./cpc-cli tx unjail --from validator_owner --node http://localhost:8000
```

**Что происходит:**

```python
# В State.apply_transaction для UNJAIL
if tx.amount == unjail_fee:  # Должно быть ровно 1000 CPC
    # Сжигаем комиссию (удаляем из обращения)
    sender.balance -= tx.amount
    # Освобождаем из jail
    val.jailed_until_height = 0
    val.missed_blocks = 0
    val.is_active = True
```

**Статус:** `jailed_until_height = 0`, `is_active = True`

**Результат:**

- Валидатор может участвовать в следующей эпохе
- Может снова производить блоки
- Счетчик пропущенных блоков сброшен

### 8. Unstaking (Вывод стейка)

**Триггер:** Транзакция `UNSTAKE`

**Пример:**

```bash
./cpc-cli tx unstake 500 --from validator_owner --node http://localhost:8000
```

**Что происходит:**

```python
# В State.apply_transaction для UNSTAKE
penalty_amount = 0
if val.jailed_until_height > 0:
    # 10% штраф при выводе во время jail
    penalty_amount = int(tx.amount * 0.10)

return_amount = tx.amount - penalty_amount
val.power -= tx.amount
sender.balance += return_amount

# Деактивация если power падает до 0
if val.power == 0:
    val.is_active = False
```

**Штрафы:**

- Обычный unstake: 0% штраф
- Unstake в jail: **10% штраф** (сжигается)

**Частичный unstake:**

- Можно вывести часть стейка
- Валидатор остается активным если `power >= min_validator_stake`
- Может продолжать валидацию с уменьшенным стейком

**Полный unstake:**

- Если `power = 0`: валидатор деактивируется
- `is_active = False`
- Прекращает участие в консенсусе

### 9. Ре-стейкинг (Добавление стейка)

**Триггер:** Новая транзакция `STAKE` с тем же `pub_key`

**Что происходит:**

```python
val = get_validator(val_addr)
if val:
    val.power += tx.amount  # Добавляется к существующему стейку
```

**Результат:**

- Повышение позиции в рейтинге
- Больше шансов остаться в топ-N
- Больше наград (если активен)

## Эпоха

### Определение

**Эпоха** — период между пересчетами набора валидаторов.

**Длительность:**

| Сеть | Блоки | Время (примерно) |
|---------|--------|----------------|
| Devnet | 10 | ~100 сек |
| Testnet | 100 | ~50 мин |
| Mainnet | 72 | ~72 мин |

### Переход эпохи

**Триггер:**

```python
if (block.header.height + 1) % config.epoch_length_blocks == 0:
    _update_consensus_from_state()
```

**Что происходит:**

1. Пересчет набора валидаторов
2. Активация/деактивация
3. Обновление `ConsensusEngine.validator_set`

## Примеры сценариев

### Сценарий 1: Становление валидатором

```
Блок 0:  Alice отправляет STAKE(1500 CPC)
Блок 1:  Транзакция включена, валидатор создан (is_active=False)
Блок 2-9: Ожидание эпохи
Блок 10: Эпоха! Alice активируется (is_active=True)
Блок 11: Alice производит первый блок (Round-Robin)
```

### Сценарий 2: Вытеснение из Топ-N

```
Эпоха 1: Топ-5: [A:2000, B:1800, C:1500, D:1200, E:1000]
         Alice (1500) — активна

Эпоха 2: Топ-5: [A:2000, B:1800, C:1500, F:1400, D:1200]
         Alice (1500) — все еще активна

Эпоха 3: Топ-5: [A:2000, B:1800, G:1600, C:1500, F:1400]
         Alice (1500) — деактивирована (вытеснена G)
```

### Сценарий 3: Возвращение в Топ-N

```
Эпоха 1: Alice деактивирована (6-я по стейку)
Эпоха 1: Alice отправляет STAKE(+500 CPC)
Эпоха 2: Alice возвращается в топ-5, активируется
```

## Мониторинг

### Проверка статуса валидатора

```bash
./cpc-cli query validators --node http://localhost:8000
```

**Вывод:**

```json
{
  "epoch": 2,
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

### Проверка текущего Proposer

```bash
# Через статус ноды
curl http://localhost:8000/status
```

**Вывод:**

```json
{
  "height": 15,
  "last_hash": "0x...",
  "network": "devnet",
  "mempool_size": 2,
  "epoch": 1
}
```

**Расчет Proposer:**

```python
height = 15
epoch = height // 10  # = 1
active_validators = get_active_validators()
proposer_index = height % len(active_validators)
proposer = active_validators[proposer_index]
```

## Следующие шаги

- **[Основы стейкинга](staking-basic.md)** — Основы стейкинга
- **[Награды](rewards.md)** — Награды за валидацию
- **[Настройка ноды](../node/run-local.md)** — Запуск ноды валидатора

