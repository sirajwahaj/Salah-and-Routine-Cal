# Daily Deen Routine — Malmö, Sweden

A full-year Islamic daily routine calendar for **2026**, built for a Muslim living in **Malmö, Sweden**.  
Compatible with **Google Calendar**, **Apple Calendar (iPhone/Mac)**, and any RFC 5545 iCalendar app.

## What's inside

Each day contains scheduled, notification-enabled events in this order:

| # | Event | Duration | Notes |
|---|-------|----------|-------|
| 1 | **Fajr Prayer** | 25 min | 5-min warning + adhan alert |
| 2 | **Azkar Sabah** | 20 min | Morning remembrance |
| 3 | **Surah Al-Baqara** | 20 min | Quran before sunrise |
| 4 | **School Drop-off** | 10 min | Daily 08:00 |
| 5 | **Dhuhr Prayer** | 20 min | 5-min warning + adhan alert |
| 6 | **School Pickup** | 10 min | Daily 14:00 |
| 7 | **Kids Dars** | 60 min | Tue & Thu 15:00 – Islamic lessons |
| 8 | **Asr Prayer** | 20 min | 5-min warning + adhan alert |
| 9 | **Quran Reading** | 25 min | Post-Asr session |
| 10 | **Family Time** | 90 min | Capped before Maghrib |
| 11 | **Maghrib Prayer** | 20 min | 3-min warning + adhan alert |
| 12 | **Azkar Masah** | 20 min | Evening remembrance |
| 13 | **Isha Prayer** | 20 min | 5-min warning + adhan alert |
| 14 | **Gym Session** | 60 min | Fri & Sun after Isha |

## Prayer times

Calculated for **Malmö, Sweden** (55.6050°N, 13.0038°E) using the **Muslim World League** method — the standard for European mosques.

## How to import

### Google Calendar
1. Open [calendar.google.com](https://calendar.google.com)
2. Settings → **Import & Export** → Import
3. Select `salah-calendar/malmo-sweden.ics`

### iPhone / Apple Calendar
1. AirDrop or email yourself `malmo-sweden.ics`
2. Tap the file → **Add All** events
3. Or: Settings → Calendar → Accounts → Add Account → Other → Add Subscribed Calendar

## How to regenerate

```bash
cd salah-calendar
uv run python generate.py
```

Requires Python 3.11+ and the `requests` package (managed by `uv`).

## Standards

The `.ics` file follows **RFC 5545** (iCalendar):
- CRLF line endings
- Lines folded at 75 UTF-8 octets
- Timezone-aware `DTSTART`/`DTEND` (Europe/Stockholm)
- Globally unique UIDs (`event-date@deen-routine.malmo`)
- UTC `DTSTAMP`
- `VALARM` popup notifications on every event
