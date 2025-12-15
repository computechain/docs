# Документация ComputeChain

> Layer-1 блокчейн с Proof-of-Compute (PoC) и стейкингом валидаторов

## Быстрый старт

### Установка и запуск ноды

```bash
# Установка зависимостей
pip install -r requirements.txt

# Инициализация ноды
./run_node.py --datadir .node init

# Запуск ноды
./run_node.py --datadir .node start

# Открыть дашборд
open http://localhost:8000
```

### Создание кошелька

```bash
# Создать ключ
./cpc-cli keys add mykey

# Проверить баланс
./cpc-cli query balance <ВАШ_АДРЕС>
```

### Стать валидатором

```bash
# Застейкать 100 CPC (минимум)
./cpc-cli tx stake 100 --from mykey

# Проверить статус валидатора
./cpc-cli query validators
```

### Делегировать валидатору

```bash
# Делегировать токены для получения наград
./cpc-cli tx delegate <АДРЕС_ВАЛИДАТОРА> <СУММА> --from mykey

# Проверить делегации
./cpc-cli query delegations <ВАШ_АДРЕС>

# Проверить награды
./cpc-cli query rewards <ВАШ_АДРЕС>
```

## Документация

- **[Гид по стейкингу](staking-guide.md)** - Стейкинг, делегирование, награды
- **[Гид валидатора](validator-guide.md)** - Запуск валидатора, управление жизненным циклом
- **[Справочник CLI](cli-reference.md)** - Полный список команд CLI
- **[Справочник API](api-reference.md)** - RPC эндпоинты
- **[Продвинутые темы](advanced.md)** - PoC, токеномика, архитектура

## Ключевые возможности

✅ **Multi-Validator PoA** - Производство блоков по очереди (round-robin)
✅ **Делегирование и награды** - Делегируйте токены, получайте пропорциональные награды
✅ **Модель комиссии** - Валидаторы получают комиссию 10% (настраивается)
✅ **Отслеживание производительности** - Подсчет uptime, автоматический jailing
✅ **Градуированный слэшинг** - Прогрессивные штрафы (5% → 10% → 100%)
✅ **Готовность к пост-квантовой криптографии** - Архитектура PQ-подписей

## Информация о сети

**Testnet:**
- Chain ID: `computechain-testnet-1`
- RPC: `https://rpc.testnet.computechain.space`
- Explorer: `https://explorer.testnet.computechain.space`

## Поддержка

- **GitHub:** [github.com/computechain/computechain](https://github.com/computechain/computechain)
- **Issues:** Сообщайте об ошибках через GitHub Issues
- **Discord:** [discord.gg/computechain](https://discord.gg/computechain)
