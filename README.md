[🇷🇺 Русская версия](README_RU.md) | [🇬🇧 English version](README.md)

# 🚀 Minecraft Donation Whitelist (Folia + Tribute Webhook)

This project runs two containers:

1. **Folia (Minecraft server)**

   * Version: `1.21.8`
   * With RCON support
   * With autosave and autobackups

2. **Backend (FastAPI)**

   * Receives webhooks from Tribute
   * Parses the nickname from the donation comment and the donation name
   * Adds the player to the whitelist via RCON
   * Logs successful and failed additions

---

## ⚙️ Installation

### 1. Clone the project

```bash
git clone https://github.com/BazZziliuS/minecraft-tribute-whitelist.git
cd minecraft-tribute-whitelist
```

### 2. Project structure

```
.
├─ backend/                # backend code
│   ├─ main.py             # FastAPI + RCON logic
│   ├─ requirements.txt    # Python dependencies
│   └─ Dockerfile          # backend Docker image
├─ data/                   # Minecraft data (worlds, configs, etc.)
├─ plugins/                # Minecraft plugins
├─ config/                 # Minecraft configs
├─ logs/                   # success/error logs
└─ docker-compose.yml      # main configuration
```

---

## 🐳 Run

Build and start the containers:

```bash
docker compose up -d --build
```

Check that the services are running:

```bash
docker compose ps
```

---

## 🌍 Tribute Webhooks

Set the webhook URL in Tribute settings:

```
http://<your_server>:8000/webhook
```

When a donation with a comment like:

```
Player123
```

is received, the player will be added to the Minecraft whitelist:

```
whitelist add Player123
```

---

## 📜 Logs

* Successful additions → `./logs/whitelist_success.log`
* Errors → `./logs/whitelist_errors.log`

Example entries:

```
[2025-08-26 18:30:01] ✅ Player123 → Added Player123 to whitelist
[2025-08-26 18:31:10] ❌ NO_NICK → Comment: "support server"
```

---

## 🔧 Configuration

All variables are set in `docker-compose.yml`:

### Minecraft (Folia)

```yaml
ENABLE_RCON: "true"
RCON_PASSWORD: "super_secret_pass"
RCON_PORT: 25575
```

### Backend

```yaml
RCON_HOST: "folia"
RCON_PORT: 25575
RCON_PASSWORD: "super_secret_pass"
ALLOWED_DONATION_NAME: "Whitelist Access"
DONATE_CURRENCY: "EUR"
DONATE_AMOUNT: 1
```

---

## 🚀 Autostart

To make the project start after server reboot, add a systemd unit:

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

Save as `/etc/systemd/system/mc.service` and enable it:

```bash
sudo systemctl enable --now mc.service
```
