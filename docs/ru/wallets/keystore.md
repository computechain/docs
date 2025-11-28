# Управление ключами (Keystore)

ComputeChain CLI (`cpc-cli`) предоставляет инструменты для управления ключами через keystore.

## Расположение ключей

**Директория:** `~/.computechain/keys/`

**Структура:**

```
~/.computechain/keys/
├── alice.json
├── bob.json
└── faucet.json
```

**Формат файла ключа:**

```json
{
  "name": "alice",
  "address": "cpc1...",
  "public_key": "02a1b2c3...",
  "private_key": "4f3edf98..."
}
```

**⚠️ Важно:** В MVP ключи хранятся **незашифрованными**. Не делитесь файлами ключей!

## Команды CLI

### Создание нового ключа

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

### Импорт существующего ключа

```bash
./cpc-cli keys import <NAME> --private-key <HEX_PRIVATE_KEY>
```

**Пример:**

```bash
./cpc-cli keys import faucet --private-key 4f3edf982522b4e51b7e8b5f2f9c4d1d7a9e5f8c2b6d4e1a3c5b7d9e0f1a2b3c
```

**Использование:**
- Импорт ключа faucet из Node A в CLI
- Восстановление ключа из резервной копии

### Список ключей

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

### Показать детали ключа

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

**Примечание:** Приватный ключ не отображается в выводе для безопасности.

## Программный доступ

### Использование KeyStore в Python

```python
from computechain.cli.keystore import KeyStore

# Создать экземпляр
ks = KeyStore()

# Создать новый ключ
key = ks.create_key("alice")
print(f"Address: {key['address']}")

# Получить существующий ключ
alice_key = ks.get_key("alice")
if alice_key:
    print(f"Address: {alice_key['address']}")
    print(f"Pubkey: {alice_key['public_key']}")
    # ⚠️ Приватный ключ доступен в alice_key['private_key']

# Импортировать ключ
imported_key = ks.import_key("bob", "4f3edf982522b4e51b7e8b5f2f9c4d1d7a9e5f8c2b6d4e1a3c5b7d9e0f1a2b3c")

# Список всех ключей
all_keys = ks.list_keys()
for k in all_keys:
    print(f"{k['name']}: {k['address']}")
```

## Безопасность

### Текущие ограничения (MVP)

**⚠️ Ключи хранятся незашифрованными:**

- Файлы в `~/.computechain/keys/` содержат приватные ключи в открытом виде
- Не делитесь этими файлами
- Не коммитьте их в Git
- Делайте резервные копии в безопасном месте

### Рекомендации

1. **Резервные копии:**
   ```bash
   # Сохранить приватные ключи в безопасном месте
   cat ~/.computechain/keys/alice.json | jq -r '.private_key' > alice_privkey_backup.txt
   # Хранить резервную копию в зашифрованном хранилище (например, менеджер паролей)
   ```

2. **Права доступа к файлам:**
   ```bash
   # Ограничить доступ к директории ключей
   chmod 700 ~/.computechain/keys/
   ```

3. **Разные ключи для разных целей:**
   - Отдельный ключ для валидатора
   - Отдельный ключ для обычных транзакций
   - Не используйте ключ faucet для продакшена

### Будущие улучшения

**Планируется:**
- Шифрование ключей паролем
- Поддержка аппаратных кошельков
- Мультиподписные кошельки

## Интеграция с нодой

### Использование ключа валидатора

**Node A (Genesis):**

```bash
# Ключ валидатора находится в:
.node_a/validator_key.hex
```

**Node B:**

```bash
# Ключ валидатора экспортирован из CLI:
python3 -c "from computechain.cli.keystore import KeyStore; print(KeyStore().get_key('alice')['private_key'])" > .node_b/validator_key.hex
```

### Использование ключа faucet

**Node A:**

```bash
# Ключ faucet находится в:
.node_a/faucet_key.hex
```

**Импорт в CLI:**

```bash
./cpc-cli keys import faucet --private-key $(cat .node_a/faucet_key.hex)
```

## Примеры использования

### Сценарий: Создание валидатора

```bash
# 1. Создать ключ Alice
./cpc-cli keys add alice

# 2. Получить адрес Alice
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 3. Пополнить баланс Alice (из faucet)
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000

# 4. Застейкать Alice
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000

# 5. Экспортировать ключ для ноды
python3 -c "from computechain.cli.keystore import KeyStore; print(KeyStore().get_key('alice')['private_key'])" > validator_key.hex
```

## Следующие шаги

- **[Форматы адресов](address-formats.md)** — Форматы адресов
- **[Стейкинг](../staking/staking-basic.md)** — Как стать валидатором
- **[Руководство CLI](../cli/cpc-cli.md)** — Полный список команд CLI
