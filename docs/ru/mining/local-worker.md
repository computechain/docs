# Локальный GPU Worker

Руководство по запуску локального воркера для выполнения синтетических задач.

## Статус реализации

**Текущая версия:** MVP (Stage 4)

**Функционал:**
- Генерация синтетических задач от хеша блока
- Mock выполнение вычислений (CPU/GPU)
- Отправка `SUBMIT_RESULT` транзакций в L1

**Будущая версия (Stage 5):**
- Реальные GPU вычисления (CUDA/ROCm)
- Подключение к PoC-валидатору
- Выполнение реальных задач из маркетплейса

## Требования

### Оборудование

- **GPU (опционально для MVP):** RTX 4090/5090 или аналогичные
- **CPU:** Достаточно для выполнения mock вычислений
- **RAM:** Минимум 4 GB

### Программное обеспечение

- **Python 3.12+**
- **ComputeChain CLI** (`cpc-cli`)
- **Доступ к L1-ноде** (локальной или удалённой)

## Быстрый старт

### Шаг 1: Создание ключа воркера

```bash
./cpc-cli keys add worker
```

**Вывод:**

```
Key 'worker' created.
Address: cpc1worker...
Pubkey:  02a1b2c3...
```

### Шаг 2: Пополнение баланса

```bash
WORKER_ADDR=$(./cpc-cli keys show worker | grep address | awk '{print $2}' | tr -d '",')
./cpc-cli tx send $WORKER_ADDR 100 --from faucet --node http://localhost:8000
```

**Важно:** Баланс должен покрывать комиссии за `SUBMIT_RESULT` транзакции (80,000 gas * gas_price).

### Шаг 3: Запуск воркера (MVP)

**Текущая реализация:**

Скрипт воркера пока не реализован. Ниже пример того, как он будет работать:

```python
# scripts/gpu_worker.py (планируется)

import time
import uuid
from computechain.cli.keystore import KeyStore
from computechain.protocol.types.tx import Transaction, TxType
from computechain.protocol.types.poc import ComputeResult
from computechain.protocol.crypto.hash import sha256

def generate_synthetic_task(block_hash: str, worker_address: str):
    """Генерирует синтетическую задачу от хеша блока"""
    seed = sha256((block_hash + worker_address).encode()).hex()
    return {
        "task_id": str(uuid.uuid4()),
        "challenge_type": "synthetic",
        "seed": seed,
        "matrix_size": 1024
    }

def execute_task(task):
    """Выполняет задачу (mock для MVP)"""
    # В будущем: реальные GPU вычисления
    # result = cuda_matrix_mul(task["seed"], task["matrix_size"])
    result = f"mock_result_{task['seed']}"
    result_hash = sha256(result.encode()).hex()
    return result_hash

def submit_result(worker_key, task_id, result_hash, node_url):
    """Отправляет результат в L1"""
    from computechain.cli.main import cmd_tx_submit_result
    
    # Формирование транзакции
    # ... (использует cmd_tx_submit_result из CLI)
    pass

def main():
    """Основной цикл воркера"""
    ks = KeyStore()
    worker_key = ks.get_key("worker")
    worker_address = worker_key['address']
    node_url = "http://localhost:8000"
    
    while True:
        # Получить последний блок
        # block_hash = get_latest_block_hash(node_url)
        
        # Генерировать задачу
        # task = generate_synthetic_task(block_hash, worker_address)
        
        # Выполнить задачу
        # result_hash = execute_task(task)
        
        # Отправить результат
        # submit_result(worker_key, task["task_id"], result_hash, node_url)
        
        # Ждать следующий блок
        time.sleep(10)  # Block time

if __name__ == "__main__":
    main()
```

## Использование CLI для отправки результатов

### Ручная отправка (текущий способ)

```bash
./cpc-cli tx submit-result \
  --task-id "550e8400-e29b-41d4-a716-446655440000" \
  --result-hash "0x1234567890abcdef..." \
  --from worker \
  --node http://localhost:8000
```

**Параметры:**

- `--task-id`: UUID задачи
- `--result-hash`: Хеш результата вычисления
- `--from`: Имя ключа воркера в keystore
- `--node`: URL L1-ноды

## Будущая реализация (Stage 5)

### Подключение к PoC-валидатору

**WebSocket протокол:**

```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    if data["type"] == "job":
        # Получена задача
        job_id = data["job_id"]
        task_id = data["task_id"]
        payload = data["payload"]
        
        # Выполнить задачу
        result_hash = execute_job(payload)
        
        # Отправить результат
        response = {
            "type": "job_result",
            "job_id": job_id,
            "worker_address": worker_address,
            "result_hash": result_hash,
            "proof": None
        }
        ws.send(json.dumps(response))

ws = websocket.WebSocketApp("ws://poc-validator:8080/worker",
                            on_message=on_message)
ws.run_forever()
```

### Реальные GPU вычисления

**Пример с CUDA:**

```python
import cupy as cp

def cuda_matrix_multiplication(seed: bytes, size: int):
    """Умножение матриц на GPU"""
    # Генерация матриц от seed
    cp.random.seed(int.from_bytes(seed[:4], 'big'))
    A = cp.random.rand(size, size)
    B = cp.random.rand(size, size)
    
    # Умножение на GPU
    C = cp.dot(A, B)
    
    # Возврат хеша результата
    result_bytes = C.tobytes()
    return sha256(result_bytes).hex()
```

## Мониторинг

### Проверка транзакций воркера

```bash
# Получить блок с SUBMIT_RESULT транзакцией
./cpc-cli query block <HEIGHT> --node http://localhost:8000 | jq '.txs[] | select(.tx_type == "SUBMIT_RESULT")'
```

### Проверка compute_root

```bash
# Получить заголовок блока
./cpc-cli query block <HEIGHT> --node http://localhost:8000 | jq '.header.compute_root'
```

## Troubleshooting

### Ошибка: Insufficient balance

**Причина:** Недостаточно баланса для оплаты комиссии

**Решение:**

```bash
# Пополнить баланс
./cpc-cli tx send <WORKER_ADDR> 10 --from faucet --node http://localhost:8000
```

### Ошибка: Invalid ComputeResult

**Причина:** Неверный формат payload

**Решение:** Убедитесь, что:
- `task_id` — валидный UUID
- `result_hash` — hex строка
- `worker_address` совпадает с `tx.from_address`

### Ошибка: Connection refused

**Причина:** L1-нода не запущена или недоступна

**Решение:**

```bash
# Проверить статус ноды
curl http://localhost:8000/status
```

## Следующие шаги

- **[Mining Overview](overview)** — Обзор майнинга
- **[Task Market](task-market)** — Публикация задач
- **[PoC Details](understand/poc)** — Детали Proof-of-Compute

