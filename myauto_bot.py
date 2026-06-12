import requests, json, os, time, threading
from datetime import datetime, timezone, timedelta

TELEGRAM_TOKEN = "8911039466:AAH1QQfAtBolwTRamovsK_D5DM1ngpEE98s"
CHAT_ID = "5885495534"
GITHUB_TOKEN = "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"
GITHUB_REPO = "lebanidzevladimer/myauto-bot"
SEEN_FILE = "seen_cars.json"
CONFIG_FILE = "searches.json"

DEFAULT_SEARCHES = [
    {
        "name": "Subaru Crosstrek",
        "mans": "39.1925",
        "year_from": 2013,
        "year_to": 2017,
        "interval": 3600,
        "max_price": None,
        "max_mileage": None
    },
    {
        "name": "Kia Niro",
        "mans": "55.1695",
        "year_from": 2018,
        "year_to": 2022,
        "interval": 1800,
        "max_price": None,
        "max_mileage": None
    },
    {
        "name": "BMW 3 Series",
        "mans": "2.18",
        "year_from": 2018,
        "year_to": 2022,
        "interval": 1800,
        "max_price": None,
        "max_mileage": None
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.myauto.ge/",
    "Origin": "https://www.myauto.ge"
}

def load_searches():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return DEFAULT_SEARCHES

def save_searches(searches):
    with open(CONFIG_FILE, "w") as f:
        json.dump(searches, f, ensure_ascii=False, indent=2)

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f: return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f: json.dump(list(seen), f)

def send_telegram(msg, chat_id=None):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": chat_id or CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except Exception as e:
        print(f"Telegram შეცდომა: {e}")

def fetch_cars(search):
    params = {"Mans": search["mans"], "YearFrom": search["year_from"],
              "YearTo": search["year_to"], "Page": 1, "SortOrder": 1}
    try:
        r = requests.get("https://api2.myauto.ge/ka/products",
                         params=params, headers=HEADERS, timeout=15)
        items = r.json().get("data", {}).get("items", [])
        if search.get("max_price"):
            items = [i for i in items if (i.get("price_usd") or 0) <= search["max_price"]]
        if search.get("max_mileage"):
            items = [i for i in items if (i.get("car_run_km") or 0) <= search["max_mileage"]]
        # ბოლო 24 საათის ფილტრი
        cutoff = time.time() - 86400
        filtered = []
        for i in items:
            pv = i.get("photo_ver", 0)
            try:
                if int(pv) >= cutoff:
                    filtered.append(i)
            except:
                filtered.append(i)
        return filtered
    except Exception as e:
        print(f"შეცდომა: {e}")
        return []

def format_msg(car, search_name):
    cid = car.get("car_id", "")
    price = car.get("price_usd") or car.get("price", 0)
    cur = "$" if car.get("price_usd") else "₾"
    fuel = {1:"⛽ ბენზინი",2:"🛢 დიზელი",3:"🔋 ჰიბრიდი",4:"⚡ ელექტრო"}.get(car.get("fuel_type_id"),"")
    gear = {1:"მექანიკა",2:"ავტომატი",3:"ტიპტრონიკი",4:"ვარიატორი"}.get(car.get("gear_type_id"),"")
    pv = car.get("photo_ver", 0)
    try:
        tbilisi = datetime.fromtimestamp(int(pv), tz=timezone.utc) + timedelta(hours=4)
        time_str = tbilisi.strftime("%d.%m.%Y %H:%M")
    except:
        time_str = "—"
    return f"""🚗 <b>{search_name} {car.get('prod_year')} — ახალი განცხადება!</b>

💰 {int(price):,} {cur}
🛣 {car.get('car_run_km',0):,} კმ
🔧 {car.get('engine_volume','')}ლ {fuel} | {gear}
🕐 დამატდა: {time_str}

🔗 <a href="https://www.myauto.ge/ka/pr/{cid}">ნახვა →</a>"""

def get_updates(offset=None):
    params = {"timeout": 30, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
                        params=params, timeout=35)
        return r.json().get("result", [])
    except:
        return []

def handle_command(text, chat_id, searches, seen, timers):
    text = text.strip()

    if text == "/start" or text == "/help":
        msg = """🤖 <b>MyAuto Bot ბრძანებები:</b>

/list — აქტიური ძიებების სია
/status — ბოტის სტატუსი
/restart — ძებნა თავიდან დაიწყება"""
        send_telegram(msg, chat_id)

    elif text == "/list":
        if not searches:
            send_telegram("❌ ძიებები არ არის", chat_id)
            return
        msg = "📋 <b>აქტიური ძიებები:</b>\n\n"
        for i, s in enumerate(searches, 1):
            msg += f"{i}. <b>{s['name']}</b>\n"
            msg += f"   📅 {s['year_from']}–{s['year_to']}\n"
            msg += f"   ⏰ {s['interval']//60} წუთში\n"
            if s.get('max_price'): msg += f"   💰 მაქს ${s['max_price']:,}\n"
            if s.get('max_mileage'): msg += f"   🛣 მაქს {s['max_mileage']:,} კმ\n"
            msg += "\n"
        send_telegram(msg, chat_id)

    elif text == "/status":
        msg = f"✅ <b>ბოტი მუშაობს!</b>\n\n"
        msg += f"🔍 ძიებების რაოდენობა: {len(searches)}\n"
        msg += f"📦 ნანახი განცხადებები: {len(seen)}\n"
        msg += f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        send_telegram(msg, chat_id)

    elif text == "/restart":
        seen.clear()
        save_seen(seen)
        for s in searches:
            timers[s["name"]] = 0
        send_telegram("🔄 ბოტი გადაიტვირთა! ყველა განცხადება ახლიდან შემოწმდება.", chat_id)

def telegram_listener(searches, seen, timers):
    offset = None
    print("📱 Telegram listener გაშვებულია...")
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text", "")
            chat_id = str(msg.get("chat", {}).get("id", ""))
            if text and chat_id == CHAT_ID:
                handle_command(text, chat_id, searches, seen, timers)
        time.sleep(2)

def run():
    searches = load_searches()
    seen = load_seen()
    timers = {s["name"]: 0 for s in searches}

    print("✅ MyAuto Bot გაშვებულია!")
    send_telegram("✅ <b>MyAuto Bot გაშვებულია!</b>\n\nბრძანებები: /list /status /restart")

    # Telegram listener ცალკე thread-ში
    t = threading.Thread(target=telegram_listener, args=(searches, seen, timers), daemon=True)
    t.start()

    while True:
        now = time.time()
        for s in searches:
            if s["name"] not in timers:
                timers[s["name"]] = 0
            if now >= timers[s["name"]]:
                print(f"[{datetime.now().strftime('%H:%M')}] {s['name']} შემოწმება...")
                cars = fetch_cars(s)
                new = 0
                for car in cars:
                    cid = str(car.get("car_id",""))
                    key = f"{s['name']}_{cid}"
                    if cid and key not in seen:
                        seen.add(key)
                        send_telegram(format_msg(car, s["name"]))
                        new += 1
                        time.sleep(1)
                save_seen(seen)
                print(f"  → {new} ახალი")
                timers[s["name"]] = now + s["interval"]
        time.sleep(30)

if __name__ == "__main__":
    run()
