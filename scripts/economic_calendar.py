#!/usr/bin/env python3
"""
economic_calendar.py - Fetch economic calendar events via TradingView.
Args: --date (YYYY-MM-DD or 'today'), --country (default US), --importance (default '2,3').
Filters by country and importance. Flags events within 30 minutes of current time.
Outputs JSON to stdout.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone


def parse_date(date_str):
    """Parse date string, supporting 'today' keyword."""
    if date_str.lower() == "today":
        return datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return None


def is_within_minutes(event_datetime_str, minutes=30):
    """Check if an event time is within `minutes` of current time."""
    now = datetime.now()
    try:
        # TradingView returns ISO format dates like "2026-03-22T08:30:00-04:00"
        # or "2026-03-22T13:30:00+00:00"
        for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
            try:
                event_dt = datetime.strptime(str(event_datetime_str), fmt)
                # If timezone-aware, convert to local naive for comparison
                if event_dt.tzinfo is not None:
                    event_dt = event_dt.replace(tzinfo=None) - event_dt.utcoffset() + (now - datetime.utcnow())
                diff = abs((event_dt - now).total_seconds())
                return diff <= minutes * 60
            except (ValueError, TypeError):
                continue
        # Fallback: try fromisoformat
        event_dt = datetime.fromisoformat(str(event_datetime_str).replace("Z", "+00:00"))
        event_dt = event_dt.replace(tzinfo=None)
        diff = abs((event_dt - datetime.utcnow()).total_seconds())
        return diff <= minutes * 60
    except Exception:
        pass
    return False


def fetch_tradingview_calendar(date_str, country="US", importance="2,3"):
    """Fetch economic calendar from TradingView's endpoint."""
    # Compute date range as unix timestamps
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    from_ts = int(target_date.replace(hour=0, minute=0, second=0).timestamp())
    to_ts = int(target_date.replace(hour=23, minute=59, second=59).timestamp())

    url = "https://economic-calendar.tradingview.com/events"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.tradingview.com",
        "Referer": "https://www.tradingview.com/",
    }

    body = urllib.parse.urlencode({
        "from": from_ts,
        "to": to_ts,
        "countries": country,
        "importance": importance,
    })

    req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data, None
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return None, (
                "TradingView economic calendar returned 403 Forbidden. "
                "The endpoint may be temporarily blocked or require browser access. "
                "Check https://www.tradingview.com/economic-calendar/ manually for today's events."
            )
        return None, f"HTTP error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Connection error: {e.reason}"
    except Exception as e:
        return None, f"Request error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Fetch economic calendar from TradingView")
    parser.add_argument(
        "--date",
        default="today",
        help="Date to query (YYYY-MM-DD or 'today', default: today)",
    )
    parser.add_argument(
        "--country",
        default="US",
        help="Country filter (default: US)",
    )
    parser.add_argument(
        "--importance",
        default="2,3",
        help="Importance filter: comma-separated 0-3 (default: '2,3' for medium+high)",
    )
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "date": None,
        "events": [],
        "high_impact_events": [],
        "upcoming_30min": [],
        "total_events": 0,
        "error": None,
    }

    # Parse date
    date_str = parse_date(args.date)
    if date_str is None:
        output["error"] = f"Invalid date format: '{args.date}'. Use YYYY-MM-DD or 'today'."
        print(json.dumps(output, indent=2))
        return

    output["date"] = date_str

    # Fetch calendar from TradingView
    raw_events, fetch_error = fetch_tradingview_calendar(
        date_str, country=args.country, importance=args.importance
    )

    if fetch_error:
        output["error"] = fetch_error
        print(json.dumps(output, indent=2))
        return

    # TradingView returns {"status": "ok", "result": [...]} or a list directly
    if isinstance(raw_events, dict):
        raw_events = raw_events.get("result", raw_events.get("data", []))
    if not raw_events or not isinstance(raw_events, list):
        output["error"] = "No calendar data returned from TradingView. Check https://www.tradingview.com/economic-calendar/ manually."
        print(json.dumps(output, indent=2))
        return

    # Filter by country (TradingView uses 2-letter codes)
    country_upper = args.country.upper()
    raw_events = [e for e in raw_events if e.get("country", "").upper() == country_upper]
    if not raw_events:
        output["error"] = f"No {args.country} events found for {date_str}. Check https://www.tradingview.com/economic-calendar/ manually."
        output["note"] = "TradingView economic calendar may have limited data for some dates."
        print(json.dumps(output, indent=2))
        return

    # Format events
    importance_names = {0: "holiday", 1: "low", 2: "medium", 3: "high"}
    events = []

    for event in raw_events:
        # TradingView fields: title, country, indicator, importance, actual, forecast, previous, date, time, etc.
        imp_num = event.get("importance", 0)
        if imp_num is None:
            imp_num = 0

        # Build event time string from the date field
        event_time = event.get("date", "") or event.get("time", "")

        formatted = {
            "time": event_time,
            "title": event.get("title", "") or event.get("indicator", "Unknown"),
            "importance": importance_names.get(imp_num, "unknown"),
            "importance_level": imp_num,
            "actual": event.get("actual"),
            "forecast": event.get("forecast"),
            "previous": event.get("previous"),
            "country": event.get("country", ""),
            "upcoming_30min": is_within_minutes(event_time, 30),
        }
        events.append(formatted)

    # Sort by importance (high first), then time
    events.sort(key=lambda x: (-x["importance_level"], x["time"]))

    output["events"] = events
    output["total_events"] = len(events)
    output["high_impact_events"] = [e for e in events if e["importance_level"] >= 3]
    output["upcoming_30min"] = [e for e in events if e["upcoming_30min"]]

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
