# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Test: send message to channel immediately (no waiting for scheduled time)
python bot.py --test

# Run bot in production (stays alive, posts daily at configured time)
python bot.py
```

## Architecture

Single-file bot (`bot.py`) with a separate config file (`config.py`) and secrets in `.env`.

- `.env` — `BOT_TOKEN` and `CHANNEL_ID` (never commit this)
- `config.py` — all user-facing settings: start date, timezone, post time, message template
- `bot.py` — reads config and `.env`, schedules `send_daily_message()` via APScheduler cron

**Flow:** `main()` starts an `AsyncIOScheduler` that fires `send_daily_message()` at `POST_HOUR:POST_MINUTE` in `TIMEZONE` every day. The function computes `day_number = (today - START_DATE).days + 1`, formats `MESSAGE_TEMPLATE`, and sends it via `Bot.send_message()` to `CHANNEL_ID`.

**Test mode:** `python bot.py --test` skips the scheduler and calls `send_daily_message()` once immediately.

## Config reference (`config.py`)

| Variable | Purpose |
|---|---|
| `START_DATE` | ISO date string of Day 1 (e.g. `"2026-04-08"`) |
| `TIMEZONE` | pytz timezone string (e.g. `"Europe/Moscow"`) |
| `POST_HOUR` / `POST_MINUTE` | Time of daily post in the above timezone |
| `TOTAL_DAYS` | Denominator in "День X / Y" |
| `MESSAGE_TEMPLATE` | f-string with `{day}`, `{total}`, `{date}` placeholders |
