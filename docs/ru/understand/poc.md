# Proof-of-Compute (PoC)

## Концепция

**Proof-of-Compute** — механизм, который заменяет бессмысленный хешрейт классического Proof-of-Work на **полезные вычисления**, выполняемые на GPU.

Вместо поиска nonce, удовлетворяющего условию хеша, воркеры выполняют реальные вычислительные задачи и предоставляют доказательства корректного выполнения.

## Архитектура PoC

### Интеграция с L1

**В заголовке блока:**

```python
class BlockHeader:
    # ... другие поля ...
    compute_root: str  # Merkle root результатов вычислений
    zk_state_proof: Optional[str] = None  # Зарезервировано для ZK-proofs
    zk_compute_proof: Optional[str] = None  # Зарезервировано для ZK-proofs
```

**`compute_root`** вычисляется как Merkle root всех транзакций `ComputeResult` в блоке:

```python
def compute_poc_root(txs: List[Transaction]) -> str:
    leaves = []
    for tx in txs:
        if tx.tx_type == TxType.SUBMIT_RESULT:
            res = ComputeResult(**tx.payload)
            data = res.model_dump_json().encode("utf-8")
            leaves.append(sha256(data))
    
    if not leaves:
        return ""
    
    return compute_merkle_root(leaves).hex()
```

### Структуры данных

#### ComputeTask

**Статус:** В разработке (Stage 5)

Задача для выполнения на GPU:

```python
class ComputeTask:
    task_id: str  # UUID задачи
    challenge_type: str  # "matrix_mul", "synthetic", и т.д.
    payload: dict  # Параметры задачи (seed, matrix_size, и т.д.)
    reward: int  # Награда за выполнение (CPC)
    deadline: int  # Дедлайн (timestamp)
```

#### ComputeResult

**Реализовано:** ✅ Stage 4

Результат выполнения задачи:

```python
class ComputeResult:
    task_id: str  # UUID задачи
    worker_address: str  # Адрес воркера (cpc1...)
    result_hash: str  # Хеш результата
    proof: Optional[str] = None  # Доказательство корректности (будущее: ZK-proof)
    nonce: Optional[int] = None  # Для синтетических задач
    signature: Optional[str] = None  # Подпись воркера
```

### Транзакция SUBMIT_RESULT

**Тип транзакции:** `TxType.SUBMIT_RESULT`

**Стоимость газа:** 80,000 gas

**Payload:**

```json
{
  "task_id": "uuid-here",
  "worker_address": "cpc1...",
  "result_hash": "0x...",
  "proof": "...",
  "nonce": 12345,
  "signature": "..."
}
```

**Валидация:**

1. Структура `ComputeResult` должна быть валидной
2. `worker_address` должен совпадать с `tx.from_address`
3. Доказательство проверяется (будущее: через ZK-верификацию)

## Процесс выполнения задач

### Текущая реализация (Stage 4)

**Упрощённый поток:**

1. **Воркер** генерирует задачу из хеша блока (синтетическая)
2. **Воркер** выполняет вычисление (CPU/GPU mock)
3. **Воркер** отправляет транзакцию `SUBMIT_RESULT` в L1
4. **L1 валидатор** проверяет структуру и включает в блок
5. **`compute_root`** обновляется в заголовке блока

### Будущая реализация (Stage 5)

**Полный поток с маркетплейсом:**

1. **Пользователь** создаёт задачу через Task Market API
2. **PoC валидатор** получает задачу и разбивает на задания
3. **PoC валидатор** распределяет задания между воркерами через WebSocket
4. **Воркер** выполняет задачу на GPU
5. **Воркер** отправляет результат с доказательством обратно
6. **PoC валидатор** проверяет результат (выборочная верификация)
7. **PoC валидатор** или **Воркер** отправляет `SUBMIT_RESULT` в L1
8. **L1 валидатор** включает транзакцию в блок
9. **Воркер** получает награду (off-chain или через L1 reward)

## Типы задач

### Синтетические задачи

**Назначение:** Стресс-тест и бенчмарк GPU

**Тип:** `challenge_type: "synthetic"`

**Свойства:**
- Детерминированный вывод
- Быстрая верификация
- Генерируется из хеша блока

**Пример:**

```python
# Генерация задачи из хеша блока
block_hash = get_latest_block_hash()
seed = sha256(block_hash + worker_address)
matrix_size = 1024

# Выполнение
result = matrix_multiplication(seed, matrix_size)
result_hash = sha256(result)
```

### Реальные задачи (Будущее)

**Назначение:** Полезные вычисления (inference, training, и т.д.)

**Тип:** `challenge_type: "inference"`, `"training"`, и т.д.

**Свойства:**
- Загружаются через Task Market
- Оплачиваются пользователем
- Проверяются через ZK-proofs или дублирующее выполнение

## Верификация результатов

### Текущая реализация

**MVP:** Валидация структуры данных

- Проверка формата `ComputeResult`
- Проверка совпадения адреса
- Результат принимается, если структура валидна

### Будущая реализация

**ZK-Proofs:**

- Воркер генерирует ZK-proof корректного выполнения
- L1 валидатор проверяет доказательство без пересчёта
- Быстрая верификация даже для сложных задач

**Выборочная верификация:**

- PoC валидатор выбирает случайные результаты для проверки
- Дублирующее выполнение на других воркерах
- Slashing за некорректные результаты

## Награды за вычисления

### Текущая реализация

**Статус:** Off-chain (в PoC валидаторе) или через простой бонус в `_distribute_rewards`

Награды ещё не интегрированы в L1 на уровне протокола.

### Будущая реализация

**Интеграция с L1:**

- Награды за транзакции `SUBMIT_RESULT`
- Распределение через `_distribute_rewards`
- Рейтинг воркера в стейте (off-chain или on-chain)

## Следующие шаги

- **[GPU Workers](../mining/overview.md)** — Как стать воркером
- **[Task Market](../mining/task-market.md)** — Публикация задач
- **[Local Worker](../mining/local-worker.md)** — Запуск локального воркера

