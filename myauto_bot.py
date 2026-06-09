import requests
import json
import time
import os
from datetime import datetime

# ===== შენი მონაცემები =====
TELEGRAM_TOKEN = "8911039466:AAH1QQfAtBolwTRamovsK_D5DM1ngpEE98s"
CHAT_ID = "5885495534"

# ===== ძიების პარამეტრები =====
MANUFACTURER_ID = 45   # Subaru
MODEL_ID = 1091        # Crosstrek
YEAR_FROM = 2013
YEAR_TO = 2017

# ===== ფაილი სადაც ვინახავთ ნანახ განცხადებებს =====
SEEN_FILE = "seen_cars.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ka-GE,ka;q=0.9,en;q=0.8",
    "Referer": "https://www.myauto.ge/",
    "Origin": "https://www.myauto.ge"
}

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        if r.status_code != 200:
            print(f"Telegram შეცდომა: {r.text}")
    except Exception as e:
        print(f"Telegram შეცდომა: {e}")

def fetch_cars():
    url = "https://api2.myauto.ge/ka/products"
    params = {
        "Mans": f"{MANUFACTURER_ID}.{MODEL_ID}",
        "YearFrom": YEAR_FROM,
        "YearTo": YEAR_TO,
        "Page": 1,
        "SortOrder": 1,  # უახლესი პირველი
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = resp.json()
        return data.get("data", {}).get("items", [])
    except Exception as e:
        print(f"MyAuto შეცდომა: {e}")
        return []

def format_message(car):
    car_id = car.get("car_id", "")
    link = f"https://www.myauto.ge/ka/pr/{car_id}"

    price_usd = car.get("price_usd", 0)
    price_gel = car.get("price", 0)

    if price_usd:
        price_str = f"{int(price_usd):,} $"
    else:
        price_str = f"{int(price_gel):,} ₾"

    year = car.get("prod_year", "—")
    mileage = car.get("car_run_km", 0)
    engine = car.get("engine_volume", "—")

    fuel_types = {1: "⛽ ბენზინი", 2: "🛢 დიზელი", 3: "🔋 ჰიბრიდი", 4: "⚡ ელექტრო", 5: "🔄 გაზი"}
    fuel = fuel_types.get(car.get("fuel_type_id"), "")

    gear_types = {1: "მექანიკა", 2: "ავტომატი", 3: "ტიპტრონიკი", 4: "ვარიატორი"}
    gear = gear_types.get(car.get("gear_type_id"), "")

    msg = f"""🚗 <b>Subaru Crosstrek {year} — ახალი განცხადება!</b>

💰 ფასი: <b>{price_str}</b>
📅 წელი: {year}
🛣 გარბენი: {mileage:,} კმ
🔧 ძრავი: {engine}ლ {fuel}
⚙️ გადაცემათა კოლოფი: {gear}

🔗 <a href="{link}">განცხადების ნახვა →</a>"""
    return msg

def check_new_cars():
    now = datetime.now().strftime('%H:%M:%S')
    print(f"[{now}] შემოწმება დაიწყო...")
    seen = load_seen()
    cars = fetch_cars()

    if not cars:
        print("  → განცხადებები ვერ მოიძებნა (შეცდომა ან ცარიელია)")
        return

    new_count = 0
    for car in cars:
        car_id = str(car.get("car_id", ""))
        if car_id and car_id not in seen:
            seen.add(car_id)
            msg = format_message(car)
            send_telegram(msg)
            new_count += 1
            time.sleep(1)

    save_seen(seen)
    print(f"  → {new_count} ახალი განცხადება გაიგზავნა")
    print(f"  → სულ ნანახი: {len(seen)} განცხადება")

# ===== გაშვება =====
if __name__ == "__main__":
    print("=" * 40)
    print("✅ MyAuto Bot გაშვებულია!")
    print(f"🔍 ეძებს: Subaru Crosstrek {YEAR_FROM}-{YEAR_TO}")
    print(f"⏰ შემოწმება: ყოველ 1 საათში")
    print("=" * 40 + "\n")

    send_telegram("✅ <b>MyAuto Bot გაშვებულია!</b>\n\n🔍 ვეძებ: Subaru Crosstrek 2013-2017\n⏰ შემოწმება ყოველ საათში\n\nახალი განცხადებების შემთხვევაში გამოგიგზავნი! 🚗")
    check_new_cars()

    while True:
        time.sleep(3600)
        check_new_cars()
