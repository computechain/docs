# Справочник CLI

Полный справочник команд для `cpc-cli` - интерфейса командной строки ComputeChain.

## Установка

```bash
chmod +x cpc-cli
./cpc-cli --help
```

## Управление ключами

### Создать ключ

```bash
./cpc-cli keys add <ИМЯ>
```

**Пример:**

```bash
./cpc-cli keys add alice
```

**Вывод:**

```
Key 'alice' created.
Address: cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v
Pubkey:  030c9ae768a358e7924d2a27fd0708549902e17af8e81cf7a545e0f319d2e177bd
Important: Private key saved unencrypted (MVP). Do not share!
```

**Хранилище:** Ключи сохраняются в `~/.computechain/keys/` как JSON файлы

⚠️ **Безопасность:** Ключи хранятся незашифрованными. Делайте бэкапы безопасно и ограничьте права доступа:

```bash
chmod 700 ~/.computechain/keys/
```

### Импортировать ключ

```bash
./cpc-cli keys import <ИМЯ> --private-key <ПРИВАТНЫЙ_КЛЮЧ_HEX>
```

**Пример:**

```bash
./cpc-cli keys import faucet --private-key 4f3edf982522b4e51b7e8b5f2f9c4d1d...
```

### Список ключей

```bash
./cpc-cli keys list
```

**Вывод:**

```
Name            Address
------------------------------------------------------------
alice           cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v
faucet          cpc1q02sr0n4kw84qfsy7q9ntp7mv6rhs5p4k9zyf6
```

### Показать ключ

```bash
./cpc-cli keys show <ИМЯ>
```

**Вывод:**

```json
{
  "name": "alice",
  "address": "cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v",
  "public_key": "030c9ae768a358e7924d2a27fd0708549902e17af8e81cf7a545e0f319d2e177bd"
}
```

## Команды запросов

### Баланс

```bash
./cpc-cli query balance <АДРЕС> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli query balance cpc17x8ky7wwrvzue2hjpel6jhgz6hxwjn93ku0x5v
```

**Вывод:**

```
Balance: 2000.0 CPC
Nonce: 1
```

### Валидаторы

```bash
./cpc-cli query validators [--node <URL>]
```

**Вывод:**

```
Epoch: 1
Address                                         Power       Active
----------------------------------------------------------------------
cpcvalcons1alice...                            1500        True
cpcvalcons1bob...                               1200        True
```

### Делегации

```bash
./cpc-cli query delegations <АДРЕС> [--node <URL>]
```

**Вывод:**

```
Делегатор: cpc1abc...
Всего делегировано: 100.0 CPC

Валидатор                                      Сумма       Комиссия  Имя
------------------------------------------------------------------------------------------
cpcvalcons1xyz...                              60.0        10.0%     Валидатор A
cpcvalcons1def...                              40.0        5.0%      Валидатор B
```

### Награды

```bash
./cpc-cli query rewards <АДРЕС> [--node <URL>]
```

**Вывод:**

```
Делегатор: cpc1abc...
Текущая эпоха: 5
Всего наград: 125.5 CPC

Эпоха      Сумма награды
------------------------------
0          25.4
1          24.8
2          25.1
```

### Блок

```bash
./cpc-cli query block <ВЫСОТА> [--node <URL>]
```

Возвращает полный JSON блока для указанной высоты.

## Команды транзакций

### Перевод

```bash
./cpc-cli tx send <АДРЕС_ПОЛУЧАТЕЛЯ> <СУММА> --from <ИМЯ_КЛЮЧА> [--node <URL>] [--gas-price <ЦЕНА>]
```

**Пример:**

```bash
./cpc-cli tx send cpc1q9u5zga8d6jtx0g7hkk4upckw7t2k38cd8n4fy 100 --from alice
```

**Параметры:**
- `--gas-price`: Цена gas (по умолчанию: 1000)
- `--gas-limit`: Лимит gas (по умолчанию: 21,000)

### Стейк

```bash
./cpc-cli tx stake <СУММА> --from <ИМЯ_КЛЮЧА> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli tx stake 1500 --from alice
```

**Требования:**
- Минимум: 100 CPC
- Создает валидатора с адресом `cpcvalcons`
- Активируется в следующую эпоху (через 100 блоков)

### Анстейк

