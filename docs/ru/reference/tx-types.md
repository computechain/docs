# Типы транзакций

Справочник по типам транзакций в ComputeChain.

## TRANSFER

**Тип:** `TxType.TRANSFER`

**Назначение:** Перевод токенов CPC между аккаунтами

**Gas Cost:** 21,000 gas

**Структура:**

```python
Transaction(
    tx_type=TxType.TRANSFER,
    from_address="cpc1sender...",
    to_address="cpc1recipient...",
    amount=100 * 10**18,  # 100 CPC (в wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=21000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Обязательные поля:**

- `from_address`: Адрес отправителя (cpc1...)
- `to_address`: Адрес получателя (cpc1...)
- `amount`: Сумма перевода (в wei, минимум 0)
- `nonce`: Номер транзакции отправителя
- `pub_key`: Публичный ключ отправителя

**Валидация:**

- Баланс отправителя >= amount + fee
- Nonce должен быть следующим в последовательности
- Подпись должна быть валидной
- `to_address` не должен быть пустым

**Пример:**

```bash
./cpc-cli tx send cpc1recipient... 100 --from alice
```

## STAKE

**Тип:** `TxType.STAKE`

**Назначение:** Стать валидатором или увеличить стейк

**Gas Cost:** 40,000 gas

**Структура:**

```python
Transaction(
    tx_type=TxType.STAKE,
    from_address="cpc1sender...",
    to_address=None,
    amount=1500 * 10**18,  # 1500 CPC (в wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=40000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={
        "pub_key": "02a1b2c3..."  # Публичный ключ валидатора (обязательно!)
    }
)
```

**Обязательные поля:**

- `from_address`: Адрес отправителя (cpc1...)
- `amount`: Сумма стейка (в wei, минимум min_validator_stake)
- `payload.pub_key`: Публичный ключ валидатора (hex строка)

**Валидация:**

- Баланс отправителя >= amount + fee
- `amount >= min_validator_stake`
- `pub_key` должен присутствовать в payload
- Подпись должна быть валидной

**Результат:**

- Создаётся или обновляется валидатор с адресом `cpcvalcons...` (вычисляется из `pub_key`)
- Стейк добавляется к существующему (если валидатор уже существует)
- `reward_address` устанавливается в `from_address` (если новый валидатор)

**Пример:**

```bash
./cpc-cli tx stake 1500 --from alice
```

## UNSTAKE

**Тип:** `TxType.UNSTAKE`

**Назначение:** Вывод застейканных токенов из валидатора

**Gas Cost:** 40,000 gas

**Структура:**

```python
Transaction(
    tx_type=TxType.UNSTAKE,
    from_address="cpc1sender...",
    to_address=None,
    amount=500 * 10**18,  # Сумма для вывода (в wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=40000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Обязательные поля:**

- `from_address`: Адрес владельца валидатора (cpc1...)
- `amount`: Сумма для вывода (в wei, должна быть > 0)
- `nonce`: Номер транзакции отправителя
- `pub_key`: Публичный ключ отправителя

**Валидация:**

- Валидатор должен существовать
- Power валидатора >= amount
- Баланс отправителя >= fee
- Подпись должна быть валидной

**Штрафы:**

- Обычный unstake: 0% штраф
- Unstake в jail: **10% штраф** (сжигается)

**Результат:**

- Токены возвращаются отправителю (минус штраф если в jail)
- Power валидатора уменьшается на amount
- Если power становится 0: валидатор деактивируется (`is_active = False`)

**Пример:**

```bash
python3 -m cli.main tx unstake 500 --from validator1
```

## UPDATE_VALIDATOR

**Тип:** `TxType.UPDATE_VALIDATOR`

**Назначение:** Обновление метаданных валидатора (имя, сайт, комиссия)

**Gas Cost:** 30,000 gas

**Структура:**

```python
Transaction(
    tx_type=TxType.UPDATE_VALIDATOR,
    from_address="cpc1owner...",
    to_address=None,
    amount=0,
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=30000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={
        "name": "MyPool",  # Опционально, макс 64 символа
        "website": "https://pool.com",  # Опционально, макс 128 символов
        "description": "Лучший пул валидаторов",  # Опционально, макс 256 символов
        "commission_rate": 0.15  # Опционально, 0.0-1.0 (15%)
    }
)
```

**Обязательные поля:**

- `from_address`: Адрес владельца валидатора (cpc1...)
- Хотя бы одно поле метаданных в payload

**Опциональные поля в payload:**

- `name`: Человекочитаемое имя (макс 64 символа)
- `website`: URL сайта (макс 128 символов)
- `description`: Описание (макс 256 символов)
- `commission_rate`: Ставка комиссии (0.0-1.0, макс 0.20 = 20%)

**Валидация:**

- Валидатор должен существовать
- Только владелец валидатора может обновлять
- Соблюдаются лимиты длины полей
- commission_rate должна быть 0.0-1.0
- Подпись должна быть валидной

**Результат:**

- Метаданные валидатора обновляются в состоянии
- Отображаются в dashboard и RPC запросах

**Пример:**

```bash
python3 -m cli.main tx update-validator \
  --name "MyPool" \
  --website "https://pool.com" \
  --commission 0.15 \
  --from validator1
```

## DELEGATE

**Тип:** `TxType.DELEGATE`

**Назначение:** Делегирование токенов валидатору

**Gas Cost:** 35,000 gas

**Структура:**

```python
Transaction(
    tx_type=TxType.DELEGATE,
    from_address="cpc1delegator...",
    to_address="cpcvalcons1validator...",  # Consensus адрес валидатора
    amount=500 * 10**18,  # Сумма делегирования (в wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=35000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Обязательные поля:**

- `from_address`: Адрес делегатора (cpc1...)
- `to_address`: Consensus адрес валидатора (cpcvalcons...)
- `amount`: Сумма делегирования (в wei, минимум 100 CPC)
- `nonce`: Номер транзакции отправителя
- `pub_key`: Публичный ключ отправителя

**Валидация:**

- Валидатор должен существовать и быть активным
- amount >= min_delegation (100 CPC)
- Баланс делегатора >= amount + fee
- Подпись должна быть валидной

**Результат:**

- Токены переводятся от делегатора к валидатору
- `total_delegated` валидатора увеличивается
- `power` валидатора увеличивается
- Делегатор получает право на награды с учетом комиссии

**Пример:**

```bash
python3 -m cli.main tx delegate cpcvalcons1abc... 500 --from delegator
```

## UNDELEGATE

**Тип:** `TxType.UNDELEGATE`

**Назначение:** Вывод делегированных токенов от валидатора

**Gas Cost:** 35,000 gas

**Структура:**

```python
Transaction(
    tx_type=TxType.UNDELEGATE,
    from_address="cpc1delegator...",
    to_address="cpcvalcons1validator...",  # Consensus адрес валидатора
    amount=200 * 10**18,  # Сумма для вывода (в wei)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=35000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Обязательные поля:**

- `from_address`: Адрес делегатора (cpc1...)
- `to_address`: Consensus адрес валидатора (cpcvalcons...)
- `amount`: Сумма для вывода (в wei, должна быть > 0)
- `nonce`: Номер транзакции отправителя
- `pub_key`: Публичный ключ отправителя

**Валидация:**

- Валидатор должен существовать
- total_delegated валидатора >= amount
- Баланс делегатора >= fee
- Подпись должна быть валидной

**Результат:**

- Токены возвращаются делегатору
- `total_delegated` валидатора уменьшается
- `power` валидатора уменьшается

**Пример:**

```bash
python3 -m cli.main tx undelegate cpcvalcons1abc... 200 --from delegator
```

## UNJAIL

**Тип:** `TxType.UNJAIL`

**Назначение:** Досрочное освобождение из jail (оплата комиссии для выхода из jail до запланированного времени)

**Gas Cost:** 50,000 gas

**Комиссия:** 1,000 CPC (сжигается) + gas комиссия

**Структура:**

```python
Transaction(
    tx_type=TxType.UNJAIL,
    from_address="cpc1validator...",
    to_address=None,
    amount=1000 * 10**18,  # Комиссия unjail: 1000 CPC (сжигается)
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=50000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={}
)
```

**Обязательные поля:**

- `from_address`: Адрес владельца валидатора (cpc1...)
- `amount`: Должна быть ровно 1,000 CPC (комиссия unjail)
- `nonce`: Номер транзакции отправителя
- `pub_key`: Публичный ключ отправителя

**Валидация:**

- Валидатор должен существовать
- Валидатор должен быть в jail (`jailed_until_height > 0`)
- amount должна быть ровно 1,000 CPC
- Баланс отправителя >= 1,000 CPC + gas комиссия
- Подпись должна быть валидной

**Результат:**

- 1,000 CPC сжигается (удаляется из обращения)
- Валидатор освобождается из jail:
  - `jailed_until_height = 0`
  - `missed_blocks = 0`
  - `is_active = True`
- Валидатор может участвовать в следующей эпохе

**Пример:**

```bash
python3 -m cli.main tx unjail --from validator1
```

**Расчет стоимости:**

```
Комиссия Unjail: 1,000 CPC (сжигается)
Gas комиссия: 50,000 * 1,000 wei = 0.00005 CPC
Итого: ~1,000.00005 CPC
```

## SUBMIT_RESULT

**Тип:** `TxType.SUBMIT_RESULT`

**Назначение:** Отправка результата выполнения compute-задачи

**Gas Cost:** 80,000 gas

**Структура:**

```python
Transaction(
    tx_type=TxType.SUBMIT_RESULT,
    from_address="cpc1worker...",
    to_address=None,
    amount=0,  # Награда пока не интегрирована в L1
    fee=gas_limit * gas_price,
    nonce=1,
    gas_price=1000,
    gas_limit=80000,
    timestamp=1700000000,
    pub_key="02a1b2c3...",
    payload={
        "task_id": "550e8400-e29b-41d4-a716-446655440000",
        "worker_address": "cpc1worker...",
        "result_hash": "0x1234567890abcdef...",
        "proof": None,  # Опционально (будущее: ZK-proof)
        "nonce": 12345,  # Опционально (для синтетических задач)
        "signature": ""  # Опционально
    }
)
```

**Обязательные поля:**

- `from_address`: Адрес воркера (cpc1...)
- `payload.task_id`: UUID задачи
- `payload.worker_address`: Адрес воркера (должен совпадать с `from_address`)
- `payload.result_hash`: Хеш результата вычисления (hex строка)

**Опциональные поля:**

- `payload.proof`: Доказательство корректности (будущее: ZK-proof)
- `payload.nonce`: Nonce для синтетических задач
- `payload.signature`: Подпись воркера

**Валидация:**

- Структура `ComputeResult` должна быть валидной
- `worker_address` должен совпадать с `tx.from_address`
- Proof проверяется (в будущем через ZK-верификацию)

**Результат:**

- Результат включается в блок
- `compute_root` обновляется в заголовке блока
- Награда пока не интегрирована в L1 (планируется)

**Пример:**

```bash
./cpc-cli tx submit-result \
  --task-id "550e8400-e29b-41d4-a716-446655440000" \
  --result-hash "0x1234567890abcdef..." \
  --from worker
```

## Общие поля транзакции

### Обязательные поля

- `tx_type`: Тип транзакции (enum)
- `from_address`: Адрес отправителя (cpc1...)
- `amount`: Сумма (в wei)
- `fee`: Комиссия (gas_used * gas_price)
- `nonce`: Номер транзакции отправителя
- `gas_price`: Цена газа (wei per gas)
- `gas_limit`: Лимит газа
- `timestamp`: Временная метка (Unix timestamp)
- `pub_key`: Публичный ключ отправителя (hex строка)
- `signature`: Подпись транзакции (hex строка)

### Опциональные поля

- `to_address`: Адрес получателя (для TRANSFER)
- `payload`: Дополнительные данные (dict)

## Лимиты

### Gas Limits

**По типам транзакций:**

| Тип транзакции | Gas Limit | Дополнительные комиссии |
|---------------|-----------|------------------------|
| TRANSFER | 21,000 | - |
| STAKE | 40,000 | - |
| UNSTAKE | 40,000 | 10% штраф если в jail |
| UPDATE_VALIDATOR | 30,000 | - |
| DELEGATE | 35,000 | - |
| UNDELEGATE | 35,000 | - |
| UNJAIL | 50,000 | +1,000 CPC (сжигается) |
| SUBMIT_RESULT | 80,000 | - |

**Блок:**

- Devnet: 10,000,000 gas
- Testnet: 15,000,000 gas
- Mainnet: 30,000,000 gas

### Минимальные значения

**Gas Price:**

- Devnet: 1,000 wei
- Testnet: 5,000 wei
- Mainnet: 1,000,000,000 wei (1 Gwei)

**Amount:**

- Минимум: 0 wei
- Для STAKE: минимум `min_validator_stake`

## Инварианты

### Nonce

- Nonce должен быть последовательным
- Начинается с 0 для нового аккаунта
- Увеличивается на 1 для каждой транзакции

### Баланс

- Баланс отправителя >= amount + fee
- Баланс не может быть отрицательным

### Подпись

- Подпись должна быть валидной для `from_address`
- Используется ECDSA (secp256k1) в MVP
- Планируется переход на Post-Quantum подписи

## Следующие шаги

- **[RPC API](rpc)** — RPC endpoints
- **[Glossary](glossary)** — Терминология
- **[Staking](staking/staking-basic)** — Как стать валидатором

