import requests
from datetime import datetime, timedelta, timezone

# ── Configuration ──────────────────────────────────────────────────────────────
LAT = 55.6050   # Malmö, Sweden
LON = 13.0038
YEAR = 2026
METHOD = 3       # Muslim World League (standard for Europe)
OUTPUT_FILE = "malmo-sweden.ics"
UID_DOMAIN = "deen-routine.malmo"   # globally-unique UID scope (RFC 5545 §3.8.4.7)

# Apple Calendar / iOS 17+ colour support (X-APPLE-DEFAULT-ALARM extension)
# Standard COLOR property per RFC 7986 §5.9 – values are CSS colour names
COLORS = {
    "PRAYER":    "teal",
    "WORSHIP":   "blue",
    "FAMILY":    "orange",
    "EDUCATION": "purple",
    "HEALTH":    "red",
}

# Single UTC stamp for the whole generation run (RFC 5545 §3.8.7.2)
NOW_UTC = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# ── Timezone definition (Europe/Stockholm – CET/CEST) ─────────────────────────
VTIMEZONE = """\
BEGIN:VTIMEZONE
TZID:Europe/Stockholm
X-LIC-LOCATION:Europe/Stockholm
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10
END:STANDARD
END:VTIMEZONE"""

# ── Per-event content (summary, description, category, priority, alarms) ──────
#   alarms: list of (trigger_minutes_offset, notification_text)
#   trigger  0 = fires exactly at event start
#   trigger -5 = fires 5 minutes before event start
CONTENT = {
    "fajr": dict(
        summary="Fajr Prayer",
        category="PRAYER",
        priority=1,
        description=(
            "الصَّلَاةُ خَيْرٌ مِنَ النَّوْم\n"
            "Prayer is better than sleep.\n\n"
            "2 Rak'ah Sunnah + 2 Rak'ah Fard\n\n"
            "After Salah:\n"
            "SubhanAllah x33 | Alhamdulillah x33 | Allahu Akbar x34\n"
            "Ayat Al-Kursi"
        ),
        alarms=[
            (-5, "Fajr in 5 minutes - make wudu now"),
            (0,  "FAJR TIME - Allahu Akbar! Rise and pray."),
        ],
    ),
    "adhkar-am": dict(
        summary="Azkar Sabah",
        category="WORSHIP",
        priority=2,
        description=(
            "Morning Remembrance - azkar al-sabah\n\n"
            "Ayat Al-Kursi\n"
            "Al-Ikhlas, Al-Falaq, An-Nas x3\n"
            "Sayyid Al-Istighfar\n"
            "Hasbiyallahu la ilaha illa hu x7\n"
            "A'udhu bi kalimatillahi at-tammati min sharri ma khalaq x3"
        ),
        alarms=[
            (0, "Azkar Sabah - start your morning remembrance now"),
        ],
    ),
    "quran-am": dict(
        summary="Surah Al-Baqara",
        category="WORSHIP",
        priority=2,
        description=(
            "Daily Quran portion before Sunrise\n\n"
            "وَرَتِّلِ الْقُرْآنَ تَرْتِيلًا\n"
            "Recite the Quran with measured recitation. (73:4)\n\n"
            "Focus on tajweed. Reflect on the meaning."
        ),
        alarms=[
            (0, "Quran time - recite your portion before Sunrise"),
        ],
    ),
    "school-drop": dict(
        summary="School Drop-off",
        category="FAMILY",
        priority=5,
        description=(
            "Drop your son at school.\n\n"
            "Du'a for leaving home:\n"
            "Bismillah, tawakkaltu 'ala Allah,\n"
            "wa la hawla wa la quwwata illa billah."
        ),
        alarms=[
            (0, "School Drop-off - time to go"),
        ],
    ),
    "dhuhr": dict(
        summary="Dhuhr Prayer",
        category="PRAYER",
        priority=1,
        description=(
            "وَأَقِمِ الصَّلَاةَ لِذِكْرِي\n"
            "Establish prayer for My remembrance. (20:14)\n\n"
            "4 Rak'ah Sunnah + 4 Rak'ah Fard + 2 Rak'ah Sunnah\n\n"
            "After Salah:\n"
            "SubhanAllah x33 | Alhamdulillah x33 | Allahu Akbar x34"
        ),
        alarms=[
            (-5, "Dhuhr in 5 minutes - prepare for prayer"),
            (0,  "DHUHR TIME - Allahu Akbar!"),
        ],
    ),
    "school-pick": dict(
        summary="School Pickup",
        category="FAMILY",
        priority=5,
        description=(
            "Pick up your son from school.\n\n"
            "Du'a for entering the home:\n"
            "Allahumma inni as'aluka khayr al-mawlaj wa khayr al-makhraj."
        ),
        alarms=[
            (0, "School Pickup - time to collect your son"),
        ],
    ),
    "kids-dars": dict(
        summary="Kids Dars",
        category="EDUCATION",
        priority=3,
        description=(
            "Islamic lesson with the children - 1 hour\n\n"
            "Rotation topics:\n"
            "- Seerah of the Prophet (peace be upon him)\n"
            "- Aqeedah basics\n"
            "- Fiqh for children\n"
            "- Quran memorisation review\n"
            "- Stories of the Sahabah (may Allah be pleased with them)"
        ),
        alarms=[
            (-5, "Kids Dars in 5 minutes - prepare your materials"),
            (0,  "Kids Dars - Islamic lesson time! Bismillah."),
        ],
    ),
    "asr": dict(
        summary="Asr Prayer",
        category="PRAYER",
        priority=1,
        description=(
            "حَافِظُوا عَلَى الصَّلَوَاتِ وَالصَّلَاةِ الْوُسْطَى\n"
            "Guard strictly the prayers and the middle prayer. (2:238)\n\n"
            "4 Rak'ah Fard\n\n"
            "After Salah:\n"
            "SubhanAllah x33 | Alhamdulillah x33 | Allahu Akbar x34"
        ),
        alarms=[
            (-5, "Asr in 5 minutes - prepare for prayer"),
            (0,  "ASR TIME - Allahu Akbar!"),
        ],
    ),
    "quran-pm": dict(
        summary="Quran Reading",
        category="WORSHIP",
        priority=2,
        description=(
            "Post-Asr Quran session - 25 minutes\n\n"
            "Those who recite the Book of Allah and establish prayer\n"
            "and spend from what We have provided for them...\n"
            "they hope for a transaction that will never perish. (35:29)\n\n"
            "Stay consistent - a little every day."
        ),
        alarms=[
            (0, "Post-Asr Quran - 25 minutes of focused recitation"),
        ],
    ),
    "family": dict(
        summary="Family Time",
        category="FAMILY",
        priority=3,
        description=(
            "خَيْرُكُمْ خَيْرُكُمْ لِأَهْلِهِ\n"
            "The best of you are those who are best to their families.\n"
            "- Prophet Muhammad (peace be upon him)\n\n"
            "Ideas:\n"
            "- Quran recitation together\n"
            "- Islamic stories for the kids\n"
            "- Walk outdoors\n"
            "- Dinner and conversation"
        ),
        alarms=[
            (-5, "Family Time in 5 minutes - put the phone down"),
            (0,  "Family Time - be fully present with your family"),
        ],
    ),
    "maghrib": dict(
        summary="Maghrib Prayer",
        category="PRAYER",
        priority=1,
        description=(
            "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً\n"
            "Our Lord, give us good in this world and good in the Hereafter. (2:201)\n\n"
            "3 Rak'ah Fard + 2 Rak'ah Sunnah\n\n"
            "After Salah:\n"
            "SubhanAllah x33 | Alhamdulillah x33 | Allahu Akbar x34\n"
            "Ayat Al-Kursi"
        ),
        alarms=[
            (-3, "Maghrib in 3 minutes - prepare for prayer"),
            (0,  "MAGHRIB TIME - Allahu Akbar!"),
        ],
    ),
    "adhkar-pm": dict(
        summary="Azkar Masah",
        category="WORSHIP",
        priority=2,
        description=(
            "Evening Remembrance - azkar al-masa'\n\n"
            "Ayat Al-Kursi\n"
            "Al-Ikhlas, Al-Falaq, An-Nas x3\n"
            "A'udhu bi kalimatillahi at-tammati min sharri ma khalaq x3\n"
            "Istighfar x100\n"
            "Allahumma bika amsayna wa bika asbahna..."
        ),
        alarms=[
            (0, "Azkar Masah - evening remembrance after Maghrib"),
        ],
    ),
    "isha": dict(
        summary="Isha Prayer",
        category="PRAYER",
        priority=1,
        description=(
            "وَمِنَ اللَّيْلِ فَسَبِّحْهُ وَأَدْبَارَ السُّجُودِ\n"
            "Glorify Him in the night and after prostration. (50:40)\n\n"
            "4 Rak'ah Fard + 2 Rak'ah Sunnah + 3 Witr\n\n"
            "After Salah:\n"
            "SubhanAllah x33 | Alhamdulillah x33 | Allahu Akbar x34\n"
            "Ayat Al-Kursi"
        ),
        alarms=[
            (-5, "Isha in 5 minutes - prepare for prayer"),
            (0,  "ISHA TIME - Allahu Akbar!"),
        ],
    ),
    "gym": dict(
        summary="Gym Session",
        category="HEALTH",
        priority=5,
        description=(
            "الْمُؤْمِنُ الْقَوِيُّ خَيْرٌ وَأَحَبُّ إِلَى اللهِ مِنَ الْمُؤْمِنِ الضَّعِيفِ\n"
            "A strong believer is better and more beloved to Allah\n"
            "than a weak believer. - Prophet Muhammad (peace be upon him)\n\n"
            "Niyyah: stay healthy to worship Allah better.\n"
            "Bismillah - let's go!"
        ),
        alarms=[
            (0, "Gym time - a strong believer is better!"),
        ],
    ),
    "jumu'ah": dict(
        summary="Jumu'ah Prayer 🕌",
        category="PRAYER",
        priority=1,
        description=(
            "يَا أَيُّهَا الَّذِينَ آمَنُوا إِذَا نُودِيَ لِلصَّلَاةِ مِن يَوْمِ الْجُمُعَةِ فَاسْعَوْا إِلَىٰ ذِكْرِ اللَّهِ\n"
            "O you who believe! When the call to prayer is made on Friday,\n"
            "hasten to the remembrance of Allah. (62:9)\n\n"
            "• Perform ghusl (ritual bath)\n"
            "• Wear clean clothes & apply perfume\n"
            "• Recite Surah Al-Kahf (18)\n"
            "• Send abundant salawat on the Prophet ﷺ\n"
            "• Arrive early to the masjid\n\n"
            "2 Rak'ah Sunnah before Khutbah + 2 Rak'ah Fard"
        ),
        alarms=[
            (-30, "Jumu'ah in 30 min — perform ghusl and prepare"),
            (-10, "Jumu'ah in 10 minutes — head to the masjid now!"),
            (0,   "JUMU'AH TIME — Allahu Akbar! Hasten to the prayer."),
        ],
    ),
}


