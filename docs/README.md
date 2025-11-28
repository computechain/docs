# ComputeChain Documentation

Документация для ComputeChain, построенная с помощью MkDocs и Material for MkDocs.

## Поддержка языков

Документация поддерживает три языка:

- **English (en)** — по умолчанию
- **Русский (ru)**
- **中文 (zh)** — Китайский

## Установка

### Требования

- Python 3.12+
- pip

### Установка зависимостей

```bash
pip install mkdocs mkdocs-material
```

**Опционально** (для отображения дат изменений):

```bash
pip install mkdocs-git-revision-date-localized-plugin
```

После установки раскомментируйте плагин в `mkdocs.yml`:
```yaml
plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true
```

## Запуск локально

### Быстрый запуск (рекомендуется)

```bash
# Из корня проекта
chmod +x start_docs.sh
./start_docs.sh
```

Документация будет доступна по адресу: `http://localhost:8008` (или `http://<your-ip>:8008`)

### Режим разработки (вручную)

**Только localhost:**

```bash
mkdocs serve
```

Документация будет доступна по адресу: `http://127.0.0.1:8000`

**На всех интерфейсах:**

```bash
mkdocs serve -a 0.0.0.0:8008
```

Документация будет доступна по адресу: `http://<your-ip>:8008`

## Структура документации

```
docs/
├── en/                    # English (default)
│   ├── index.md
│   ├── understand/
│   ├── wallets/
│   ├── staking/
│   ├── mining/
│   ├── node/
│   ├── cli/
│   ├── testnet/
│   └── reference/
├── ru/                    # Русский
│   ├── index.md
│   └── ... (переводы)
└── zh/                    # 中文
    ├── index.md
    └── ... (переводы)
```

## Добавление переводов

### Структура файлов

Каждый язык имеет свою директорию (`en/`, `ru/`, `zh/`) с одинаковой структурой поддиректорий.

### Перевод страницы

1. Скопируйте файл из `en/` в соответствующую языковую директорию
2. Переведите содержимое
3. Обновите навигацию в `mkdocs.yml` (если нужно)

### Пример

```bash
# Скопировать файл для перевода
cp docs/en/understand/overview.md docs/ru/understand/overview.md

# Отредактировать и перевести
nano docs/ru/understand/overview.md
```

## Сборка

### Создание статических файлов

```bash
mkdocs build
```

Статические файлы будут созданы в директории `site/`.

### Развёртывание

```bash
# На GitHub Pages
mkdocs gh-deploy

# Или скопировать site/ на веб-сервер
rsync -av site/ user@server:/var/www/docs/
```

## Настройка nginx (опционально)

### Конфигурация для локального домена

```nginx
server {
    listen 80;
    server_name docs.localhost;

    location / {
        proxy_pass http://127.0.0.1:8008;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Конфигурация для продакшена

```nginx
server {
    listen 80;
    server_name docs.computechain.ru;

    location / {
        proxy_pass http://127.0.0.1:8008;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Обновление документации

### Добавление новой страницы

1. Создайте файл `.md` в соответствующей директории `en/`
2. Добавьте ссылку в `mkdocs.yml` в секцию `nav`
3. При необходимости создайте переводы в `ru/` и `zh/`

