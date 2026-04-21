"""
Fetch cheapest one-way SFO -> CAN fares for every day in November 2026,
keeping only itineraries with total duration < 18h. Writes data/flights.json.

Uses the Duffel API (https://duffel.com). Search is free on Duffel —
you only pay per confirmed booking, which this script never creates.

Required env vars:
  DUFFEL_ACCESS_TOKEN    starts with 'duffel_test_' or 'duffel_live_'

Optional env vars:
  DUFFEL_API_VERSION   default "v2"
  MAX_DURATION_H       default 18
  ORIGIN               default SFO
  DESTINATION          default CAN
  MONTH_YEAR           default 2026-11
  CABIN_CLASS          default "economy" (also: premium_economy, business, first)
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
MONTH_YEAR = os.environ.get("MONTH_YEAR", "2026-11")  # YYYY-MM
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
    """Parse an ISO-8601 duration like 'PT14H35M' into hours (float)."""
    m = _DUR_RE.match(s or "")
    if not m:
        return float("inf")
    h = int(m.group(1) or 0)
    mins = int(m.group(2) or 0)
    return h + mins / 60.0


def _request_with_retry(method: str, url: str, **kwargs: Any) -> requests.Response:
    """Small retry wrapper for 429/5xx."""
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
    return resp  # final attempt's response (may still be an error)


def search_day(day: date) -> dict[str, Any] | None:
    """Create an offer request for `day` and return the cheapest eligible offer, or None."""
    body = {
        "data": {
            "slices": [
                {
                    "origin": ORIGIN,
                    "destination": DESTINATION,
                    "departure_date": day.isoformat(),
                }
            ],
            "passengers": [{"type": "adult"}],
            "cabin_class": CABIN_CLASS,
        }
    }
    # return_offers=false creates the request fast; we then page offers sorted by price.
    resp = _request_with_retry(
        "POST",
        f"{BASE_URL}/air/offer_requests?return_offers=false",
        headers=_headers(),
        data=json.dumps(body),
    )
    if not resp.ok:
        raise requests.HTTPError(f"{resp.status_code} {resp.text[:300]}", response=resp)
    offer_request_id = resp.json()["data"]["id"]

    # Pull cheapest-first offers, page until we find one under 18h or run out.
    cheapest: dict[str, Any] | None = None
    after: str | None = None
    pages_scanned = 0
    while pages_scanned < 5:  # cap pagination; 5 * 50 offers = plenty
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
                continue  # fails our duration filter

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
            entry = {
                "price": price,
                "currency": offer.get("total_currency", "USD"),
                "duration_hours": round(dur_h, 2),
                "stops": stops,
                "carriers": carriers,
                "depart_time": segments[0].get("departing_at") if segments else None,
                "arrive_time": segments[-1].get("arriving_at") if segments else None,
                "offer_id": offer.get("id"),
                "deep_link": (
                    f"https://www.google.com/travel/flights?q=Flights+from+{ORIGIN}+to+"
                    f"{DESTINATION}+on+{day.isoformat()}"
                ),
            }
            if cheapest is None or entry["price"] < cheapest["price"]:
                cheapest = entry
                # Since offers are sorted by total_amount ascending, the first one that
                # passes the duration filter is the winner — stop early.
                return cheapest

        meta = body.get("meta") or {}
        after = meta.get("after")
        pages_scanned += 1
        if not after:
            break

    return cheapest


def main() -> int:
    year, month = (int(x) for x in MONTH_YEAR.split("-"))
    _, last_day = monthrange(year, month)

    results: dict[str, Any] = {}
    errors: list[dict[str, str]] = []

    for d in range(1, last_day + 1):
        day = date(year, month, d)
        if day < date.today():
            continue
        try:
            entry = search_day(day)
            results[day.isoformat()] = entry
            print(
                f"{day.isoformat()}: "
                + ("no eligible fares" if entry is None else f"${entry['price']:.0f} / {entry['duration_hours']}h")
            )
        except requests.HTTPError as e:
            msg = f"{day.isoformat()}: {e}"
            print(msg, file=sys.stderr)
            errors.append({"date": day.isoformat(), "error": str(e)[:300]})
            results[day.isoformat()] = None
        # gentle pacing
        time.sleep(0.2)

    token = os.environ.get("DUFFEL_ACCESS_TOKEN", "")
    api_env = "live" if token.startswith("duffel_live_") else ("test" if token.startswith("duffel_test_") else "unknown")

    payload = {
        "meta": {
            "origin": ORIGIN,
            "destination": DESTINATION,
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
