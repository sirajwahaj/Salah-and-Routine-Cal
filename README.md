# Daily Deen Routine — Malmö, Sweden

> بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ

A full-year **2026** Islamic daily routine calendar for a Muslim living in **Malmö, Sweden**.  
Compatible with Google Calendar, iPhone, Mac, and any RFC 5545 iCalendar app.

## 🔗 Live calendar (use this URL)

```
https://sirajwahaj.github.io/Salah-and-Routine-Cal/malmo-sweden.ics
```

**Landing page with import buttons →** https://sirajwahaj.github.io/Salah-and-Routine-Cal/

## How to import

### iPhone / Apple Calendar (one tap)
1. Open this on your iPhone: https://sirajwahaj.github.io/Salah-and-Routine-Cal/
2. Tap **"Add to iPhone / Apple Calendar"**
3. Tap **"Add All"** — done ✅

### Google Calendar
1. Go to https://sirajwahaj.github.io/Salah-and-Routine-Cal/
2. Click **"Subscribe in Google Calendar"**
3. Confirm — events appear within minutes ✅

### Manual subscription URL
Copy this URL and paste it into any calendar app's "Subscribe to Calendar" field:
```
https://sirajwahaj.github.io/Salah-and-Routine-Cal/malmo-sweden.ics
```

> **Note:** If you previously used the GitHub blob URL (`github.com/.../blob/...`), it will not work for large files. Use the GitHub Pages URL above instead.

## Enable GitHub Pages (one-time setup)

The calendar is published automatically via GitHub Actions. To activate:
1. Go to **Settings → Pages** in this repository
2. Under **Source**, select **"GitHub Actions"**
3. Save — the workflow will run and publish the site

## Daily schedule

| Event | Duration | When |
|-------|----------|------|
| **Fajr Prayer** | 25 min | At Fajr time — 5-min warning |
| **Azkar Sabah** | 20 min | Immediately after Fajr |
| **Surah Al-Baqara** | 20 min | Before sunrise |
| **School Drop-off** | 10 min | 08:00 daily |
| **Dhuhr Prayer** | 20 min | At Dhuhr time — 5-min warning |
| **School Pickup** | 10 min | 14:00 daily |
| **Kids Dars** | 60 min | Tue & Thu 15:00 |
| **Asr Prayer** | 20 min | At Asr time — 5-min warning |
| **Quran Reading** | 25 min | After Asr |
| **Family Time** | 90 min | After Quran, capped before Maghrib |
| **Maghrib Prayer** | 20 min | At Maghrib time — 3-min warning |
| **Azkar Masah** | 20 min | After Maghrib |
| **Isha Prayer** | 20 min | At Isha time — 5-min warning |
| **Gym Session** | 60 min | Fri & Sun after Isha |

## Prayer times

Calculated for **Malmö, Sweden** (55.6050°N, 13.0038°E) using the **Muslim World League** method — standard for European mosques. Times shift daily throughout the year.

## Regenerate locally

```bash
cd salah-calendar
uv run python generate.py
```

The GitHub Actions workflow also regenerates and publishes automatically on every push to `main`.

## Standards

The `.ics` file is fully **RFC 5545** compliant:
- CRLF line endings
- Lines folded at 75 UTF-8 octets
- Timezone-aware `DTSTART`/`DTEND` (Europe/Stockholm VTIMEZONE block)
- Globally unique UIDs (`event-date@deen-routine.malmo`)
- UTC `DTSTAMP`
- `VALARM` popup notifications on every event
- `CATEGORIES` + `PRIORITY` for calendar app filtering
