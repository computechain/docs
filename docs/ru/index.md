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

- ✅ **Консенсус Tendermint BFT** - Византийская отказоустойчивость, мгновенная финальность
- ✅ **Делегирование и награды** - Делегируйте токены, получайте пропорциональные награды
- ✅ **Модель комиссии** - Валидаторы получают комиссию (макс. 20%, настраивается)
- ✅ **Управление валидаторами** - Автоматический jailing за простой
- ✅ **Защита от слэшинга** - Экономические штрафы за нарушения (базовая ставка 5%)
- ✅ **Готовность к пост-квантовой криптографии** - Схема подписи Dilithium3 (PQ)

## Информация о сети

**Devnet (Локальная):**
- Chain ID: `cpc-devnet-1`
- RPC: `http://localhost:8000`
- Метрики: `http://localhost:8000/metrics`

**Testnet (Скоро):**
- Chain ID: `cpc-testnet-1`
- RPC: TBA
- Explorer: TBA

## Поддержка

- **GitHub:** [github.com/computechain/computechain](https://github.com/computechain/computechain)
- **Issues:** Сообщайте об ошибках через GitHub Issues
- **Discord:** [discord.gg/computechain](https://discord.gg/computechain)
