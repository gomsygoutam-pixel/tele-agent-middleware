from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Tailscale IP of your local AI agent
LOCAL_AGENT = os.getenv("LOCAL_AGENT")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


@app.get("/")
async def health():
    return {"status": "running"}


@app.post("/telegram/webhook")
async def telegram_webhook(req: Request):

    body = await req.json()

    # Telegram message
    message = body["message"]["text"]

    # Telegram chat ID
    chat_id = body["message"]["chat"]["id"]

    # Send request to local agent over Tailscale
    agent_response = requests.post(
        f"{LOCAL_AGENT}/process",
        json={"query": message},
        timeout=120
    )

    result = agent_response.json()["response"]

    # Send response back to Telegram
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": result
        }
    )

    return {"ok": True}