```bash
./cpc-cli tx unstake <СУММА> --from <ИМЯ_КЛЮЧА> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli tx unstake 500 --from alice
```

⚠️ **Штраф:** 10% слэшится при выводе в состоянии jailed

### Делегировать

```bash
./cpc-cli tx delegate <АДРЕС_ВАЛИДАТОРА> <СУММА> --from <ИМЯ_КЛЮЧА> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli tx delegate cpcvalcons1abc... 500 --from delegator
```

**Требования:**
- Валидатор должен быть активен
- Получайте пропорциональные награды на основе суммы делегирования

### Отменить делегирование

```bash
./cpc-cli tx undelegate <АДРЕС_ВАЛИДАТОРА> <СУММА> --from <ИМЯ_КЛЮЧА> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli tx undelegate cpcvalcons1abc... 200 --from delegator
```

### Обновить валидатора

```bash
./cpc-cli tx update-validator --from <ИМЯ_КЛЮЧА> [--name <ИМЯ>] [--website <URL>] [--description <ТЕКСТ>] [--commission <СТАВКА>] [--node <URL>]
```

**Пример:**

```bash
./cpc-cli tx update-validator \
  --name "MyPool" \
  --website "https://pool.com" \
  --description "Лучший пул валидаторов" \
  --commission 0.15 \
  --from alice
```

**Параметры:**
- `--name`: Имя валидатора (макс 64 символа)
- `--website`: URL сайта (макс 128 символов)
- `--description`: Описание (макс 256 символов)
- `--commission`: Ставка комиссии (0.0-1.0, макс 20%)

### Unjail

```bash
./cpc-cli tx unjail --from <ИМЯ_КЛЮЧА> [--node <URL>]
```

**Пример:**

```bash
./cpc-cli tx unjail --from alice
```

**Стоимость:**
- Плата за unjail: 1000 CPC (сжигается)
- Плата за gas: ~50,000 gas
- Работает только если валидатор в состоянии jailed

## Переменные окружения

### CPC_NODE

Установить URL ноды по умолчанию:

```bash
export CPC_NODE=http://localhost:8000
./cpc-cli query balance cpc1...
```

**Приоритет:**
1. Флаг `--node`
2. Переменная окружения `CPC_NODE`
3. `http://localhost:8000` (по умолчанию)

## Полные примеры

### Создать и пополнить валидатора

```bash
# 1. Создать ключ
./cpc-cli keys add alice

# 2. Получить адрес
ALICE=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 3. Пополнить аккаунт
./cpc-cli tx send $ALICE 2000 --from faucet

# 4. Проверить баланс
./cpc-cli query balance $ALICE

# 5. Застейкать
./cpc-cli tx stake 1500 --from alice

# 6. Ждать перехода эпохи (~100 блоков)

# 7. Проверить активность валидатора
./cpc-cli query validators
```

### Делегировать и получать награды

```bash
# 1. Создать ключ делегатора
./cpc-cli keys add delegator

# 2. Пополнить делегатора
./cpc-cli tx send <АДРЕС_ДЕЛЕГАТОРА> 500 --from faucet

# 3. Найти валидатора
./cpc-cli query validators

# 4. Делегировать
./cpc-cli tx delegate cpcvalcons1abc... 400 --from delegator

# 5. Проверить делегации
./cpc-cli query delegations <АДРЕС_ДЕЛЕГАТОРА>

# 6. Проверить награды (через несколько эпох)
./cpc-cli query rewards <АДРЕС_ДЕЛЕГАТОРА>
```

## Устранение неполадок

### Ключ не найден

```bash
# Проверить доступные ключи
./cpc-cli keys list

# Создать ключ при необходимости
./cpc-cli keys add <ИМЯ>
```

### Соединение отклонено

```bash
# Проверить статус ноды
curl http://localhost:8000/status

# Или указать URL ноды
./cpc-cli query balance cpc1... --node http://192.168.1.100:8000
```

### Недостаточный баланс

```bash
# Проверить баланс
./cpc-cli query balance <АДРЕС>

# Пополнить из faucet
./cpc-cli tx send <АДРЕС> <СУММА> --from faucet
```

## Следующие шаги

- **[Гид по стейкингу](staking-guide.md)** - Стейк, делегирование, награды
- **[Гид валидатора](validator-guide.md)** - Запуск ноды валидатора
- **[Справочник API](api-reference.md)** - RPC эндпоинты
