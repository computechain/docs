# Подключение к Тестнету

Руководство по подключению к публичному тестнету ComputeChain.

## Статус Тестнета

**Текущая версия:** 🚧 В разработке

**Планируемый запуск:** После завершения Stage 4

**Параметры тестнета:**

- Network ID: `testnet`
- Chain ID: `cpc-testnet-1`
- Block Time: 30 секунд
- Epoch Length: 100 блоков (~50 минут)
- Min Validator Stake: 100,000 CPC
- Max Validators: 21

## Подготовка

### Требования

- Python 3.12+
- ComputeChain нода (последняя версия)
- Минимум 100,000 CPC для валидатора (или меньше для обычной ноды)
- Стабильное интернет-соединение
- Открытый порт 9000 (для P2P)

### Установка

```bash
git clone https://github.com/computechain/computechain.git
cd computechain
pip install -r requirements.txt
chmod +x cpc-cli run_node.py
```

## Получение genesis.json

### Из официального источника

**После запуска тестнета:**

```bash
# Скачать genesis.json
curl https://testnet.computechain.ru/genesis.json > genesis.json

# Или через GitHub
wget https://raw.githubusercontent.com/computechain/testnet/main/genesis.json
```

**Верификация:**

```bash
cat genesis.json | jq '.header.height'  # Должно быть 0
cat genesis.json | jq '.header.chain_id'  # Должно быть "cpc-testnet-1"
```

## Получение списка пиров

### Из официального источника

**После запуска тестнета:**

```bash
# Получить список пиров
curl https://testnet.computechain.ru/peers.json

# Или через GitHub
wget https://raw.githubusercontent.com/computechain/testnet/main/peers.json
```

**Формат:**

```json
[
  "testnet-peer-1.computechain.ru:9000",
  "testnet-peer-2.computechain.ru:9000",
  "192.168.1.100:9000"
]
```

## Запуск Ноды

### Инициализация

```bash
./run_node.py --datadir .testnet_node init
```

**Важно:** Замените `genesis.json` на версию тестнета:

```bash
cp genesis.json .testnet_node/genesis.json
```

### Запуск с пирами

```bash
./run_node.py --datadir .testnet_node run \
  --peers testnet-peer-1.computechain.ru:9000,testnet-peer-2.computechain.ru:9000
```

### Проверка подключения

**Через статус:**

```bash
curl http://localhost:8000/status
```

**Вывод:**

```json
{
  "height": 12345,
  "last_hash": "0x...",
  "network": "testnet",
  "mempool_size": 5,
  "epoch": 123
}
```

**Проверка синхронизации:**

- `height` должен увеличиваться
- `network` должен быть `"testnet"`
- Логи показывают подключения к пирам

## Становление Валидатором

### Получение токенов

**Faucet (если доступен):**

```bash
# Запросить токены через faucet
curl -X POST https://testnet.computechain.ru/faucet \
  -H "Content-Type: application/json" \
  -d '{"address": "cpc1your_address..."}'
```

**Или через биржу:**

- Купить токены на DEX
- Получить от других участников

### Стейкинг

```bash
# Создать ключ
./cpc-cli keys add validator

# Получить адрес
VALIDATOR_ADDR=$(./cpc-cli keys show validator | grep address | awk '{print $2}' | tr -d '",')

# Пополнить баланс (минимум 100,000 CPC + комиссии)
# ... (через faucet или биржу)

# Застейкать
./cpc-cli tx stake 100000 --from validator --node http://localhost:8000
```

### Ожидание активации

**Эпоха:** 100 блоков (~50 минут)

**Проверка:**

```bash
./cpc-cli query validators --node http://localhost:8000
```

**После эпохи:**

- Валидатор должен появиться в списке
- `is_active` должно быть `true`
- Валидатор начнет производить блоки в Round-Robin

## Мониторинг

### Проверка статуса ноды

```bash
curl http://localhost:8000/status
```

### Проверка валидаторов

```bash
./cpc-cli query validators --node http://localhost:8000
```

### Проверка баланса

```bash
./cpc-cli query balance <ADDRESS> --node http://localhost:8000
```

### Логи ноды

**Типичные логи:**

```
Starting ComputeChain node...
Data DB: .testnet_node/chain.db
RPC: 0.0.0.0:8000
P2P: 0.0.0.0:9000
Connected to peer testnet-peer-1.computechain.ru:9000
Handshake completed with testnet-peer-1.computechain.ru:9000
Syncing blocks: 0 -> 12345
Block 12345 added. Hash: 0x... (Round 0)
```

## Устранение неполадок

### Проблема: Не удается подключиться к пирам

**Причины:**

- Пиры недоступны
- Файрвол блокирует подключения
- Некорректный genesis.json

**Решение:**

```bash
# Проверить доступность пира
telnet testnet-peer-1.computechain.ru 9000

# Проверить файрвол
sudo ufw status
sudo ufw allow 9000/tcp

# Проверить genesis.json
cat .testnet_node/genesis.json | jq '.header.chain_id'
```

### Проблема: Нода не синхронизируется

**Причины:**

- Нет подключений к пирам
- Лаг слишком большой
- Проблемы с сетью

**Решение:**

```bash
# Добавить больше пиров
./run_node.py --datadir .testnet_node run \
  --peers peer1:9000,peer2:9000,peer3:9000

# Проверить подключения
cat .testnet_node/peers.json
```

### Проблема: Genesis mismatch

**Причина:** Некорректный genesis.json

**Решение:**

```bash
# Скачать правильный genesis.json
curl https://testnet.computechain.ru/genesis.json > .testnet_node/genesis.json

# Перезапустить ноду
./run_node.py --datadir .testnet_node run
```

## Полезные ссылки

- **Explorer:** https://explorer.testnet.computechain.ru (планируется)
- **Faucet:** https://faucet.testnet.computechain.ru (планируется)
- **Discord/Telegram:** (ссылки будут добавлены после запуска)

## Следующие шаги

- **[Известные проблемы](known-issues.md)** — Известные проблемы
- **[Bug Bounty](bug-bounty.md)** — Сообщить об ошибке
- **[Настройка ноды](../node/run-local.md)** — Конфигурация ноды