# ── ICS helpers ────────────────────────────────────────────────────────────────

def to_dt(date_str, time_str):
    clean = time_str.split(" ")[0]
    return datetime.strptime(f"{date_str} {clean}", "%d-%m-%Y %H:%M")


def fmt(dt):
    return dt.strftime("%Y%m%dT%H%M%S")


def add_min(dt, m):
    return dt + timedelta(minutes=m)


def ics_escape(value):
    """Escape special characters per RFC 5545 §3.3.11."""
    return (
        value
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold_line(line):
    """RFC 5545 §3.1 – fold long lines at 75 octets, continuation with CRLF + space."""
    parts = []
    while len(line.encode("utf-8")) > 75:
        i = 75
        while len(line[:i].encode("utf-8")) > 75:
            i -= 1
        parts.append(line[:i])
        line = " " + line[i:]
    parts.append(line)
    return "\r\n".join(parts)


def valarm_block(trigger_mins, message):
    """Build a VALARM component that fires a popup notification."""
    if trigger_mins < 0:
        trigger = f"-PT{abs(trigger_mins)}M"
    elif trigger_mins == 0:
        trigger = "PT0S"
    else:
        trigger = f"PT{trigger_mins}M"
    return "\r\n".join([
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"TRIGGER:{trigger}",
        fold_line(f"DESCRIPTION:{ics_escape(message)}"),
        "END:VALARM",
    ])


def build_event(uid, key, start, end):
    """Build a complete VEVENT block with description and VALARM notifications."""
    c = CONTENT[key]
    lines = [
        "BEGIN:VEVENT",
        # UID must be globally unique – scoped to our domain (RFC 5545 §3.8.4.7)
        fold_line(f"UID:{uid}@{UID_DOMAIN}"),
        # DTSTAMP = UTC time this entry was generated, NOT the event time (RFC 5545 §3.8.7.2)
        f"DTSTAMP:{NOW_UTC}",
        fold_line(f"SUMMARY:{ics_escape(c['summary'])}"),
        f"DTSTART;TZID=Europe/Stockholm:{fmt(start)}",
        f"DTEND;TZID=Europe/Stockholm:{fmt(end)}",
        f"CATEGORIES:{c['category']}",
        f"PRIORITY:{c['priority']}",
        f"COLOR:{COLORS.get(c['category'], 'teal')}",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        fold_line(f"DESCRIPTION:{ics_escape(c['description'])}"),
    ]
    for trigger_mins, message in c["alarms"]:
        lines.append(valarm_block(trigger_mins, message))
    lines.append("END:VEVENT")
    return "\r\n".join(lines)  # RFC 5545 §3.1 mandates CRLF line endings


# ── Calendar generation ────────────────────────────────────────────────────────

parts = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Daily Deen Routine - Malmo//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Daily Deen Routine",
    "X-WR-TIMEZONE:Europe/Stockholm",
    VTIMEZONE,
]

