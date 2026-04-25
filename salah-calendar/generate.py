import requests
from datetime import datetime, timedelta

CITY = "Stockholm"
COUNTRY = "Sweden"
YEAR = 2026
OUTPUT_FILE = "stockholm-routine.ics"

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

def add_minutes(dt, mins):
    return dt + timedelta(minutes=mins)

cal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Daily Deen Routine//EN
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

    base_date = datetime.strptime(date_str, "%d-%m-%Y")

    day_id = date_str.replace("-", "")

    # --- FAJR BLOCK ---
    fajr_end = add_minutes(fajr, 20)
    cal += event(f"{day_id}-fajr", "Fajr Prayer", fajr, fajr_end)

    adhkar_am_end = add_minutes(fajr_end, 15)
    cal += event(f"{day_id}-adhkar-am", "Morning Dhikr", fajr_end, adhkar_am_end)

    quran_am_end = add_minutes(adhkar_am_end, 20)
    cal += event(f"{day_id}-quran-am", "Quran Study", adhkar_am_end, quran_am_end)

    # --- SCHOOL DROP ---
    school_drop = base_date.replace(hour=8, minute=0)
    cal += event(f"{day_id}-school-drop", "School Drop", school_drop, add_minutes(school_drop, 10))

    # --- DHUHR ---
    dhuhr_end = add_minutes(dhuhr, 25)
    cal += event(f"{day_id}-dhuhr", "Dhuhr Prayer", dhuhr, dhuhr_end)

    # --- SCHOOL PICKUP ---
    school_pick = base_date.replace(hour=14, minute=0)
    cal += event(f"{day_id}-school-pick", "School Pickup", school_pick, add_minutes(school_pick, 10))

    # --- ASR ---
    asr_end = add_minutes(asr, 20)
    cal += event(f"{day_id}-asr", "Asr Prayer", asr, asr_end)

    # --- FAMILY TIME (AFTER ASR → BEFORE MAGHRIB) ---
    family_start = asr_end
    family_end = add_minutes(family_start, 90)  # 1.5 hours

    # Make sure it doesn't overlap Maghrib
    if family_end > maghrib:
        family_end = maghrib

    cal += event(f"{day_id}-family", "Family Time", family_start, family_end)

    # --- MAGHRIB ---
    maghrib_end = add_minutes(maghrib, 20)
    cal += event(f"{day_id}-maghrib", "Maghrib Prayer", maghrib, maghrib_end)

    # --- ISHA ---
    isha_end = add_minutes(isha, 20)
    cal += event(f"{day_id}-isha", "Isha Prayer", isha, isha_end)

    # --- EVENING ADHKAR ---
    adhkar_pm_end = add_minutes(isha_end, 15)
    cal += event(f"{day_id}-adhkar-pm", "Evening Dhikr", isha_end, adhkar_pm_end)

cal += "END:VCALENDAR"

with open(OUTPUT_FILE, "w") as f:
    f.write(cal)

print(f"Generated {OUTPUT_FILE}")
