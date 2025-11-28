# ComputeChain Documentation

> **⚠️ Living Documentation**  
> This documentation is actively maintained and will be updated as the ComputeChain project evolves. Some features described here may be in development or planned for future releases.

This repository contains the complete documentation for **ComputeChain** — an experimental Layer-1 blockchain with Proof-of-Compute architecture.

---

## 📖 Documentation Site

The documentation is built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

**Live site:** [https://docs.computechain.space](https://docs.computechain.space) *(planned)*

---

## 🚀 Local Development

**Prerequisites:**
- Python 3.12+
- pip

**Setup:**

```bash
pip install mkdocs mkdocs-material mkdocs-static-i18n
```

**Run locally:**

```bash
mkdocs serve -a 0.0.0.0:8008
```

Documentation will be available at `http://localhost:8008`

---

## 📁 Structure

```
docs/
├── docs/            # Documentation source files
│   ├── en/          # English documentation
│   └── ru/          # Russian documentation
├── mkdocs.yml       # MkDocs configuration
└── site/            # Generated site (gitignored)
```

---

## 🌐 Supported Languages

- 🇬🇧 **English** (default)
- 🇷🇺 **Русский** (Russian)

---

## 📄 License

**MIT License**

---

## 🔗 Related Repositories

- **[ComputeChain Core](https://github.com/computechain/computechain)** — Main blockchain implementation

