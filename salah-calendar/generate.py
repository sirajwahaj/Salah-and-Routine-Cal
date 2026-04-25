import requests
from datetime import datetime, timedelta

CITY = "Stockholm"
COUNTRY = "Sweden"
YEAR = 2026
OUTPUT_FILE = "stockholm-sweden.ics"

url = f"https://api.aladhan.com/v1/calendarByCity?city={CITY}&country={COUNTRY}&method=2&year={YEAR}"
data = requests.get(url).json()["data"]

def to_dt(date_str, time_str):
    clean_time = time_str.split(" ")[0]
    return datetime.strptime(f"{date_str} {clean_time}", "%d-%m-%Y %H:%M")

def fmt(dt):
    return dt.strftime("%Y%m%dT%H%M%S")

def event(uid, summary, start, end):
    return f"""BEGIN:VEVENT
UID:{uid}
DTSTAMP:{fmt(start)}
SUMMARY:{summary}
DTSTART:{fmt(start)}
DTEND:{fmt(end)}
END:VEVENT
"""

cal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Salah Routine Calendar//EN
CALSCALE:GREGORIAN
"""

for d in data:
    date_str = d["date"]["gregorian"]["date"]
    t = d["timings"]

    fajr = to_dt(date_str, t["Fajr"])
    dhuhr = to_dt(date_str, t["Dhuhr"])
    asr = to_dt(date_str, t["Asr"])
    maghrib = to_dt(date_str, t["Maghrib"])
    isha = to_dt(date_str, t["Isha"])

    def plus(dt, mins):
        return dt + timedelta(minutes=mins)

    day_id = date_str.replace("-", "")

    # Fajr block
    cal += event(f"{day_id}-fajr", "Fajr", fajr, plus(fajr, 10))
    cal += event(f"{day_id}-adhkar-am", "Morning Adhkar", plus(fajr, 10), plus(fajr, 25))
    cal += event(f"{day_id}-quran-am", "Qur’an (Morning)", plus(fajr, 25), plus(fajr, 45))

    # Dhuhr & Asr
    cal += event(f"{day_id}-dhuhr", "Dhuhr", dhuhr, plus(dhuhr, 10))
    cal += event(f"{day_id}-asr", "Asr", asr, plus(asr, 10))

    # Maghrib + family
    cal += event(f"{day_id}-maghrib", "Maghrib", maghrib, plus(maghrib, 10))
    cal += event(f"{day_id}-family", "Family Qur’an Time", plus(maghrib, 10), plus(maghrib, 30))

    # Isha + evening
    cal += event(f"{day_id}-isha", "Isha", isha, plus(isha, 10))
    cal += event(f"{day_id}-adhkar-pm", "Evening Adhkar", plus(isha, 10), plus(isha, 25))

cal += "END:VCALENDAR"

with open(OUTPUT_FILE, "w") as f:
    f.write(cal)

print(f"Generated {OUTPUT_FILE}")
