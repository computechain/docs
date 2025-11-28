# Конфигурация Ноды

Параметры сети и конфигурация ноды ComputeChain.

## Параметры Сети

### NetworkConfig

**Расположение:** `protocol/config/params.py`

**Структура:**

```python
class NetworkConfig:
    network_id: str              # "devnet", "testnet", "mainnet"
    chain_id: str               # "cpc-devnet-1", etc.
    block_time_sec: int         # Время между блоками (сек)
    min_gas_price: int          # Минимальная цена газа (wei)
    block_gas_limit: int        # Максимум газа на блок
    max_tx_per_block: int       # Максимум транзакций
    genesis_premine: int        # Премайн в генезисе (wei)
    bech32_prefix_acc: str      # Префикс адреса аккаунта
    bech32_prefix_val: str      # Префикс адреса валидатора (future)
    bech32_prefix_cons: str     # Префикс адреса консенсуса
    epoch_length_blocks: int    # Длительность эпохи (блоки)
    min_validator_stake: int    # Минимальный стейк (wei)
    max_validators: int         # Максимум валидаторов
```

## Сети

### Devnet

**Параметры:**

```python
NetworkConfig(
    network_id="devnet",
    chain_id="cpc-devnet-1",
    block_time_sec=10,
    min_gas_price=1000,
    block_gas_limit=10_000_000,
    max_tx_per_block=100,
    genesis_premine=1_000_000_000 * 10**18,  # 1B CPC
    epoch_length_blocks=10,
    min_validator_stake=1000 * 10**18,  # 1,000 CPC
    max_validators=5
)
```

**Использование:**
- Локальная разработка
- Тестирование
- Детерминированный ключ faucet

### Testnet

**Параметры:**

```python
NetworkConfig(
    network_id="testnet",
    chain_id="cpc-testnet-1",
    block_time_sec=30,
    min_gas_price=5000,
    block_gas_limit=15_000_000,
    max_tx_per_block=1000,
    genesis_premine=100_000_000 * 10**18,  # 100M CPC
    epoch_length_blocks=100,
    min_validator_stake=100_000 * 10**18,  # 100,000 CPC
    max_validators=21
)
```

**Использование:**
- Публичный тестнет
- Интеграционное тестирование
- Подготовка к mainnet

### Mainnet

**Параметры:**

```python
NetworkConfig(
    network_id="mainnet",
    chain_id="cpc-mainnet-1",
    block_time_sec=60,
    min_gas_price=1_000_000_000,  # 1 Gwei
    block_gas_limit=30_000_000,
    max_tx_per_block=5000,
    genesis_premine=0,  # Fair launch
    epoch_length_blocks=72,  # ~72 минуты
    min_validator_stake=100_000 * 10**18,  # 100,000 CPC
    max_validators=100
)
```

**Использование:**
- Продакшн сеть
- Реальные транзакции и токены

## Стоимость Газа

### Базовая стоимость

**Расположение:** `protocol/config/params.py`

```python
GAS_PER_TYPE = {
    TxType.TRANSFER:      21_000,
    TxType.STAKE:         40_000,
    TxType.SUBMIT_RESULT: 80_000,
}
```

**Расчет комиссии:**

```python
fee = gas_used * gas_price
```

**Примеры:**

| Тип транзакции | Gas Used | Gas Price (Devnet) | Fee (wei) | Fee (CPC) |
|-----------------|----------|-------------------|-----------|-----------|
| TRANSFER | 21,000 | 1,000 | 21,000,000 | 0.000021 |
| STAKE | 40,000 | 1,000 | 40,000,000 | 0.00004 |
| SUBMIT_RESULT | 80,000 | 1,000 | 80,000,000 | 0.00008 |

## Переключение сети

### Текущая сеть

**По умолчанию:** Devnet

```python
# protocol/config/params.py
CURRENT_NETWORK = NETWORKS["devnet"]
```

### Изменение сети

**В коде:**

```python
from computechain.protocol.config.params import NETWORKS, CURRENT_NETWORK

# Переключиться на testnet
CURRENT_NETWORK = NETWORKS["testnet"]
```

**Через переменную окружения (Future):**

```bash
export CPC_NETWORK=testnet
./run_node.py --datadir .node_a run
```

## Параметры Ноды

### RPC Сервер

**Параметры запуска:**

```bash
./run_node.py --datadir .node_a run \
  --host 0.0.0.0 \
  --port 8000
```

**По умолчанию:**
- Host: `0.0.0.0` (все интерфейсы)
- Port: `8000`

**Безопасность:**
- В продакшене используйте `127.0.0.1` или файрвол
- Настройте HTTPS через reverse proxy (nginx)

### P2P Сервер

**Параметры запуска:**

```bash
./run_node.py --datadir .node_a run \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000
```

**По умолчанию:**
- Host: `0.0.0.0`
- Port: `9000`

**Файрвол:**
- Откройте порт для входящих соединений
- Рекомендуется использовать статический IP

### Пиры

**При запуске:**

```bash
./run_node.py --datadir .node_a run \
  --peers 192.168.1.100:9000,192.168.1.101:9000
```

**Автоматическое сохранение:**

- Пиры сохраняются в `peers.json`
- Автоматически подключаются при следующем запуске

## Пересборка стейта (Rebuild State)

### Когда нужно

**Случаи:**

- Повреждение стейта
- Изменение логики стейта
- Отладка

### Как выполнить

```bash
./run_node.py --datadir .node_a run --rebuild-state
```

**Процесс:**

1. Загрузка всех блоков из базы данных
2. Повторное применение транзакций
3. Пересчет стейта
4. Сохранение нового стейта

## Переменные окружения

### CPC_NODE

**Использование:** URL ноды для CLI

```bash
export CPC_NODE=http://localhost:8000
./cpc-cli query balance cpc1...
```

### CPC_NETWORK (Future)

**Использование:** Выбор сети

```bash
export CPC_NETWORK=testnet
./run_node.py --datadir .node_a run
```

## Примеры конфигурации

### Локальная разработка

```bash
# Node A
./run_node.py --datadir .node_a run \
  --port 8000 \
  --p2p-port 9000

# Node B
./run_node.py --datadir .node_b run \
  --port 8001 \
  --p2p-port 9001 \
  --peers 127.0.0.1:9000
```

### Testnet Валидатор

```bash
./run_node.py --datadir .testnet_node run \
  --host 0.0.0.0 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers testnet-peer-1:9000,testnet-peer-2:9000
```

### Продакшн Нода

```bash
./run_node.py --datadir .mainnet_node run \
  --host 127.0.0.1 \
  --port 8000 \
  --p2p-host 0.0.0.0 \
  --p2p-port 9000 \
  --peers mainnet-peer-1:9000,mainnet-peer-2:9000
```

**Рекомендации:**

- Используйте reverse proxy (nginx) для HTTPS
- Настройте мониторинг (Prometheus, Grafana)
- Настройте логирование в файл
- Используйте systemd для автозапуска

## Следующие шаги

- **[Запуск локально](run-local.md)** — Запуск локальной ноды
- **[P2P синхронизация](p2p-sync.md)** — Синхронизация сети
- **[Руководство CLI](../cli/cpc-cli.md)** — Использование CLI

