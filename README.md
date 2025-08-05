# Telegram Bot Example

A clean, async-ready Telegram bot template built with [aiogram 3.x] (aiogram==3.21.0)

---

## 🚀 Key Features

- ⚡ **uvloop** — faster event loop (Linux-only)
- 📦 **Poetry** — modern dependency and virtualenv manager
- 🐬 **MySQL** via **asyncmy** using repository pattern
- 🔐 **Throttling middleware** — based on **TTLCache**
- 🧠 **DBPool middleware** — injects **MySQL + Redis** into context
- 👥 **User tracking** — saves users to database
- 📝 **Logging** — bot startup, messages, errors
- 🔁 **pm2** — for process management & production deployment

---

## ⚙️ Installation

```bash
git clone git@github.com:SkrudjReal/tgbot-example.git
cd tgbot-example
poetry install --no-root
cp settings.env.example settings.env  # Create and edit environment config
```

## Start

## Development

```bash
poetry run python3 main.py
```

## Production via pm2

# With ecosystem file
```bash
pm2 start ecosystem.config.js
pm2 save && pm2 startup
```

# or manually
```bash
pm2 start "poetry run python3 app.py" --name "tgbot-example"
pm2 save && pm2 startup
```

You are amazing.