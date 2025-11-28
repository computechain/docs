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

| Тип транзакции | Gas Limit |
|---------------|-----------|
| TRANSFER | 21,000 |
| STAKE | 40,000 |
| SUBMIT_RESULT | 80,000 |

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

