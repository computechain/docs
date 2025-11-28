# CLI Кошелёк (cpc-cli)

Командная строка для работы с ComputeChain: управление ключами, отправка транзакций, запросы к нодам.

## Установка

**Текущая версия:** Исполняемый скрипт в корне репозитория

```bash
chmod +x cpc-cli
./cpc-cli --help
```

## Команды

### Keys — Управление ключами

#### Создать ключ

```bash
./cpc-cli keys add <NAME>
```

**Пример:**

```bash
./cpc-cli keys add alice
```

**Вывод:**

```
Key 'alice' created.
Address: cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
Pubkey:  02a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
Important: Private key saved unencrypted (MVP). Do not share!
```

#### Импортировать ключ

```bash
./cpc-cli keys import <NAME> --private-key <HEX_PRIVATE_KEY>
```

**Пример:**

```bash
./cpc-cli keys import faucet --private-key 4f3edf982522b4e51b7e8b5f2f9c4d1d7a9e5f8c2b6d4e1a3c5b7d9e0f1a2b3c
```

#### Список ключей

```bash
./cpc-cli keys list
```

**Вывод:**

```
Name            Address                                          
------------------------------------------------------------
alice           cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
faucet          cpc1f1a2u3c4e5t6k7e8y9a0b1c2d3e4f5g6h7i8j9k0
```

#### Показать ключ

```bash
./cpc-cli keys show <NAME>
```

**Пример:**

```bash
./cpc-cli keys show alice
```

**Вывод:**

```json
{
  "name": "alice",
  "address": "cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
  "public_key": "02a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
}
```

### Query — Запросы к ноде

#### Баланс

```bash
./cpc-cli query balance <ADDRESS> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli query balance cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t --node http://localhost:8000
```

**Вывод:**

```
Balance: 2000.0 CPC
Nonce: 1
```

#### Блок

```bash
./cpc-cli query block <HEIGHT> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli query block 10 --node http://localhost:8000
```

**Вывод:** JSON с полным блоком

#### Валидаторы

```bash
./cpc-cli query validators [--node <URL>]
```

**Пример:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

**Вывод:**

```
Epoch: 1
Address                                         Power       Active
----------------------------------------------------------------------
cpcvalcons1alice...                            1500        True
cpcvalcons1bob...                               1200        True
```

### Tx — Транзакции

#### Отправить монеты

```bash
./cpc-cli tx send <TO_ADDRESS> <AMOUNT> --from <KEY_NAME> [--node <URL>] [--gas-price <PRICE>] [--gas-limit <LIMIT>]
```

**Пример:**

```bash
./cpc-cli tx send cpc1bob... 100 --from alice --node http://localhost:8000
```

**Параметры:**

- `--gas-price`: Цена газа (по умолчанию: 1000 для devnet)
- `--gas-limit`: Лимит газа (по умолчанию: 21,000 для TRANSFER)

**Вывод:**

```
Sending 100.0 CPC to cpc1bob...
Success! TxHash: 0x1234567890abcdef...
```

#### Стейкинг

```bash
./cpc-cli tx stake <AMOUNT> --from <KEY_NAME> [--node <URL>] [--gas-price <PRICE>] [--gas-limit <LIMIT>]
```

**Пример:**

```bash
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000
```

**Параметры:**

- `--gas-price`: Цена газа (по умолчанию: 1000)
- `--gas-limit`: Лимит газа (по умолчанию: 40,000 для STAKE)

**Вывод:**

```
Staking 1500.0 CPC from cpc1alice...
Success! TxHash: 0xabcdef1234567890...
```

**Важно:** Публичный ключ автоматически берётся из keystore.

#### Отправить результат PoC

```bash
./cpc-cli tx submit-result --task-id <UUID> --result-hash <HEX> --from <KEY_NAME> [--node <URL>] [--proof <PROOF>] [--nonce <NONCE>]
```

**Пример:**

```bash
./cpc-cli tx submit-result \
  --task-id "550e8400-e29b-41d4-a716-446655440000" \
  --result-hash "0x1234567890abcdef..." \
  --from worker \
  --node http://localhost:8000
```

**Параметры:**

- `--task-id`: UUID задачи (обязательно)
- `--result-hash`: Хеш результата (обязательно)
- `--proof`: Доказательство (опционально)
- `--nonce`: Nonce для синтетических задач (опционально)

**Вывод:**

```
Submitting result for task 550e8400-e29b-41d4-a716-446655440000...
Success! TxHash: 0x9876543210fedcba...
```

## Переменные окружения

### CPC_NODE

**Использование:** URL ноды по умолчанию

```bash
export CPC_NODE=http://localhost:8000
./cpc-cli query balance cpc1...
```

**Приоритет:**

1. Параметр команды `--node`
2. Переменная окружения `CPC_NODE`
3. `http://localhost:8000` (по умолчанию)

## Примеры использования

### Пример 1: Полный сценарий создания валидатора

```bash
# 1. Создать ключ
./cpc-cli keys add alice

# 2. Получить адрес
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 3. Пополнить аккаунт
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000

# 4. Проверить баланс
./cpc-cli query balance $ALICE_ADDR --node http://localhost:8000

# 5. Застейкать
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000

# 6. Проверить валидаторов
./cpc-cli query validators --node http://localhost:8000
```

### Пример 2: Отправка транзакций с пользовательским газом

```bash
# Высокая цена газа для быстрого включения
./cpc-cli tx send cpc1bob... 100 \
  --from alice \
  --node http://localhost:8000 \
  --gas-price 5000 \
  --gas-limit 21000
```

### Пример 3: Работа с несколькими нодами

```bash
# Node A
./cpc-cli query balance cpc1alice... --node http://localhost:8000

# Node B
./cpc-cli query balance cpc1alice... --node http://localhost:8001
```

## Устранение неполадок

### Ошибка: Ключ не найден

**Причина:** Ключ не существует в keystore

**Решение:**

```bash
# Проверить список ключей
./cpc-cli keys list

# Создать ключ
./cpc-cli keys add <NAME>
```

### Ошибка: Connection refused

**Причина:** Нода не запущена или недоступна

**Решение:**

```bash
# Проверить статус ноды
curl http://localhost:8000/status

# Указать правильный URL
./cpc-cli query balance cpc1... --node http://192.168.1.100:8000
```

### Ошибка: Insufficient balance

**Причина:** Недостаточный баланс для транзакции

**Решение:**

```bash
# Проверить баланс
./cpc-cli query balance cpc1... --node http://localhost:8000

# Пополнить аккаунт
./cpc-cli tx send <ADDRESS> <AMOUNT> --from faucet
```

### Ошибка: Invalid nonce

**Причина:** Nonce не соответствует ожидаемому

**Решение:**

- CLI автоматически получает nonce из ноды
- Если ошибка повторяется, проверьте, что транзакция не была отправлена дважды

## Следующие шаги

- **[Node CLI](node-cli.md)** — Команды для управления нодой
- **[Кошельки](../wallets/keystore.md)** — Управление ключами
- **[Стейкинг](../staking/staking-basic.md)** — Как стать валидатором
