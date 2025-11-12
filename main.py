from astral.sun import sun
from astral import Observer
from datetime import datetime, timedelta
from time import sleep
import pytz
import subprocess
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

SOAPY_CMD = [
    "soapypower",
    "-f", "25M:200M",
    "-B", "2.0M",
    "-i", "10",
    "-e", "2h",
    "-F", "csv",
    "-o", "flare_auto.csv"
]

lat = float(os.getenv("LAT"))
lon = float(os.getenv("LON"))
elev = float(os.getenv("ELEV"))

tz = pytz.timezone(os.getenv("TIMEZONE"))
now = datetime.now(tz)
obs = Observer(latitude=lat, longitude=lon, elevation=elev)

s = sun(obs, date=now.date(), tzinfo=tz)

start_recording = (s["sunrise"] - timedelta(hours=1))
stop_recording = (s["sunset"] + timedelta(hours=1))

print(f"🌅 Sunrise: {s['sunrise'].strftime('%H:%M')} | 🌇 Sunset: {s['sunset'].strftime('%H:%M')}")
print(f"🕓 Now: {now.strftime('%H:%M')} | Recording window: {start_recording.strftime('%H:%M')} → {stop_recording.strftime('%H:%M')}")

if start_recording <= now <= stop_recording:
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

  output_dir = os.getenv("OUTPUT_DIR", ".")
  output_file = os.path.join(output_dir, f"flare_{timestamp}.csv")

  SOAPY_CMD = [
      "soapypower",
      "-f", "25M:200M",
      "-B", "2.0M",
      "-i", "10",
      "-e", "1h",
      "-F", "csv",
      "-o", str(output_file)
  ]

  print(f"☀️  The Sun is above the horizon... Recording started → {output_file}")
  try:
      subprocess.run(SOAPY_CMD, check=True)
      print("✅ Recording finished successfully.")
  except subprocess.CalledProcessError as e:
      print(f"❌ Error during recording: {e}")
else: 
  print("🌙 The Sun is below the horizon.")
  sleep(3600)