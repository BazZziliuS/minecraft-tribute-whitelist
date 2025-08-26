# 🚀 Minecraft Donation Whitelist (Folia + Tribute Webhook)

Этот проект поднимает два контейнера:

1. **Folia (Minecraft-сервер)**  
   - Версия: `1.21.8`  
   - С поддержкой RCON  
   - С автосохранением и автобэкапами  

2. **Backend (FastAPI)**  
   - Принимает вебхуки от Tribute  
   - Парсит ник из комментария к донату  
   - Через RCON добавляет игрока в whitelist  
   - Ведёт логи успешных и ошибочных добавлений

---

## ⚙️ Установка

### 1. Клонировать проект
```bash
git clone https://github.com/yourname/mc-donation-whitelist.git
cd mc-donation-whitelist
````

### 2. Структура проекта

```
.
├─ backend/                # код бэкенда
│   ├─ main.py             # FastAPI + логика работы с RCON
│   ├─ requirements.txt    # зависимости Python
│   └─ Dockerfile          # докер-образ для backend
├─ data/                   # данные Minecraft (миры, настройки и т.д.)
├─ plugins/                # плагины Minecraft
├─ config/                 # конфиги Minecraft
├─ logs/                   # сюда будут писаться success/errors
└─ docker-compose.yml      # общая конфигурация
```

---

## 🐳 Запуск

Собрать и запустить контейнеры:

```bash
docker compose up -d --build
```

Проверить, что сервисы поднялись:

```bash
docker compose ps
```

---

## 🌍 Вебхуки Tribute

Укажите в настройках Tribute webhook URL:

```
http://<ваш_сервер>:8000/webhook
```

При успешном донате с комментарием вида:

```
Player123
```

Игрок будет добавлен в whitelist Minecraft:

```
whitelist add Player123
```

---

## 📜 Логи

* Успешные добавления → `./logs/whitelist_success.log`
* Ошибки → `./logs/whitelist_errors.log`

Примеры строк:

```
[2025-08-26 18:30:01] ✅ Player123 → Added Player123 to whitelist
[2025-08-26 18:31:10] ❌ NO_NICK → Комментарий: "поддержка сервера"
```

---

## 🔧 Конфигурация

Все переменные задаются в `docker-compose.yml`:

### Minecraft (folia-1)

```yaml
ENABLE_RCON: "true"
RCON_PASSWORD: "super_secret_pass"
RCON_PORT: 25575
```

### Backend

```yaml
RCON_HOST: "folia-1"
RCON_PORT: 25575
RCON_PASSWORD: "super_secret_pass"
```

---

## 🚀 Автостарт

Чтобы проект стартовал после перезагрузки сервера, можно добавить systemd unit:

```ini
[Unit]
Description=Minecraft Folia + Backend
After=docker.service
Requires=docker.service

[Service]
Restart=always
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```

Сохранить как `/etc/systemd/system/mc.service` и активировать:

```bash
sudo systemctl enable --now mc.service
```