for month in range(1, 13):   # January – December 2026 (full year)
    url = (
        f"https://api.aladhan.com/v1/calendar/{YEAR}/{month}"
        f"?latitude={LAT}&longitude={LON}&method={METHOD}"
    )
    data = requests.get(url).json()["data"]

    for d in data:
        date_str = d["date"]["gregorian"]["date"]
        t = d["timings"]

        fajr    = to_dt(date_str, t["Fajr"])
        dhuhr   = to_dt(date_str, t["Dhuhr"])
        asr     = to_dt(date_str, t["Asr"])
        maghrib = to_dt(date_str, t["Maghrib"])
        isha    = to_dt(date_str, t["Isha"])

        base_date = datetime.strptime(date_str, "%d-%m-%Y")
        day_id    = date_str.replace("-", "")
        weekday   = base_date.weekday()   # 0=Mon … 6=Sun

        # ── Fajr block ────────────────────────────────────────────────────────
        fajr_end = add_min(fajr, 25)
        parts.append(build_event(f"{day_id}-fajr", "fajr", fajr, fajr_end))

        adhkar_am_end = add_min(fajr_end, 20)
        parts.append(build_event(f"{day_id}-adhkar-am", "adhkar-am", fajr_end, adhkar_am_end))

        quran_am_end = add_min(adhkar_am_end, 20)
        parts.append(build_event(f"{day_id}-quran-am", "quran-am", adhkar_am_end, quran_am_end))

        # ── School drop (daily 08:00) ─────────────────────────────────────────
        school_drop = base_date.replace(hour=8, minute=0)
        parts.append(build_event(f"{day_id}-school-drop", "school-drop", school_drop, add_min(school_drop, 10)))

        # ── Dhuhr (or Jumu'ah on Friday) ─────────────────────────────────────
        dhuhr_end = add_min(dhuhr, 20)
        if weekday == 4:   # Friday → Jumu'ah replaces Dhuhr
            parts.append(build_event(f"{day_id}-jumuah", "jumu'ah", dhuhr, dhuhr_end))
        else:
            parts.append(build_event(f"{day_id}-dhuhr", "dhuhr", dhuhr, dhuhr_end))

        # ── School pickup (daily 14:00) ───────────────────────────────────────
        school_pick = base_date.replace(hour=14, minute=0)
        parts.append(build_event(f"{day_id}-school-pick", "school-pick", school_pick, add_min(school_pick, 10)))

        # ── Kids Dars (Tuesday & Thursday 15:00–16:00) ───────────────────────
        if weekday in (1, 3):
            kids_dars = base_date.replace(hour=15, minute=0)
            parts.append(build_event(f"{day_id}-kids-dars", "kids-dars", kids_dars, add_min(kids_dars, 60)))

        # ── Asr ───────────────────────────────────────────────────────────────
        asr_end = add_min(asr, 20)
        parts.append(build_event(f"{day_id}-asr", "asr", asr, asr_end))

        # ── Post-Asr Quran (25 min) ───────────────────────────────────────────
        quran_pm_end = add_min(asr_end, 25)
        parts.append(build_event(f"{day_id}-quran-pm", "quran-pm", asr_end, quran_pm_end))

        # ── Family time (90 min, capped before Maghrib) ───────────────────────
        family_start = quran_pm_end
        family_end   = add_min(family_start, 90)
        if family_end > maghrib:
            family_end = maghrib
        parts.append(build_event(f"{day_id}-family", "family", family_start, family_end))

        # ── Maghrib ───────────────────────────────────────────────────────────
        maghrib_end = add_min(maghrib, 20)
        parts.append(build_event(f"{day_id}-maghrib", "maghrib", maghrib, maghrib_end))

        # ── Azkar Masah (20 min after Maghrib) ───────────────────────────────
        adhkar_pm_end = add_min(maghrib_end, 20)
        parts.append(build_event(f"{day_id}-adhkar-pm", "adhkar-pm", maghrib_end, adhkar_pm_end))

        # ── Isha ──────────────────────────────────────────────────────────────
        isha_end = add_min(isha, 20)
        parts.append(build_event(f"{day_id}-isha", "isha", isha, isha_end))

        # ── Gym (Friday & Sunday after Isha) ─────────────────────────────────
        if weekday in (4, 6):
            parts.append(build_event(f"{day_id}-gym", "gym", isha_end, add_min(isha_end, 60)))

