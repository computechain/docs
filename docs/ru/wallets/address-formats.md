# Форматы адресов

ComputeChain использует **Bech32** кодирование для адресов с различными префиксами в зависимости от типа сущности.

## Типы адресов

### Аккаунты (Accounts)

**Префикс:** `cpc`

**Пример:** `cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

**Использование:**
- Обычные пользователи
- Получатели транзакций
- Адреса для наград валидаторов (`reward_address`)

**Генерация:**

```python
from computechain.protocol.crypto.keys import public_key_from_private
from computechain.protocol.crypto.address import address_from_pubkey

priv_key_bytes = bytes.fromhex("...")
pub_key_bytes = public_key_from_private(priv_key_bytes)
address = address_from_pubkey(pub_key_bytes, prefix="cpc")
```

### Валидаторы (Validators)

**Префикс:** `cpcvalcons` (consensus address)

**Пример:** `cpcvalcons1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

**Использование:**
- Идентификация валидаторов в консенсусе
- Адрес в `Validator.address`
- Используется в `BlockHeader.proposer_address`

**Генерация:**

```python
# При стейкинге указывается pub_key в payload
pub_key_hex = tx.payload.get("pub_key")
val_pub_bytes = bytes.fromhex(pub_key_hex)
val_addr = address_from_pubkey(val_pub_bytes, prefix="cpcvalcons")
```

**Важно:** Валидатор имеет два адреса:
- `cpcvalcons...` — для консенсуса (используется в блокчейне)
- `cpc1...` — для получения наград (обычный аккаунт)

### Operator Address (Future)

**Префикс:** `cpcvaloper`

**Статус:** Зарезервировано для будущего использования

**Планируемое использование:**
- Адрес оператора валидатора
- Отделение оператора от консенсус-адреса

## Структура адреса

**Bech32 формат:**

```
<prefix>1<data><checksum>
```

**Компоненты:**
- `prefix`: Префикс (cpc, cpcvalcons, cpcvaloper)
- `1`: Разделитель
- `data`: Закодированные данные (20 байт для адреса)
- `checksum`: Контрольная сумма для обнаружения ошибок

## Примеры использования

### Создание адреса из приватного ключа

```python
from computechain.cli.keystore import KeyStore

ks = KeyStore()
key = ks.create_key("alice")
print(f"Address: {key['address']}")  # cpc1...
print(f"Pubkey: {key['public_key']}")
```

### Получение адреса валидатора

```python
from computechain.protocol.crypto.address import address_from_pubkey

# Из публичного ключа валидатора
pub_key_hex = "02a1b2c3d4e5f6..."
pub_key_bytes = bytes.fromhex(pub_key_hex)
val_addr = address_from_pubkey(pub_key_bytes, prefix="cpcvalcons")
print(f"Validator address: {val_addr}")
```

### Проверка формата адреса

```python
def is_valid_address(address: str) -> bool:
    """Проверяет, является ли строка валидным адресом ComputeChain"""
    if not address:
        return False
    
    # Проверка префикса
    valid_prefixes = ["cpc", "cpcvalcons", "cpcvaloper"]
    if not any(address.startswith(p) for p in valid_prefixes):
        return False
    
    # Проверка формата Bech32
    try:
        from bech32 import bech32_decode
        hrp, data = bech32_decode(address)
        return hrp is not None and data is not None
    except:
        return False
```

## Конфигурация префиксов

**Параметры сети:**

```python
# protocol/config/params.py
bech32_prefix_acc: str = "cpc"           # Аккаунты
bech32_prefix_val: str = "cpcvaloper"    # Операторы (future)
bech32_prefix_cons: str = "cpcvalcons"   # Консенсус-адреса
```

**Разные сети могут иметь разные префиксы:**
- Devnet: `cpc`, `cpcvalcons`
- Testnet: `cpc`, `cpcvalcons`
- Mainnet: `cpc`, `cpcvalcons`

## Следующие шаги

- **[Keystore](keystore)** — Управление ключами
- **[Staking](staking/staking-basic)** — Как стать валидатором

