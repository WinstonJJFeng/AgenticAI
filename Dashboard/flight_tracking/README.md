# SFO → CAN · November 2026 Fare Dashboard

A calendar-view dashboard showing the cheapest one-way fare from San Francisco (SFO) to Guangzhou Baiyun (CAN) for each day in November 2026, filtered to itineraries under 18 hours. Refreshed daily by a GitHub Actions workflow and served via GitHub Pages.

## What's in this folder

- `index.html` — the dashboard. Renders a month calendar, color-coded by price tercile; click a day for details.
- `data/flights.json` — data file rewritten daily by the workflow.
- `scripts/fetch_flights.py` — queries Duffel's Flight Offers API for each day of the month, keeps the cheapest itinerary under 18h.
- `scripts/requirements.txt` — Python deps.
- `.github/workflows/refresh.yml` — cron workflow (daily 08:00 PT during PST) that runs the fetch, commits the JSON, and deploys Pages.

## One-time setup

### 1. Get a Duffel access token

Sign up at <https://app.duffel.com> (about a minute). Under `Developers → Access tokens`, create a token:

- **Test mode** (`duffel_test_…`): works immediately, returns plausible synthetic fares. Good for end-to-end testing.
- **Live mode** (`duffel_live_…`): real airline content. Duffel requires a short account-verification step to unlock live tokens — usually same-day. You want live mode for accurate pricing.

Duffel's pricing model is pay-per-booking only — searches are free at any volume, so this dashboard costs $0 to operate.

### 2. Add the repo secret

In GitHub: `Settings → Secrets and variables → Actions → New repository secret`

- `DUFFEL_ACCESS_TOKEN` — paste the token from step 1

Optional repo **variable** (not secret): `DUFFEL_API_VERSION = v2` (default). Bump only if Duffel releases a version you need to pin to.

### 3. Enable GitHub Pages

`Settings → Pages → Build and deployment → Source: GitHub Actions`. The workflow's `deploy-pages` job publishes this folder. The site will live at `https://<username>.github.io/<repo>/` — since this dashboard is uploaded from `Dashboard/`, `index.html` lands at the Pages root.

### 4. Seed the first run

`Actions → Refresh flight dashboard → Run workflow` so `data/flights.json` gets populated without waiting for the next cron tick.

## About the schedule

The cron is `0 16 * * *` (16:00 UTC), which is **08:00 PT during Pacific Standard Time** (early November through mid-March). Your target month is entirely in November 2026 — PST is in effect all month, so the 8am PT timing is exact.

If you later extend this past DST boundaries and want 08:00 PT year-round, either add a second `0 15 * * *` cron and gate by month, or accept a 1-hour seasonal drift.

## Changing the search

All parameters are env vars in the workflow:

```yaml
ORIGIN: SFO
DESTINATION: CAN
MONTH_YEAR: "2026-11"
MAX_DURATION_H: "18"
CABIN_CLASS: economy     # or premium_economy, business, first
```

## Notes & caveats

- Duffel aggregates 300+ airlines via GDS and direct NDC connections, including China Southern, Cathay Pacific, and United on SFO-CAN routes — the relevant carriers for this lane.
- "Duration" is the itinerary's total elapsed time (including layovers), matching how Google Flights reports it.
- Each cell links to a Google Flights search for that date so you can cross-check the price before booking.
- In **test mode**, fares are synthetic; do not treat them as real prices. Switch to a live token before trusting the numbers.
- Duffel returns offers sorted by price — we grab the cheapest one that fits under 18h and stop. Since Duffel sorts ascending, the first passing offer is guaranteed to be the cheapest eligible.
