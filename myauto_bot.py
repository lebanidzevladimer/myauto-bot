import requests, json, os, time
from datetime import datetime

TELEGRAM_TOKEN = "8911039466:AAH1QQfAtBolwTRamovsK_D5DM1ngpEE98s"
CHAT_ID = "5885495534"
SEEN_FILE = "seen_cars.json"

SEARCHES = [
    {
        "name": "Subaru Crosstrek",
        "mans": "45.1091",
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
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.myauto.ge/",
    "Origin": "https://www.myauto.ge"
}

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f: return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f: json.dump(list(seen), f)

def send_telegram(msg):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)

def fetch_cars(search):
    params = {"Mans": search["mans"], "YearFrom": search["year_from"],
              "YearTo": search["year_to"], "Page": 1, "SortOrder": 1}
    try:
        r = requests.get("https://api2.myauto.ge/ka/products",
                         params=params, headers=HEADERS, timeout=15)
        items = r.json().get("data", {}).get("items", [])
        if search["max_price"]:
            items = [i for i in items if (i.get("price_usd") or 0) <= search["max_price"]]
        if search["max_mileage"]:
            items = [i for i in items if (i.get("car_run_km") or 0) <= search["max_mileage"]]
        return items
    except: return []

def format_msg(car, search_name):
    cid = car.get("car_id", "")
    price = car.get("price_usd") or car.get("price", 0)
    cur = "$" if car.get("price_usd") else "₾"
    fuel = {1:"⛽ ბენზინი",2:"🛢 დიზელი",3:"🔋 ჰიბრიდი",4:"⚡ ელექტრო"}.get(car.get("fuel_type_id"),"")
    gear = {1:"მექანიკა",2:"ავტომატი",3:"ტიპტრონიკი",4:"ვარიატორი"}.get(car.get("gear_type_id"),"")
    return f"""🚗 <b>{search_name} {car.get('prod_year')} — ახალი!</b>

💰 {int(price):,} {cur}
🛣 {car.get('car_run_km',0):,} კმ
🔧 {car.get('engine_volume','')}ლ {fuel} | {gear}

🔗 <a href="https://www.myauto.ge/ka/pr/{cid}">ნახვა →</a>"""

def run():
    seen = load_seen()
    timers = {s["name"]: 0 for s in SEARCHES}
    print("✅ MyAuto Bot გაშვებულია!")
    while True:
        now = time.time()
        for s in SEARCHES:
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
