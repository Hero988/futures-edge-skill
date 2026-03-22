#!/usr/bin/env python3
"""
economic_calendar.py - Fetch economic calendar events via Finnhub.
Args: --date (YYYY-MM-DD or 'today'), --api-key (or env FINNHUB_API_KEY or diary config).
Filters for US events, sorts by impact. Flags events within 30 minutes of current time.
Outputs JSON to stdout.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_api_key(provided_key=None):
    """Resolve Finnhub API key from args, env, or diary config."""
    # 1. Provided via argument
    if provided_key:
        return provided_key

    # 2. Environment variable
    env_key = os.environ.get("FINNHUB_API_KEY")
    if env_key:
        return env_key

    # 3. Diary config file
    config_paths = [
        Path(__file__).resolve().parent.parent / "diary" / "config.json",
    ]

    for config_path in config_paths:
        try:
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
                key = config.get("finnhub_api_key") or config.get("finnhub_key")
                if key:
                    return key
        except (json.JSONDecodeError, OSError):
            continue

    return None


def parse_date(date_str):
    """Parse date string, supporting 'today' keyword."""
    if date_str.lower() == "today":
        return datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return None


def is_within_minutes(event_time_str, minutes=30):
    """Check if an event time is within `minutes` of current time."""
    now = datetime.now()
    try:
        # Try various time formats
        for fmt in ["%H:%M:%S", "%H:%M", "%Y-%m-%d %H:%M:%S"]:
            try:
                if "T" in str(event_time_str) or "-" in str(event_time_str):
                    event_dt = datetime.fromisoformat(str(event_time_str).replace("Z", ""))
                else:
                    event_time = datetime.strptime(str(event_time_str), fmt)
                    event_dt = now.replace(
                        hour=event_time.hour,
                        minute=event_time.minute,
                        second=event_time.second if hasattr(event_time, "second") else 0,
                    )
                diff = abs((event_dt - now).total_seconds())
                return diff <= minutes * 60
            except (ValueError, TypeError):
                continue
    except Exception:
        pass
    return False


def main():
    parser = argparse.ArgumentParser(description="Fetch economic calendar from Finnhub")
    parser.add_argument(
        "--date",
        default="today",
        help="Date to query (YYYY-MM-DD or 'today', default: today)",
    )
    parser.add_argument("--api-key", default=None, help="Finnhub API key")
    parser.add_argument(
        "--country",
        default="US",
        help="Country filter (default: US)",
    )
    parser.add_argument(
        "--days-ahead",
        type=int,
        default=0,
        help="Additional days to include (default: 0)",
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

    # Find API key
    api_key = find_api_key(args.api_key)
    if not api_key:
        output["error"] = (
            "No Finnhub API key found. Provide via --api-key, "
            "FINNHUB_API_KEY env variable, or diary/config.json. "
            "Get a free key at https://finnhub.io"
        )
        print(json.dumps(output, indent=2))
        return

    # Compute date range
    from_date = date_str
    if args.days_ahead > 0:
        end_dt = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=args.days_ahead)
        to_date = end_dt.strftime("%Y-%m-%d")
    else:
        to_date = date_str

    # Fetch calendar
    try:
        import finnhub

        client = finnhub.Client(api_key=api_key)
        calendar = client.calendar_economic(_from=from_date, to=to_date)

        if not calendar or "economicCalendar" not in calendar:
            output["error"] = "No calendar data returned from Finnhub."
            print(json.dumps(output, indent=2))
            return

        raw_events = calendar.get("economicCalendar", [])

        # Filter by country
        filtered = []
        for event in raw_events:
            country = event.get("country", "")
            if args.country.upper() == "ALL" or country.upper() == args.country.upper():
                filtered.append(event)

        # Format events
        impact_names = {1: "low", 2: "medium", 3: "high"}
        events = []
        for event in filtered:
            impact_num = event.get("impact", 0)
            formatted = {
                "time": event.get("time", ""),
                "event": event.get("event", "Unknown"),
                "impact": impact_names.get(impact_num, "unknown"),
                "impact_level": impact_num,
                "actual": event.get("actual"),
                "estimate": event.get("estimate"),
                "prev": event.get("prev"),
                "unit": event.get("unit", ""),
                "country": event.get("country", ""),
                "upcoming_30min": is_within_minutes(event.get("time", ""), 30),
            }
            events.append(formatted)

        # Sort by impact (high first), then time
        events.sort(key=lambda x: (-x["impact_level"], x["time"]))

        output["events"] = events
        output["total_events"] = len(events)
        output["high_impact_events"] = [e for e in events if e["impact_level"] >= 3]
        output["upcoming_30min"] = [e for e in events if e["upcoming_30min"]]

    except ImportError:
        output["error"] = "finnhub-python not installed. Run install_deps.py first."
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg:
            output["error"] = "Finnhub API key is invalid or expired. Check your key at https://finnhub.io"
        elif "429" in error_msg:
            output["error"] = "Finnhub rate limit exceeded. Wait a moment and try again."
        else:
            output["error"] = f"Finnhub error: {error_msg}"

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
