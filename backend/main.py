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

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    comment = data.get("comment", "")
    nickname = extract_nickname(comment)

    if nickname:
        try:
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                resp = mcr.command(f"whitelist add {nickname}")
                log_success(nickname, resp)
        except Exception as e:
            log_error(nickname, str(e))
    else:
        log_error("NO_NICK", f"Комментарий: {comment}")

    return {"status": "ok"}


def extract_nickname(comment: str) -> str | None:
    match = re.search(r"([A-Za-z0-9_]{3,16})", comment)
    return match.group(1) if match else None


def log_success(nickname: str, resp: str):
    line = f"[{datetime.now()}] ✅ {nickname} → {resp}\n"
    with open(SUCCESS_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def log_error(nickname: str, error: str):
    line = f"[{datetime.now()}] ❌ {nickname} → {error}\n"
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(line)
