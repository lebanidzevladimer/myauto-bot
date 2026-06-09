<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MyAuto Bot</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #22263a;
    --border: #2e3248;
    --accent: #4f6ef7;
    --accent-hover: #3d5ce8;
    --danger: #e74c3c;
    --success: #2ecc71;
    --text: #e8eaf0;
    --text-muted: #7c82a0;
    --text-dim: #4a5070;
  }

  body {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 24px 16px;
  }

  .header {
    text-align: center;
    margin-bottom: 32px;
  }

  .header h1 {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }

  .header h1 span { color: var(--accent); }

  .header p {
    color: var(--text-muted);
    margin-top: 6px;
    font-size: 14px;
  }

  .container { max-width: 680px; margin: 0 auto; }

  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
  }

  .card-title {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 16px;
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
  }

  .form-row.three { grid-template-columns: 1fr 1fr 1fr; }
  .form-row.full { grid-template-columns: 1fr; }

  label {
    font-size: 12px;
    color: var(--text-muted);
    display: block;
    margin-bottom: 6px;
    font-weight: 500;
  }

  select, input {
    width: 100%;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-size: 14px;
    padding: 10px 12px;
    font-family: inherit;
    transition: border-color 0.2s;
    outline: none;
    appearance: none;
  }

  select:focus, input:focus { border-color: var(--accent); }

  select option { background: var(--surface2); }

  .btn {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: none;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
    margin-top: 4px;
  }

  .btn-primary {
    background: var(--accent);
    color: white;
  }

  .btn-primary:hover { background: var(--accent-hover); }

  .btn-danger {
    background: transparent;
    color: var(--danger);
    border: 1px solid var(--danger);
    padding: 6px 12px;
    width: auto;
    font-size: 12px;
    border-radius: 8px;
    margin-top: 0;
  }

  .btn-danger:hover { background: rgba(231,76,60,0.1); }

  .cars-list { display: flex; flex-direction: column; gap: 10px; }

  .car-item {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .car-info { flex: 1; }

  .car-name {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
  }

  .car-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 6px;
  }

  .tag {
    font-size: 11px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 3px 8px;
    border-radius: 20px;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--success);
    flex-shrink: 0;
    box-shadow: 0 0 6px var(--success);
  }

  .empty-state {
    text-align: center;
    padding: 32px;
    color: var(--text-dim);
    font-size: 14px;
  }

  .copy-section { margin-top: 8px; }

  .code-block {
    background: #0a0c14;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #a8b4ff;
    white-space: pre;
    overflow-x: auto;
    line-height: 1.7;
    margin-top: 12px;
  }

  .copy-btn {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 12px;
    cursor: pointer;
    font-family: inherit;
    float: right;
    transition: all 0.2s;
  }

  .copy-btn:hover { color: var(--text); border-color: var(--accent); }

  .notice {
    background: rgba(79, 110, 247, 0.08);
    border: 1px solid rgba(79, 110, 247, 0.2);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #8fa4ff;
    margin-top: 12px;
    line-height: 1.5;
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>MyAuto <span>Bot</span> Manager</h1>
    <p>მართე შენი ბოტის საძიებო პარამეტრები</p>
  </div>

  <!-- Add Car Form -->
  <div class="card">
    <div class="card-title">+ ახალი მანქანის დამატება</div>

    <div class="form-row">
      <div>
        <label>მარკა</label>
        <select id="make">
          <option value="">აირჩიე...</option>
          <option value="45.0">Subaru</option>
          <option value="55.0">Kia</option>
          <option value="48.0">Hyundai</option>
          <option value="1.0">Toyota</option>
          <option value="2.0">BMW</option>
          <option value="3.0">Mercedes-Benz</option>
          <option value="4.0">Audi</option>
          <option value="5.0">Honda</option>
          <option value="6.0">Ford</option>
          <option value="7.0">Chevrolet</option>
          <option value="8.0">Nissan</option>
          <option value="9.0">Mazda</option>
          <option value="10.0">Volkswagen</option>
          <option value="11.0">Lexus</option>
          <option value="12.0">Mitsubishi</option>
        </select>
      </div>
      <div>
        <label>მოდელი</label>
        <select id="model">
          <option value="">ჯერ მარკა აირჩიე</option>
        </select>
      </div>
    </div>

    <div class="form-row three">
      <div>
        <label>წელი (დან)</label>
        <select id="yearFrom"></select>
      </div>
      <div>
        <label>წელი (მდე)</label>
        <select id="yearTo"></select>
      </div>
      <div>
        <label>შემოწმება</label>
        <select id="interval">
          <option value="1800">30 წუთში</option>
          <option value="3600" selected>1 საათში</option>
          <option value="7200">2 საათში</option>
          <option value="21600">6 საათში</option>
        </select>
      </div>
    </div>

    <div class="form-row">
      <div>
        <label>მაქს. ფასი ($) — არასავალდებულო</label>
        <input type="number" id="maxPrice" placeholder="მაგ: 15000">
      </div>
      <div>
        <label>მაქს. გარბენი (კმ) — არასავალდებულო</label>
        <input type="number" id="maxMileage" placeholder="მაგ: 150000">
      </div>
    </div>

    <button class="btn btn-primary" onclick="addCar()">+ დამატება</button>
  </div>

  <!-- Cars List -->
  <div class="card">
    <div class="card-title">აქტიური ძიებები</div>
    <div class="cars-list" id="carsList">
      <div class="empty-state">ჯერ მანქანა არ დამატებულა</div>
    </div>
  </div>

  <!-- Generated Code -->
  <div class="card">
    <div class="card-title">მზა კოდი — GitHub-ზე ატვირთე</div>
    <div class="copy-section">
      <button class="copy-btn" onclick="copyCode()">📋 კოპირება</button>
      <div class="code-block" id="codeBlock">← მარცხნივ მანქანა დაამატე და კოდი გამოჩნდება</div>
    </div>
    <div class="notice">
      📌 კოდი რომ განახლდება — GitHub-ზე <strong>myauto_bot.py</strong> ფაილი ჩაანაცვლე ახლით. Railway ავტომატურად გადაიტვირთება!
    </div>
  </div>
</div>

<script>
const MODELS = {
  "45.0": [["1091","Crosstrek"],["1092","Forester"],["1093","Impreza"],["1094","Outback"],["1095","XV"]],
  "55.0": [["2001","Niro"],["2002","Sportage"],["2003","Sorento"],["2004","Stinger"],["2005","Seltos"]],
  "48.0": [["3001","Kona"],["3002","Tucson"],["3003","Santa Fe"],["3004","Ioniq"],["3005","i30"]],
  "1.0":  [["4001","Corolla"],["4002","Camry"],["4003","RAV4"],["4004","Prius"],["4005","Land Cruiser"]],
  "2.0":  [["5001","3 Series"],["5002","5 Series"],["5003","X5"],["5004","X3"],["5005","7 Series"]],
  "3.0":  [["6001","C-Class"],["6002","E-Class"],["6003","GLC"],["6004","S-Class"],["6005","A-Class"]],
  "4.0":  [["7001","A4"],["7002","A6"],["7003","Q5"],["7004","Q7"],["7005","A3"]],
  "5.0":  [["8001","Civic"],["8002","Accord"],["8003","CR-V"],["8004","HR-V"],["8005","Pilot"]],
  "6.0":  [["9001","Focus"],["9002","Fiesta"],["9003","Escape"],["9004","Explorer"],["9005","Mustang"]],
  "7.0":  [["10001","Cruze"],["10002","Malibu"],["10003","Equinox"],["10004","Traverse"],["10005","Camaro"]],
  "8.0":  [["11001","Qashqai"],["11002","X-Trail"],["11003","Juke"],["11004","Micra"],["11005","Leaf"]],
  "9.0":  [["12001","CX-5"],["12002","CX-3"],["12003","Mazda3"],["12004","Mazda6"],["12005","MX-5"]],
  "10.0": [["13001","Golf"],["13002","Passat"],["13003","Tiguan"],["13004","Polo"],["13005","Touareg"]],
  "11.0": [["14001","RX"],["14002","NX"],["14003","ES"],["14004","IS"],["14005","GX"]],
  "12.0": [["15001","Outlander"],["15002","Eclipse Cross"],["15003","ASX"],["15004","Pajero"],["15005","L200"]],
};

const MAKE_NAMES = {
  "45.0":"Subaru","55.0":"Kia","48.0":"Hyundai","1.0":"Toyota","2.0":"BMW",
  "3.0":"Mercedes-Benz","4.0":"Audi","5.0":"Honda","6.0":"Ford","7.0":"Chevrolet",
  "8.0":"Nissan","9.0":"Mazda","10.0":"Volkswagen","11.0":"Lexus","12.0":"Mitsubishi"
};

const INTERVAL_NAMES = {"1800":"30 წუთში","3600":"1 საათში","7200":"2 საათში","21600":"6 საათში"};

let cars = JSON.parse(localStorage.getItem('myauto_cars') || '[]');

// Init years
const yearFrom = document.getElementById('yearFrom');
const yearTo = document.getElementById('yearTo');
for (let y = 2024; y >= 1990; y--) {
  yearFrom.innerHTML += `<option value="${y}" ${y==2013?'selected':''}>${y}</option>`;
  yearTo.innerHTML += `<option value="${y}" ${y==2017?'selected':''}>${y}</option>`;
}

document.getElementById('make').addEventListener('change', function() {
  const modelSel = document.getElementById('model');
  modelSel.innerHTML = '';
  const models = MODELS[this.value] || [];
  if (!models.length) { modelSel.innerHTML = '<option>მოდელი ვერ მოიძებნა</option>'; return; }
  models.forEach(([id, name]) => modelSel.innerHTML += `<option value="${id}">${name}</option>`);
});

function addCar() {
  const make = document.getElementById('make').value;
  const model = document.getElementById('model').value;
  const modelName = document.getElementById('model').selectedOptions[0]?.text || '';
  const yearF = document.getElementById('yearFrom').value;
  const yearT = document.getElementById('yearTo').value;
  const interval = document.getElementById('interval').value;
  const maxPrice = document.getElementById('maxPrice').value;
  const maxMileage = document.getElementById('maxMileage').value;

  if (!make || !model) { alert('მარკა და მოდელი სავალდებულოა!'); return; }

  const makeId = make.split('.')[0];
  const car = {
    id: Date.now(),
    makeName: MAKE_NAMES[make],
    makeId,
    modelId: model,
    modelName,
    yearFrom: yearF,
    yearTo: yearT,
    interval: parseInt(interval),
    maxPrice: maxPrice || null,
    maxMileage: maxMileage || null,
    mans: `${makeId}.${model}`
  };

  cars.push(car);
  save();
  render();
}

function removeCar(id) {
  cars = cars.filter(c => c.id !== id);
  save();
  render();
}

function save() {
  localStorage.setItem('myauto_cars', JSON.stringify(cars));
}

function render() {
  const list = document.getElementById('carsList');
  if (!cars.length) {
    list.innerHTML = '<div class="empty-state">ჯერ მანქანა არ დამატებულა</div>';
    document.getElementById('codeBlock').textContent = '← მარცხნივ მანქანა დაამატე და კოდი გამოჩნდება';
    return;
  }

  list.innerHTML = cars.map(c => `
    <div class="car-item">
      <div class="status-dot"></div>
      <div class="car-info">
        <div class="car-name">${c.makeName} ${c.modelName}</div>
        <div class="car-tags">
          <span class="tag">📅 ${c.yearFrom}–${c.yearTo}</span>
          <span class="tag">⏰ ${INTERVAL_NAMES[c.interval]}</span>
          ${c.maxPrice ? `<span class="tag">💰 მაქს $${parseInt(c.maxPrice).toLocaleString()}</span>` : ''}
          ${c.maxMileage ? `<span class="tag">🛣 მაქს ${parseInt(c.maxMileage).toLocaleString()} კმ</span>` : ''}
        </div>
      </div>
      <button class="btn btn-danger" onclick="removeCar(${c.id})">წაშლა</button>
    </div>
  `).join('');

  generateCode();
}

function generateCode() {
  const token = "8911039466:AAH1QQfAtBolwTRamovsK_D5DM1ngpEE98s";
  const chatId = "5885495534";

  const searches = cars.map(c => {
    let s = `    {
        "name": "${c.makeName} ${c.modelName}",
        "mans": "${c.mans}",
        "year_from": ${c.yearFrom},
        "year_to": ${c.yearTo},
        "interval": ${c.interval},
        "max_price": ${c.maxPrice || 'None'},
        "max_mileage": ${c.maxMileage || 'None'}
    }`;
    return s;
  }).join(',\n');

  const code = `import requests, json, os, time
from datetime import datetime

TELEGRAM_TOKEN = "${token}"
CHAT_ID = "${chatId}"
SEEN_FILE = "seen_cars.json"

SEARCHES = [
${searches}
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
    run()`;

  document.getElementById('codeBlock').textContent = code;
}

function copyCode() {
  const code = document.getElementById('codeBlock').textContent;
  navigator.clipboard.writeText(code).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = '✅ კოპირებულია!';
    setTimeout(() => btn.textContent = '📋 კოპირება', 2000);
  });
}

// Load initial Subaru Crosstrek
if (!cars.length) {
  cars = [{
    id: Date.now(),
    makeName: 'Subaru', makeId: '45', modelId: '1091', modelName: 'Crosstrek',
    yearFrom: '2013', yearTo: '2017', interval: 3600,
    maxPrice: null, maxMileage: null, mans: '45.1091'
  }];
  save();
}

render();
</script>
</body>
</html>
