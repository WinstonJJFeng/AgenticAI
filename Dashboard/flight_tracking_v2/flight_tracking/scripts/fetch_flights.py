"""
Fetch cheapest one-way fares in BOTH directions (SFO -> CAN and CAN -> SFO)
for every day in November 2026, keeping only itineraries with total duration < 18h.
Writes data/flights.json with shape:

  {
    "meta": {...},
    "days": {
      "2026-11-03": {
        "outbound": { price, duration_hours, stops, carriers, ... } | null,
        "inbound":  { price, duration_hours, stops, carriers, ... } | null
      },
      ...
    }
  }

Uses the Duffel API (https://duffel.com). Search is free on Duffel —
you only pay per confirmed booking, which this script never creates.

Required env vars:
  DUFFEL_ACCESS_TOKEN    starts with 'duffel_test_' or 'duffel_live_'

Optional env vars:
  DUFFEL_API_VERSION   default "v2"
  MAX_DURATION_H       default 18
  ORIGIN               default SFO   (outbound origin / return destination)
  DESTINATION          default CAN   (outbound destination / return origin)
  MONTH_YEAR           default 2026-11
  CABIN_CLASS          default "economy"
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from calendar import monthrange
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import requests

BASE_URL = "https://api.duffel.com"
API_VERSION = os.environ.get("DUFFEL_API_VERSION", "v2")

ORIGIN = os.environ.get("ORIGIN", "SFO")
DESTINATION = os.environ.get("DESTINATION", "CAN")
MONTH_YEAR = os.environ.get("MONTH_YEAR", "2026-11")
MAX_DURATION_H = float(os.environ.get("MAX_DURATION_H", "18"))
CABIN_CLASS = os.environ.get("CABIN_CLASS", "economy")

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "flights.json"


def _token() -> str:
    token = os.environ.get("DUFFEL_ACCESS_TOKEN")
    if not token:
        print("ERROR: DUFFEL_ACCESS_TOKEN must be set.", file=sys.stderr)
        sys.exit(1)
    return token


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_token()}",
        "Duffel-Version": API_VERSION,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


_DUR_RE = re.compile(r"^PT(?:(\d+)H)?(?:(\d+)M)?$")


def parse_iso8601_duration_hours(s: str) -> float:
    m = _DUR_RE.match(s or "")
    if not m:
        return float("inf")
    h = int(m.group(1) or 0)
    mins = int(m.group(2) or 0)
    return h + mins / 60.0


def _request_with_retry(method: str, url: str, **kwargs: Any) -> requests.Response:
    for attempt in range(5):
        resp = requests.request(method, url, timeout=60, **kwargs)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", "2"))
            time.sleep(wait)
            continue
        if 500 <= resp.status_code < 600:
            time.sleep(2 ** attempt)
            continue
        return resp
    return resp


def search_leg(day: date, origin: str, destination: str) -> dict[str, Any] | None:
    """Return the cheapest offer under MAX_DURATION_H hours for a given day/route, or None."""
    body = {
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": day.isoformat(),
                }
            ],
            "passengers": [{"type": "adult"}],
            "cabin_class": CABIN_CLASS,
        }
    }
    resp = _request_with_retry(
        "POST",
        f"{BASE_URL}/air/offer_requests?return_offers=false",
        headers=_headers(),
        data=json.dumps(body),
    )
    if not resp.ok:
        raise requests.HTTPError(f"{resp.status_code} {resp.text[:300]}", response=resp)
    offer_request_id = resp.json()["data"]["id"]

    after: str | None = None
    for _ in range(5):
        params = {
            "offer_request_id": offer_request_id,
            "sort": "total_amount",
            "limit": 50,
        }
        if after:
            params["after"] = after
        resp = _request_with_retry(
            "GET", f"{BASE_URL}/air/offers", headers=_headers(), params=params
        )
        if not resp.ok:
            raise requests.HTTPError(f"{resp.status_code} {resp.text[:300]}", response=resp)
        body = resp.json()
        for offer in body.get("data", []):
            slices = offer.get("slices") or []
            if not slices:
                continue
            slc = slices[0]
            dur_h = parse_iso8601_duration_hours(slc.get("duration", ""))
            if dur_h >= MAX_DURATION_H:
                continue

            try:
                price = float(offer["total_amount"])
            except (KeyError, TypeError, ValueError):
                continue

            segments = slc.get("segments") or []
            carriers = sorted(
                {
                    (seg.get("marketing_carrier") or {}).get("iata_code")
                    for seg in segments
                    if (seg.get("marketing_carrier") or {}).get("iata_code")
                }
            )
            stops = max(len(segments) - 1, 0)
            # Offers are sorted ascending by total_amount; first passing offer is cheapest.
            return {
                "price": price,
                "currency": offer.get("total_currency", "USD"),
                "duration_hours": round(dur_h, 2),
                "stops": stops,
                "carriers": carriers,
                "depart_time": segments[0].get("departing_at") if segments else None,
                "arrive_time": segments[-1].get("arriving_at") if segments else None,
                "offer_id": offer.get("id"),
                "deep_link": (
                    f"https://www.google.com/travel/flights?q=Flights+from+{origin}+to+"
                    f"{destination}+on+{day.isoformat()}"
                ),
            }

        meta = body.get("meta") or {}
        after = meta.get("after")
        if not after:
            break

    return None


def main() -> int:
    year, month = (int(x) for x in MONTH_YEAR.split("-"))
    _, last_day = monthrange(year, month)

    routes = [
        ("outbound", ORIGIN, DESTINATION),
        ("inbound", DESTINATION, ORIGIN),
    ]

    results: dict[str, Any] = {}
    errors: list[dict[str, str]] = []

    for d in range(1, last_day + 1):
        day = date(year, month, d)
        if day < date.today():
            continue
        day_key = day.isoformat()
        results[day_key] = {}
        for label, orig, dest in routes:
            try:
                entry = search_leg(day, orig, dest)
                results[day_key][label] = entry
                tag = "no eligible" if entry is None else f"${entry['price']:.0f} / {entry['duration_hours']}h"
                print(f"{day_key} {orig}->{dest}: {tag}")
            except requests.HTTPError as e:
                msg = f"{day_key} {orig}->{dest}: {e}"
                print(msg, file=sys.stderr)
                errors.append({"date": day_key, "route": f"{orig}->{dest}", "error": str(e)[:300]})
                results[day_key][label] = None
            time.sleep(0.2)  # pacing

    token = os.environ.get("DUFFEL_ACCESS_TOKEN", "")
    api_env = (
        "live" if token.startswith("duffel_live_")
        else ("test" if token.startswith("duffel_test_") else "unknown")
    )

    payload = {
        "meta": {
            "routes": [
                {"label": "outbound", "origin": ORIGIN, "destination": DESTINATION},
                {"label": "inbound",  "origin": DESTINATION, "destination": ORIGIN},
            ],
            "month": MONTH_YEAR,
            "max_duration_hours": MAX_DURATION_H,
            "cabin_class": CABIN_CLASS,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "api": "duffel",
            "api_env": api_env,
            "errors": errors,
        },
        "days": results,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
