import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://fruityblox.com/stock"
WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1488285593187385564/aaM4apW-Ac6aI10cRu56vDSaqyCQdKwvONT29rBLSY6pdRqSOYItVuVdRtKuL3Oz8igT")

RARE_FRUITS = [
    "Dragon", "Leopard", "Dough", "Spirit",
    "Venom", "Shadow", "Control",
    "Mammoth", "T-Rex", "Kitsune"
]

last_sent = []

def get_all_fruits():
    res = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    return [h3.text.strip() for h3 in soup.find_all("h3")]

def send_webhook(rare):
    data = {
        "content": "@everyone 🚨 **RARE FRUIT ALERT!**",
        "embeds": [{
            "title": "Rare fruits in stock",
            "description": "\n".join(f"• {r}" for r in rare),
            "color": 16711680
        }]
    }
    requests.post(WEBHOOK_URL, json=data)

while True:
    try:
        fruits = get_all_fruits()
        rare = [f for f in fruits if f in RARE_FRUITS]

        if rare and rare != last_sent:
            send_webhook(rare)
            last_sent = rare
            print("Sent:", rare)
        else:
            print("No rare fruit")

    except Exception as e:
        print(e)

    time.sleep(60)
