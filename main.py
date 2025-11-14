from astral.sun import sun
from astral import Observer
from datetime import datetime, timedelta
from time import sleep
import pytz
import os
from dotenv import load_dotenv
import SoapySDR
from SoapySDR import *
import numpy as np
import csv
import time

# --------------------------
# Load configuration (.env)
# --------------------------
load_dotenv()

lat = float(os.getenv("LAT"))
lon = float(os.getenv("LON"))
elev = float(os.getenv("ELEV"))
output_dir = os.getenv("OUTPUT_DIR", ".")

tz = pytz.timezone(os.getenv("TIMEZONE"))
now = datetime.now(tz)

obs = Observer(latitude=lat, longitude=lon, elevation=elev)
s = sun(obs, date=now.date(), tzinfo=tz)

start_recording = s["sunrise"] - timedelta(hours=1)
stop_recording  = s["sunset"]  + timedelta(hours=1)

print(f"🌅 Sunrise: {s['sunrise'].strftime('%H:%M')} | 🌇 Sunset: {s['sunset'].strftime('%H:%M')}")
print(f"🕓 Now: {now.strftime('%H:%M')} | Recording window: {start_recording.strftime('%H:%M')} → {stop_recording.strftime('%H:%M')}")


# --------------------------
# Scanner settings
# --------------------------
F_START     = 25e6
F_STOP      = 200e6
STEP        = 1e6
SAMPLE_RATE = 2.0e6
GAIN        = 40
DWELL       = 0.40
BUFF_SIZE   = 4096


def scan_and_save(output_file):
    print("📡 Opening SDR device…")
    sdr = SoapySDR.Device(dict(driver="sdrplay"))

    sdr.setSampleRate(SOAPY_SDR_RX, 0, SAMPLE_RATE)
    sdr.setGain(SOAPY_SDR_RX, 0, GAIN)

    rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
    sdr.activateStream(rxStream)

    buff = np.zeros(BUFF_SIZE, dtype=np.complex64)

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["freq_hz", "power_dbm"])

        freq = F_START
        while freq <= F_STOP:
            sdr.setFrequency(SOAPY_SDR_RX, 0, freq)
            time.sleep(DWELL)

            sr = sdr.readStream(rxStream, [buff], BUFF_SIZE)

            if sr.ret > 0:
                power = 10 * np.log10(np.mean(np.abs(buff)**2) + 1e-12)
            else:
                # retry once
                time.sleep(0.2)
                sr = sdr.readStream(rxStream, [buff], BUFF_SIZE)
                if sr.ret > 0:
                    power = 10 * np.log10(np.mean(np.abs(buff)**2) + 1e-12)
                else:
                    power = -200

            writer.writerow([freq, power])
            print(f"{freq/1e6:.1f} MHz -> {power:.1f} dB")

            freq += STEP

    sdr.deactivateStream(rxStream)
    sdr.closeStream(rxStream)
    print("📁 Scan complete:", output_file)



# --------------------------
# Sunrise / Sunset logic
# --------------------------
if start_recording <= now <= stop_recording:

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_file = os.path.join(output_dir, f"flare_{timestamp}.csv")

    print(f"☀️  Sun above horizon → starting recording → {output_file}")
    scan_and_save(output_file)
    print("✅ Recording finished.")
else:
    print("🌙 The Sun is below the horizon. Sleeping for 1 hour…")
    sleep(3600)
