import os
import re
from datetime import datetime
from fastapi import FastAPI, Request
from mcrcon import MCRcon

RCON_HOST = os.getenv("RCON_HOST", "minecraft")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
RCON_PASSWORD = os.getenv("RCON_PASSWORD", "12345")

LOG_DIR = "/logs"
SUCCESS_LOG = os.path.join(LOG_DIR, "whitelist_success.log")
ERROR_LOG = os.path.join(LOG_DIR, "whitelist_errors.log")

# 🔹 Название доната, по которому разрешено добавление в whitelist
ALLOWED_DONATION_NAME = os.getenv("ALLOWED_DONATION_NAME", "Whitelist доступ")

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    event_name = data.get("name")
    payload = data.get("payload", {})
    message = payload.get("message", "")
    donation_name = payload.get("donation_name", "")

    # Проверяем, что донат с нужным названием
    if donation_name != ALLOWED_DONATION_NAME:
        log_error("WRONG_DONATION", f"{event_name} → donation_name={donation_name}")
        return {"status": "ignored", "reason": "donation_name mismatch"}

    if event_name in ["new_donation", "recurrent_donation"]:
        nickname = extract_nickname(message)
        if nickname:
            try:
                with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                    resp = mcr.command(f"whitelist add {nickname}")
                    log_success(nickname, f"{event_name} → {resp}")
            except Exception as e:
                log_error(nickname, f"{event_name} → {e}")
        else:
            log_error("NO_NICK", f"{event_name} → Сообщение: {message}")

    elif event_name == "cancelled_donation":
        log_error("CANCEL", f"cancelled_donation → {payload}")

    else:
        log_error("UNKNOWN_EVENT", f"{event_name} → {payload}")

    return {"status": "ok"}


def extract_nickname(message: str) -> str | None:
    match = re.search(r"([A-Za-z0-9_]{3,16})", message)
    return match.group(1) if match else None


def log_success(nickname: str, resp: str):
    line = f"[{datetime.now()}] ✅ {nickname} → {resp}\n"
    with open(SUCCESS_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def log_error(nickname: str, error: str):
    line = f"[{datetime.now()}] ❌ {nickname} → {error}\n"
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(line)
