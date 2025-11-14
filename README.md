<<<<<<< HEAD
☀️ SO-Flare-Community
=======
# ☀️ **SO-Flare-Community**
### *Solar Flare Recorder — Automatic SDR Radio Spectrogram Logger*

**SO-Flare-Community** is a Python-based automation tool for recording **solar radio emissions** using a Software Defined Radio (SDR).  
It automatically calculates **sunrise and sunset** based on your location and records only while the Sun is above the horizon — perfect for detecting **solar flares** and other solar radio bursts.

---

## 🛰️ **Key Features**
- 📡 Automatic spectrum recording via `soapypower` (25–200 MHz range)
- 🕑 Calculates sunrise and sunset using [Astral](https://pypi.org/project/astral/)
- 🌇 Records only during daylight hours (configurable ± offsets)
- 🧭 Easy configuration via `.env` file
- 🧾 Timestamped CSV output (`flare_YYYY-MM-DD_HH-MM.csv`)
- 💤 Sleeps at night to save resources
- ✅ Compatible with **Linux (Ubuntu Server)** and **Windows**

---

## ⚙️ **Requirements**
- Python **3.8+**
- Python dependencies:
  - `astral`
  - `pytz`
  - `python-dotenv`
- SDR software stack:
  - `soapypower` (part of SoapySDR)
  - Compatible SDR receiver (RTL-SDR, SDRplay, AirSpy, etc.)

---

## 🧰 **Installation**
```bash
git clone https://github.com/<your-username>/SO-Flare-Community.git
cd SO-Flare-Community
```

(Optional) create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🗺️ **Configuration (.env)**
Create a `.env` file in the project root (you can copy from `.env.example`):

```bash
LAT=40.6005
LON=12.4550
ELEV=15
TIMEZONE=Europe/Rome
OUTPUT_DIR=/home/user/
```

| Variable | Description | Example |
|-----------|-------------|----------|
| `LAT` | Latitude (decimal degrees) | 44.6669 |
| `LON` | Longitude (decimal degrees) | 10.4779 |
| `ELEV` | Elevation above sea level (m) | 121 |
| `TIMEZONE` | IANA timezone name | Europe/Rome |
| `OUTPUT_DIR` | Folder to save CSV files | `/home/user/data` |

> 💡 Example output file: `flare_2025-11-12_09-00.csv`

---

## 🚀 **Running the Recorder**
Run manually:
```bash
python3 main.py
```

- If the Sun **is above the horizon** → starts a **1-hour recording**
- If it’s **nighttime** → waits for 1 hour and rechecks

---

## 🔁 **Continuous Operation (Linux)**
You can run it 24/7 using a simple loop script:

```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGFILE="$SCRIPT_DIR/sfc_scheduler.log"

while true; do
    python3 "$SCRIPT_DIR/main.py" >> "$LOGFILE" 2>&1
done
```

Make it executable:
```bash
chmod +x scheduler.sh
```

Optionally, set it up as a **systemd service** for full automation.

---

## 📂 **Project Structure**
```
SO-Flare-Community/
├── main.py              # Main program
├── .env.example         # Example configuration
├── requirements.txt     # Python dependencies
├── scheduler.sh         # Optional continuous runner
├── .gitignore
└── README.md
```

---

## 🧩 **Example Output**
```
🌅 Sunrise: 07:14 | 🌇 Sunset: 16:51
🕓 Now: 10:00 | Recording window: 06:14 → 17:51
☀️  The Sun is above the horizon... Recording started → /home/user/flare_2025-11-12_10-00.csv
✅ Recording finished successfully.
```

---

## 💡 **Tips**
- Expand frequency range (`-f 20M:500M`) or resolution in `soapypower`
- Monitor disk space — CSV files can grow large
- Compare data with [e-CALLISTO](https://www.e-callisto.org/) to confirm real solar bursts

---

## 🧾 **License**
Released under the **MIT License** — free to use, modify, and distribute with attribution.

---

## 🙌 **Author**
**SO-Flare-Community**  
Open-source solar radio observation project using SDR technology.
>>>>>>> 4693d3e863c9b357f205d11c919ec69a6bbdfb8e
