#!/usr/bin/env python3
"""
diary_review.py - Pattern recognition across diary entries.
Args: --diary-path, --period (week/month/quarter).
Reads post-session files and trade logs. Identifies patterns, mistakes, and trends.
Outputs JSON to stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict


def parse_date_arg(date_str):
    """Parse date argument."""
    if date_str is None or date_str.lower() == "today":
        return datetime.now().date()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return datetime.now().date()


def get_date_range(period, ref_date):
    """Return (start_date, end_date) for the given period."""
    if period == "week":
        start = ref_date - timedelta(days=ref_date.weekday())
        end = start + timedelta(days=6)
        return start, end
    elif period == "month":
        start = ref_date.replace(day=1)
        if ref_date.month == 12:
            end = ref_date.replace(year=ref_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = ref_date.replace(month=ref_date.month + 1, day=1) - timedelta(days=1)
        return start, end
    elif period == "quarter":
        quarter_start_month = ((ref_date.month - 1) // 3) * 3 + 1
        start = ref_date.replace(month=quarter_start_month, day=1)
        end_month = quarter_start_month + 2
        if end_month == 12:
            end = ref_date.replace(month=12, day=31)
        else:
            end = ref_date.replace(month=end_month + 1, day=1) - timedelta(days=1)
        return start, end
    else:  # all
        return datetime(2020, 1, 1).date(), datetime(2030, 12, 31).date()


def find_diary_files(diary_path, start_date, end_date):
    """Find all diary files (trade logs and post-session) within the date range."""
    diary = Path(diary_path)
    files = {"trades": [], "post_sessions": [], "premarket": []}

    if not diary.exists():
        return files

    for year_dir in sorted(diary.iterdir()):
        if not year_dir.is_dir() or year_dir.name.startswith(".") or year_dir.name in ("lessons", "stats", "backtests", "config.json"):
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for day_dir in sorted(month_dir.iterdir()):
                if not day_dir.is_dir():
                    continue
                try:
                    dir_date = datetime.strptime(day_dir.name, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if dir_date < start_date or dir_date > end_date:
                    continue

                # Trade files
                trades_dir = day_dir / "trades"
                if trades_dir.exists():
                    for tf in sorted(trades_dir.iterdir()):
                        if tf.suffix == ".md" and tf.name.startswith("trade-"):
                            files["trades"].append((dir_date, tf))

                # Post-session
                post = day_dir / "post-session.md"
                if post.exists():
                    files["post_sessions"].append((dir_date, post))

                # Pre-market
                pre = day_dir / "premarket.md"
                if pre.exists():
                    files["premarket"].append((dir_date, pre))

    return files


def parse_trade_file(filepath):
    """Parse a trade log for review analysis."""
    trade = {
        "setup": None,
        "session": None,
        "instrument": None,
        "direction": None,
        "pnl": None,
        "r_multiple": None,
        "result": None,
        "grade": None,
        "plan_followed": None,
        "strategy": None,
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return trade

    # Extract fields
    patterns = {
        "setup": r"[Ss]etup[:\s]*\*?\*?(.+?)(?:\n|\||\*)",
        "session": r"[Ss]ession[:\s]*\*?\*?([\w\s]+?)(?:\n|\||\*)",
        "instrument": r"[Ii]nstrument[:\s]*\*?\*?([A-Z0-9!]+)",
        "direction": r"[Dd]irection[:\s]*\*?\*?(long|short|Long|Short)",
        "pnl": r"[Pp](?:&|n)[Ll][:\s]*\$?\*?\*?([-+]?[\d,]+\.?\d*)",
        "r_multiple": r"[Rr][-\s]?[Mm]ultiple[:\s]*\*?\*?([-+]?[\d.]+)",
        "grade": r"[Gg]rade[:\s]*\*?\*?([A-Fa-f][+-]?)",
        "strategy": r"[Ss]trategy[:\s]*\*?\*?(.+?)(?:\n|\||\*)",
    }

    for field, pat in patterns.items():
        match = re.search(pat, content)
        if match:
            val = match.group(1).strip().rstrip("*")
            if field == "pnl":
                try:
                    trade[field] = float(val.replace(",", ""))
                except ValueError:
                    pass
            elif field == "r_multiple":
                try:
                    trade[field] = float(val)
                except ValueError:
                    pass
            else:
                trade[field] = val

    # Check plan adherence
    plan_patterns = [
        r"[Pp]lan\s+[Ff]ollowed[:\s]*\*?\*?(yes|no|Yes|No|YES|NO|partially)",
        r"[Ff]ollowed\s+[Pp]lan[:\s]*\*?\*?(yes|no|Yes|No|YES|NO|partially)",
    ]
    for pat in plan_patterns:
        match = re.search(pat, content)
        if match:
            val = match.group(1).strip().lower()
            trade["plan_followed"] = val in ("yes", "true")
            break

    # Determine result
    if trade["pnl"] is not None:
        trade["result"] = "win" if trade["pnl"] > 0 else ("loss" if trade["pnl"] < 0 else "breakeven")
    elif trade["r_multiple"] is not None:
        trade["result"] = "win" if trade["r_multiple"] > 0 else ("loss" if trade["r_multiple"] < 0 else "breakeven")

    return trade


def parse_post_session(filepath):
    """Parse a post-session file for mistakes and lessons."""
    data = {
        "grade": None,
        "mistakes": [],
        "lessons": [],
        "emotions": [],
        "rules_followed": None,
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return data

    # Grade
    match = re.search(r"[Gg]rade[:\s]*\*?\*?([A-Fa-f][+-]?)", content)
    if match:
        data["grade"] = match.group(1).strip()

    # Mistakes section
    mistake_section = re.search(
        r"(?:[Mm]istakes?|[Ee]rrors?|[Ww]hat\s+went\s+wrong)[:\s]*\n((?:[-*]\s+.+\n?)+)",
        content,
    )
    if mistake_section:
        mistakes = re.findall(r"[-*]\s+(.+)", mistake_section.group(1))
        data["mistakes"] = [m.strip() for m in mistakes]

    # Lessons section
    lesson_section = re.search(
        r"(?:[Ll]essons?|[Kk]ey\s+[Tt]akeaways?|[Ww]hat\s+[Ii]\s+[Ll]earned)[:\s]*\n((?:[-*]\s+.+\n?)+)",
        content,
    )
    if lesson_section:
        lessons = re.findall(r"[-*]\s+(.+)", lesson_section.group(1))
        data["lessons"] = [l.strip() for l in lessons]

    # Emotions
    emotion_patterns = [
        r"[Ee]motional?\s+[Ss]tate[:\s]*\*?\*?(.+?)(?:\n|\*)",
        r"[Ff]eelings?[:\s]*\*?\*?(.+?)(?:\n|\*)",
        r"[Mm]indset[:\s]*\*?\*?(.+?)(?:\n|\*)",
    ]
    for pat in emotion_patterns:
        match = re.search(pat, content)
        if match:
            data["emotions"].append(match.group(1).strip())

    # Rules compliance
    rules_match = re.search(r"[Rr]ules?\s+[Ff]ollowed[:\s]*\*?\*?([\d]+)[/%]", content)
    if rules_match:
        try:
            data["rules_followed"] = int(rules_match.group(1))
        except ValueError:
            pass

    return data


def analyze_patterns(trades_by_date, post_sessions_by_date):
    """Analyze patterns across the review period."""
    analysis = {
        "top_winning_setups": [],
        "top_losing_setups": [],
        "common_mistakes": [],
        "day_of_week_performance": {},
        "session_performance": {},
        "rule_compliance": {"scores": [], "average": None},
        "grade_distribution": {},
        "suggested_focus": [],
        "plan_adherence": {"followed": 0, "deviated": 0, "rate": None},
        "streak_analysis": {"current_wins": 0, "current_losses": 0, "max_wins": 0, "max_losses": 0},
    }

    # Aggregate setup performance
    setup_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0, "r": 0.0})
    session_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0})
    dow_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0})
    all_mistakes = []
    grade_counts = Counter()

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for trade_date, trades in sorted(trades_by_date.items()):
        dow = day_names[trade_date.weekday()]

        for t in trades:
            setup = t.get("setup") or "unknown"
            session = t.get("session") or "unknown"
            pnl = t.get("pnl") or 0
            r = t.get("r_multiple") or 0
            result = t.get("result")

            setup_stats[setup]["trades"] += 1
            setup_stats[setup]["pnl"] += pnl
            setup_stats[setup]["r"] += r

            session_stats[session]["trades"] += 1
            session_stats[session]["pnl"] += pnl

            dow_stats[dow]["trades"] += 1
            dow_stats[dow]["pnl"] += pnl

            if result == "win":
                setup_stats[setup]["wins"] += 1
                session_stats[session]["wins"] += 1
                dow_stats[dow]["wins"] += 1

            if t.get("plan_followed") is True:
                analysis["plan_adherence"]["followed"] += 1
            elif t.get("plan_followed") is False:
                analysis["plan_adherence"]["deviated"] += 1

    # Post-session analysis
    for ps_date, ps_data in post_sessions_by_date.items():
        if ps_data.get("grade"):
            grade_counts[ps_data["grade"]] += 1
        if ps_data.get("rules_followed") is not None:
            analysis["rule_compliance"]["scores"].append(ps_data["rules_followed"])
        all_mistakes.extend(ps_data.get("mistakes", []))

    # Top winning setups (by total R, min 2 trades)
    winning_setups = [
        {"setup": k, "trades": v["trades"], "total_r": round(v["r"], 2), "pnl": round(v["pnl"], 2),
         "win_rate": round(v["wins"] / v["trades"] * 100, 1) if v["trades"] > 0 else 0}
        for k, v in setup_stats.items() if v["r"] > 0
    ]
    winning_setups.sort(key=lambda x: x["total_r"], reverse=True)
    analysis["top_winning_setups"] = winning_setups[:3]

    # Top losing setups
    losing_setups = [
        {"setup": k, "trades": v["trades"], "total_r": round(v["r"], 2), "pnl": round(v["pnl"], 2),
         "win_rate": round(v["wins"] / v["trades"] * 100, 1) if v["trades"] > 0 else 0}
        for k, v in setup_stats.items() if v["r"] < 0
    ]
    losing_setups.sort(key=lambda x: x["total_r"])
    analysis["top_losing_setups"] = losing_setups[:3]

    # Common mistakes
    mistake_counts = Counter()
    for m in all_mistakes:
        # Normalize mistake text for grouping
        normalized = m.lower().strip().rstrip(".")
        mistake_counts[normalized] += 1
    analysis["common_mistakes"] = [
        {"mistake": k, "frequency": v}
        for k, v in mistake_counts.most_common(5)
    ]

    # Day of week performance
    for dow in day_names[:5]:  # Only weekdays
        if dow in dow_stats:
            d = dow_stats[dow]
            analysis["day_of_week_performance"][dow] = {
                "trades": d["trades"],
                "pnl": round(d["pnl"], 2),
                "win_rate": round(d["wins"] / d["trades"] * 100, 1) if d["trades"] > 0 else 0,
            }

    # Best / worst day
    if analysis["day_of_week_performance"]:
        best_day = max(analysis["day_of_week_performance"].items(), key=lambda x: x[1]["pnl"])
        worst_day = min(analysis["day_of_week_performance"].items(), key=lambda x: x[1]["pnl"])
        analysis["best_day_of_week"] = {"day": best_day[0], **best_day[1]}
        analysis["worst_day_of_week"] = {"day": worst_day[0], **worst_day[1]}

    # Session performance
    for sess, d in session_stats.items():
        analysis["session_performance"][sess] = {
            "trades": d["trades"],
            "pnl": round(d["pnl"], 2),
            "win_rate": round(d["wins"] / d["trades"] * 100, 1) if d["trades"] > 0 else 0,
        }

    if analysis["session_performance"]:
        best_session = max(analysis["session_performance"].items(), key=lambda x: x[1]["pnl"])
        worst_session = min(analysis["session_performance"].items(), key=lambda x: x[1]["pnl"])
        analysis["best_session"] = {"session": best_session[0], **best_session[1]}
        analysis["worst_session"] = {"session": worst_session[0], **worst_session[1]}

    # Rule compliance average
    if analysis["rule_compliance"]["scores"]:
        analysis["rule_compliance"]["average"] = round(
            sum(analysis["rule_compliance"]["scores"]) / len(analysis["rule_compliance"]["scores"]), 1
        )

    # Grade distribution
    analysis["grade_distribution"] = dict(grade_counts)

    # Plan adherence rate
    total_adherence = analysis["plan_adherence"]["followed"] + analysis["plan_adherence"]["deviated"]
    if total_adherence > 0:
        analysis["plan_adherence"]["rate"] = round(
            analysis["plan_adherence"]["followed"] / total_adherence * 100, 1
        )

    # Suggested focus areas
    if analysis["top_losing_setups"]:
        worst = analysis["top_losing_setups"][0]
        analysis["suggested_focus"].append(
            f"Review and potentially stop trading '{worst['setup']}' setup (lost {worst['total_r']}R)"
        )
    if analysis["common_mistakes"]:
        top_mistake = analysis["common_mistakes"][0]
        analysis["suggested_focus"].append(
            f"Address recurring mistake: '{top_mistake['mistake']}' ({top_mistake['frequency']}x)"
        )
    if analysis["plan_adherence"].get("rate") is not None and analysis["plan_adherence"]["rate"] < 80:
        analysis["suggested_focus"].append(
            f"Improve plan adherence (currently {analysis['plan_adherence']['rate']}%)"
        )
    if not analysis["suggested_focus"]:
        analysis["suggested_focus"].append("Maintain current approach. Focus on consistency.")

    return analysis


def main():
    parser = argparse.ArgumentParser(description="Diary pattern recognition and review")
    parser.add_argument("--diary-path", required=True, help="Path to diary directory")
    parser.add_argument(
        "--period",
        choices=["week", "month", "quarter", "all"],
        default="week",
        help="Review period (default: week)",
    )
    parser.add_argument("--date", default="today", help="Reference date (default: today)")
    args = parser.parse_args()

    ref_date = parse_date_arg(args.date)
    start_date, end_date = get_date_range(args.period, ref_date)

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "period": args.period,
        "date_range": {"start": str(start_date), "end": str(end_date)},
        "analysis": None,
        "total_trading_days": 0,
        "total_trades": 0,
        "error": None,
    }

    # Find files
    files = find_diary_files(args.diary_path, start_date, end_date)

    if not files["trades"] and not files["post_sessions"]:
        output["error"] = f"No diary entries found for {args.period} ({start_date} to {end_date})"
        output["analysis"] = analyze_patterns({}, {})
        print(json.dumps(output, indent=2))
        return

    # Parse trade files grouped by date
    trades_by_date = defaultdict(list)
    for trade_date, filepath in files["trades"]:
        trade = parse_trade_file(filepath)
        trade["date"] = str(trade_date)
        trades_by_date[trade_date].append(trade)
        output["total_trades"] += 1

    # Parse post-session files
    post_sessions_by_date = {}
    for ps_date, filepath in files["post_sessions"]:
        ps_data = parse_post_session(filepath)
        post_sessions_by_date[ps_date] = ps_data

    output["total_trading_days"] = len(set(list(trades_by_date.keys()) + list(post_sessions_by_date.keys())))

    # Analyze patterns
    output["analysis"] = analyze_patterns(trades_by_date, post_sessions_by_date)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
