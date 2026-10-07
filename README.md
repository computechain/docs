# ComputeChain documentation / Документация

Four short pages per language, describing the current CometBFT devnet, not
legacy feature claims. English and Russian have the same structure.

Четыре короткие страницы на язык: обзор, запуск, архитектура, разработка.
Документация соответствует текущему CometBFT-стенду, а не старым обещаниям.

- [English](docs/en/index.md)
- [Русский](docs/ru/index.md)

## Build / Сборка

From this repository; Python 3.12 and pip required. Dependencies stay local.

Из этого репозитория; нужны Python 3.12 и pip. Зависимости устанавливаются локально.

```bash
python3 -m venv ../.tools/docs-venv --without-pip
pip --python ../.tools/docs-venv install -r requirements.txt
../.tools/docs-venv/bin/mkdocs build --strict
../.tools/docs-venv/bin/mkdocs serve -a 192.168.0.100:8008
```

Open [English](http://192.168.0.100:8008/) or [Русский](http://192.168.0.100:8008/ru/)
while the preview server runs. Replace the address on a different LAN host.
Ctrl-C stops the preview. No deployment or push is performed by these commands.

Откройте English или Русский по ссылкам выше, пока preview работает.
На другом LAN-хосте замените адрес. Ctrl-C останавливает preview.
Эти команды ничего не публикуют и не пушат.

Generated `site/` is ignored by Git. Old documents remain in Git history.
Do not restore stale staking/API instructions into the current navigation.

Сборка `site/` исключена из Git. Старые страницы доступны в истории Git.
Устаревшие staking/API-инструкции не должны возвращаться в актуальное меню.

## Keeping it accurate / Актуальность

Check changes against `computechain/blockchain/comet/`, the operator scripts,
and the sibling monitoring repository. Update both languages together.
Distinguish working features, plans and measured experiments; publish matching
code/docs versions together. MIT license.

Сверяйте изменения с `computechain/blockchain/comet/`, operator scripts и
соседним monitoring-репозиторием. Обновляйте оба языка вместе. Отделяйте готовые
функции от планов и экспериментальных цифр; публикуйте согласованные версии
кода и документации. Лицензия MIT.
