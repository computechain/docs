# Основы Стейкинга

Стейкинг позволяет вам стать валидатором в сети ComputeChain и участвовать в консенсусе.

## Требования

### Минимальный стейк

**По сетям:**

| Сеть | Минимальный стейк |
|---------|---------------|
| Devnet | 1,000 CPC |
| Testnet | 100,000 CPC |
| Mainnet | 100,000 CPC |

### Максимум валидаторов

| Сеть | Максимум валидаторов |
|---------|-------------------|
| Devnet | 5 |
| Testnet | 21 |
| Mainnet | 100 |

## Транзакция STAKE

### Структура транзакции

**Тип:** `TxType.STAKE`

**Поля:**

```python
Transaction(
    tx_type=TxType.STAKE,
    from_address="cpc1...",  # Адрес отправителя
    to_address=None,  # Не используется для стейкинга
    amount=1500 * 10**18,  # Сумма стейка (в wei)
    fee=gas_limit * gas_price,
    nonce=...,
    gas_price=1000,
    gas_limit=40000,  # GAS_PER_TYPE[STAKE]
    payload={
        "pub_key": "02a1b2c3..."  # Публичный ключ валидатора (обязательно!)
    }
)
```

### Обязательные поля

**`pub_key` в payload:**

- Публичный ключ валидатора (hex строка)
- Используется для генерации consensus адреса (`cpcvalcons...`)
- Транзакция будет отклонена без `pub_key`

**Автоматическое заполнение:**

CLI автоматически берет публичный ключ из keystore:

```python
# В cmd_tx_stake
pub_key_hex = sender_key['public_key']
tx.payload = {"pub_key": pub_key_hex}
```

## Процесс Стейкинга

### Шаг 1: Создать ключ

```bash
./cpc-cli keys add alice
```

### Шаг 2: Пополнить баланс

```bash
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000
```

**Важно:** Баланс должен покрывать:
- Сумму стейка (минимум 1,000 CPC для devnet)
- Комиссию за транзакцию (~40,000 gas * gas_price)

### Шаг 3: Отправить STAKE транзакцию

```bash
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000
```

**Что происходит:**

1. CLI создает `STAKE` транзакцию
2. Автоматически добавляет `pub_key` из keystore
3. Рассчитывает `gas_limit` (40,000) и `fee`
4. Подписывает транзакцию
5. Отправляет в мемпул через RPC `/tx/send`

### Шаг 4: Ожидание включения в блок

**Время ожидания:**

- Devnet: ~10 секунд (1 блок)
- После включения, валидатор создан, но еще не активен

### Шаг 5: Активация валидатора

**Эпоха:**

- Devnet: каждые 10 блоков (~100 секунд)
- Testnet: каждые 100 блоков (~50 минут)
- Mainnet: каждые 72 блока (~72 минуты)

**Что происходит в эпоху:**

1. Пересчет набора валидаторов
2. Сортировка по стейку (по убыванию)
3. Выбор топ-N валидаторов (N = max_validators)
4. Активация валидаторов (`is_active = True`)
5. Деактивация валидаторов вне топ-N

**Проверка статуса:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

## Увеличение стейка

### Добавление к существующему стейку

**Просто отправьте еще одну STAKE транзакцию:**

```bash
./cpc-cli tx stake 500 --from alice --node http://localhost:8000
```

**Что происходит:**

- Если валидатор с таким `pub_key` уже существует, стейк добавляется
- `val.power += tx.amount`
- Валидатор остается в наборе (если был активен)

## Адрес для наград (Reward Address)

### Установка адреса для наград

**По умолчанию:**

- `reward_address` устанавливается в `tx.from_address` (адрес отправителя)
- Награды за блоки идут на этот адрес

**Изменение (Future):**

Планируется возможность изменения `reward_address` через отдельную транзакцию.

## Стоимость газа

### Комиссия за STAKE

**Стоимость газа:** 40,000 gas

**Пример расчета:**

```python
gas_limit = 40_000
gas_price = 1_000  # Devnet
fee = 40_000 * 1_000 = 40_000_000 wei = 0.00004 CPC
```

**Минимальный баланс для стейкинга:**

```
Минимальный Стейк + Комиссия + Буфер
= 1,000 CPC + 0.00004 CPC + ~1 CPC
≈ 1,001 CPC
```

## Примеры

### Полный сценарий (Node B)

```bash
# 1. Импорт ключа faucet с Node A
./cpc-cli keys import faucet --private-key $(cat .node_a/faucet_key.hex)

# 2. Создать Alice
./cpc-cli keys add alice

# 3. Получить адрес Alice
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 4. Пополнить аккаунт
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000

# 5. Застейкать
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000

# 6. Ждать эпоху (10 блоков)
sleep 120

# 7. Проверить статус
./cpc-cli query validators --node http://localhost:8000
```

## Следующие шаги

- **[Жизненный цикл валидатора](validator-lifecycle.md)** — Жизненный цикл валидатора
- **[Награды](rewards.md)** — Награды за валидацию
- **[Настройка ноды](../node/run-local.md)** — Запуск ноды валидатора

