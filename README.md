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

## LAN stand site / Сайт на LAN-стенде

From the sibling blockchain repository / Из соседнего репозитория блокчейна:

```bash
./start_test.sh docs-up          # strict build + start/update static Nginx
./start_test.sh docs-status
./start_test.sh docs-logs
./start_test.sh docs-down        # only docs; leaves blockchain/monitoring running
```

Open [English](http://192.168.0.100:8008/) or [Русский](http://192.168.0.100:8008/ru/).
No login needed. The site uses the saved monitoring LAN address; override with
`--monitoring-host 192.168.0.100 --docs-port 8008`. Ordinary `start_test.sh up`
also builds/starts docs (`--no-docs` skips this); `cleanup.sh` stops the site.
After editing Markdown, run `docs-up` again. Docker restarts the site after a
host reboot unless explicitly stopped. HTTPS/public-domain deployment is separate.

Пароль не требуется. Адрес берётся из настройки мониторинга; флаги выше позволяют
выбрать другой LAN-адрес/порт. Обычный `up` включает сайт, `--no-docs` пропускает
его, `cleanup.sh` останавливает. После правки Markdown повторите `docs-up`.
Docker перезапускает сайт после reboot, если он не был остановлен явно.

Only generated HTML and Nginx config are mounted, read-only, into a non-root,
digest-pinned container. Per-stand releases/config live in `<devnet>/docs-site/`,
outside Git. Failed builds leave the previous release intact; no keys/node data,
source repository or Docker socket are served. The local origin uses trusted-LAN
HTTP; the public edge terminates HTTPS. Runtime releases are preserved on stop.

В контейнер read-only попадают только готовый HTML и Nginx config. Ключи, данные
нод, исходники и Docker socket не монтируются. Сборки — в `<devnet>/docs-site/`
вне Git; неудачная сборка не меняет предыдущую, остановка не удаляет данные.
Локальный origin использует HTTP доверенной LAN; публичный edge принимает HTTPS.

## Public site / Публичный сайт

[English](https://docs.computechain.space/) / [Русский](https://docs.computechain.space/ru/).
The existing edge Nginx forwards only this site's traffic to the LAN origin.
Set its canonical HTTPS URL once from the workspace; later docs-up keeps it:

```bash
python3 docs/stack.py up --site-url https://docs.computechain.space/
```

Сайт доступен по HTTPS через существующий edge Nginx. Команда выше сохраняет
canonical URL для последующих сборок. Ключи TLS находятся только на edge;
настройки и продление описаны в core PUBLIC_SITES.md. Документация по-прежнему
описывает экспериментальный локальный devnet, не production blockchain.

## Keeping it accurate / Актуальность

Check changes against `computechain/blockchain/comet/`, the operator scripts,
and the sibling monitoring repository. Update both languages together.
Distinguish working features, plans and measured experiments; publish matching
code/docs versions together. MIT license.

Сверяйте изменения с `computechain/blockchain/comet/`, operator scripts и
соседним monitoring-репозиторием. Обновляйте оба языка вместе. Отделяйте готовые
функции от планов и экспериментальных цифр; публикуйте согласованные версии
кода и документации. Лицензия MIT.