# ── Islamic holidays 2026 (all-day VEVENT) ────────────────────────────────────
# Dates are approximations based on moon-sighting; actual dates may shift ±1 day.
ISLAMIC_HOLIDAYS = [
    # (YYYYMMDD,  summary,                      description)
    ("20260109", "Islamic New Year 1448 AH 🌙",
     "Ra's al-Sana al-Hijriyya — Islamic New Year.\n"
     "Reflect on the Hijrah of the Prophet ﷺ from Mecca to Medina."),
    ("20260119", "Ashura — 10th Muharram 🤲",
     "The Prophet ﷺ fasted on this day and encouraged fasting on\n"
     "9th & 10th Muharram (or 10th & 11th).\n"
     "Fast today and the day before or after."),
    ("20260319", "Mawlid al-Nabawi ﷺ",
     "Birthday of the Prophet Muhammad ﷺ — 12th Rabi' al-Awwal.\n"
     "Increase salawat: اللهم صل على محمد وعلى آل محمد"),
    ("20260319", "Isra wal Mi'raj 🌙",
     "The Night Journey and Ascension of the Prophet ﷺ.\n"
     "Pray Qiyam al-Layl tonight and reflect on the gift of Salah."),
    ("20260218", "Ramadan Begins 🌙",
     "First day of Ramadan 1447 AH (approx).\n"
     "رمضان مبارك — May Allah accept our fasting, prayers, and deeds.\n\n"
     "• Pray Tarawih every night\n"
     "• Increase Quran recitation\n"
     "• Give sadaqah generously"),
    ("20260319", "Last 10 Nights of Ramadan begin ✨",
     "The last 10 nights of Ramadan — seek Laylat al-Qadr.\n"
     "لَيْلَةُ الْقَدْرِ خَيْرٌ مِّنْ أَلْفِ شَهْرٍ\n"
     "Laylat al-Qadr is better than a thousand months. (97:3)\n\n"
     "Pray Qiyam, make I'tikaf if possible, make abundant du'a."),
    ("20260328", "Laylat al-Qadr (27th Ramadan) ✨",
     "The Night of Power — most likely on the odd nights of the last 10.\n"
     "Pray all night: Allahuma innaka 'afuwwun tuhibbul 'afwa fa'fu 'anni."),
    ("20260319", "Eid al-Fitr 🎉",
     "عيد الفطر المبارك — Eid Mubarak!\n\n"
     "• Perform ghusl, wear best clothes\n"
     "• Eat before Eid prayer (Sunnah)\n"
     "• Pay Zakat al-Fitr before prayer\n"
     "• Attend Eid prayer at the masjid\n"
     "• Visit family and spread joy"),
    ("20260527", "Eid al-Fitr 1447 AH 🎉",
     "عيد الفطر المبارك — Eid Mubarak! (approx date)\n\n"
     "• Perform ghusl, wear best clothes\n"
     "• Eat before Eid prayer (Sunnah)\n"
     "• Pay Zakat al-Fitr before prayer\n"
     "• Attend Eid prayer at the masjid"),
    ("20260809", "Day of Arafah 🤲",
     "9th Dhul Hijjah — the greatest day of the year.\n"
     "Fast today — it expiates sins of the past and coming year.\n"
     "Make abundant du'a, dhikr, and istighfar."),
    ("20260810", "Eid al-Adha 1447 AH 🐑",
     "عيد الأضحى المبارك — Eid al-Adha Mubarak! (approx date)\n\n"
     "• Perform ghusl, wear best clothes\n"
     "• Do NOT eat before Eid prayer\n"
     "• Attend Eid prayer at the masjid\n"
     "• Make Udhiyah (sacrifice) if able\n"
     "• Distribute meat to family, neighbours, and the poor"),
]

for date_str, summary, description in ISLAMIC_HOLIDAYS:
    uid = f"{date_str}-{summary[:12].lower().replace(' ', '-').replace('/', '')}@{UID_DOMAIN}"
    lines = [
        "BEGIN:VEVENT",
        fold_line(f"UID:{uid}"),
        f"DTSTAMP:{NOW_UTC}",
        fold_line(f"SUMMARY:{ics_escape(summary)}"),
        f"DTSTART;VALUE=DATE:{date_str}",
        f"DTEND;VALUE=DATE:{date_str}",
        "CATEGORIES:HOLIDAY",
        "COLOR:red",
        "PRIORITY:1",
        "TRANSP:TRANSPARENT",
        fold_line(f"DESCRIPTION:{ics_escape(description)}"),
        "END:VEVENT",
    ]
    parts.append("\r\n".join(lines))

parts.append("END:VCALENDAR")

# RFC 5545 §3.1: CRLF line endings; newline='' so Python doesn't add extra CR
with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(parts) + "\r\n")

print(f"Generated {OUTPUT_FILE} — full year {YEAR}, 365 days")
