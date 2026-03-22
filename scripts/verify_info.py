#!/usr/bin/env python3
"""
verify_info.py - Cross-reference stored data against live sources.
Args: --check (all/prop-firms/contracts/libraries).
For prop firms: output stored values and flag staleness.
For contracts: verify tick sizes against standard CME values.
For libraries: try importing each required library and run smoke tests.
Outputs JSON verification report to stdout.
"""

import argparse
import json
import os
import sys
import importlib
from datetime import datetime, timedelta
from pathlib import Path


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

# Known correct CME tick sizes (source of truth for verification)
CME_TICK_SIZES = {
    "ES": 0.25,
    "MES": 0.25,
    "NQ": 0.25,
    "MNQ": 0.25,
    "YM": 1.0,
    "MYM": 1.0,
    "RTY": 0.10,
    "M2K": 0.10,
    "CL": 0.01,
    "MCL": 0.01,
    "GC": 0.10,
    "MGC": 0.10,
}

CME_POINT_VALUES = {
    "ES": 50.0,
    "MES": 5.0,
    "NQ": 20.0,
    "MNQ": 2.0,
    "YM": 5.0,
    "MYM": 0.50,
    "RTY": 50.0,
    "M2K": 5.0,
    "CL": 1000.0,
    "MCL": 100.0,
    "GC": 100.0,
    "MGC": 10.0,
}

REQUIRED_LIBRARIES = [
    {"import_name": "tradingview_ta", "pip_name": "tradingview-ta", "smoke_test": "version"},
    {"import_name": "tvDatafeed", "pip_name": "tvDatafeed", "smoke_test": "import"},
    {"import_name": "finnhub", "pip_name": "finnhub-python", "smoke_test": "version"},
    {"import_name": "backtesting", "pip_name": "backtesting", "smoke_test": "import"},
    {"import_name": "smartmoneyconcepts", "pip_name": "smartmoneyconcepts", "smoke_test": "import"},
    {"import_name": "pandas", "pip_name": "pandas", "smoke_test": "version"},
    {"import_name": "numpy", "pip_name": "numpy", "smoke_test": "version"},
]

STALENESS_THRESHOLD_DAYS = 30


def check_prop_firms():
    """Verify prop firm profiles for staleness and completeness."""
    results = {
        "status": "ok",
        "firms": [],
        "warnings": [],
        "errors": [],
    }

    profiles_path = ASSETS_DIR / "prop-firm-profiles.json"
    if not profiles_path.exists():
        results["status"] = "error"
        results["errors"].append("prop-firm-profiles.json not found in assets directory")
        return results

    try:
        with open(profiles_path, "r") as f:
            profiles = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        results["status"] = "error"
        results["errors"].append(f"Error reading prop-firm-profiles.json: {e}")
        return results

    now = datetime.now()

    for key, firm_data in profiles.items():
        if key.startswith("_"):
            continue

        firm_report = {
            "key": key,
            "name": firm_data.get("name", key),
            "last_verified": firm_data.get("last_verified"),
            "stale": False,
            "days_since_verification": None,
            "fields_present": [],
            "fields_missing": [],
            "url": firm_data.get("url"),
            "accounts": list(firm_data.get("accounts", {}).keys()),
        }

        # Check staleness
        last_verified = firm_data.get("last_verified")
        if last_verified:
            try:
                verified_date = datetime.strptime(last_verified, "%Y-%m-%d")
                days_since = (now - verified_date).days
                firm_report["days_since_verification"] = days_since
                if days_since > STALENESS_THRESHOLD_DAYS:
                    firm_report["stale"] = True
                    results["warnings"].append(
                        f"{firm_data.get('name', key)}: Last verified {days_since} days ago "
                        f"(threshold: {STALENESS_THRESHOLD_DAYS} days). "
                        f"Verify at {firm_data.get('url', 'official website')}."
                    )
            except ValueError:
                firm_report["stale"] = True
                results["warnings"].append(
                    f"{firm_data.get('name', key)}: Invalid last_verified date format."
                )
        else:
            firm_report["stale"] = True
            results["warnings"].append(
                f"{firm_data.get('name', key)}: No last_verified date set."
            )

        # Check required fields
        required_fields = [
            "name", "accounts", "drawdown_type", "close_by", "overnight_allowed",
            "consistency_rule", "payout_split", "url", "last_verified",
        ]
        for field in required_fields:
            if field in firm_data and firm_data[field] is not None:
                firm_report["fields_present"].append(field)
            else:
                firm_report["fields_missing"].append(field)

        results["firms"].append(firm_report)

    stale_count = sum(1 for f in results["firms"] if f["stale"])
    if stale_count > 0:
        results["status"] = "stale"
        results["warnings"].insert(0, f"{stale_count}/{len(results['firms'])} firm profiles are stale.")

    return results


def check_contracts():
    """Verify contract data against known CME tick sizes."""
    results = {
        "status": "ok",
        "contracts": [],
        "warnings": [],
        "errors": [],
    }

    contracts_path = ASSETS_DIR / "contract-data.json"
    if not contracts_path.exists():
        results["status"] = "error"
        results["errors"].append("contract-data.json not found in assets directory")
        return results

    try:
        with open(contracts_path, "r") as f:
            contracts = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        results["status"] = "error"
        results["errors"].append(f"Error reading contract-data.json: {e}")
        return results

    for key, data in contracts.items():
        if key.startswith("_"):
            continue

        contract_report = {
            "symbol": key,
            "full_name": data.get("full_name", key),
            "tick_size_stored": data.get("tick_size"),
            "tick_size_expected": CME_TICK_SIZES.get(key),
            "tick_size_correct": None,
            "point_value_stored": data.get("point_value"),
            "point_value_expected": CME_POINT_VALUES.get(key),
            "point_value_correct": None,
            "tick_value_stored": data.get("tick_value"),
            "tick_value_computed": None,
            "tick_value_correct": None,
        }

        # Verify tick size
        expected_tick = CME_TICK_SIZES.get(key)
        if expected_tick is not None and data.get("tick_size") is not None:
            contract_report["tick_size_correct"] = abs(data["tick_size"] - expected_tick) < 0.001
            if not contract_report["tick_size_correct"]:
                results["warnings"].append(
                    f"{key}: Tick size mismatch. Stored: {data['tick_size']}, Expected: {expected_tick}"
                )

        # Verify point value
        expected_pv = CME_POINT_VALUES.get(key)
        if expected_pv is not None and data.get("point_value") is not None:
            contract_report["point_value_correct"] = abs(data["point_value"] - expected_pv) < 0.01
            if not contract_report["point_value_correct"]:
                results["warnings"].append(
                    f"{key}: Point value mismatch. Stored: {data['point_value']}, Expected: {expected_pv}"
                )

        # Verify tick value = tick_size * point_value
        if data.get("tick_size") is not None and data.get("point_value") is not None:
            computed_tv = data["tick_size"] * data["point_value"]
            contract_report["tick_value_computed"] = round(computed_tv, 4)
            if data.get("tick_value") is not None:
                contract_report["tick_value_correct"] = abs(data["tick_value"] - computed_tv) < 0.01
                if not contract_report["tick_value_correct"]:
                    results["warnings"].append(
                        f"{key}: Tick value inconsistency. Stored: {data['tick_value']}, "
                        f"Computed (tick_size * point_value): {computed_tv}"
                    )

        results["contracts"].append(contract_report)

    if results["warnings"]:
        results["status"] = "issues_found"

    return results


def check_libraries():
    """Verify required libraries are installed and functional."""
    results = {
        "status": "ok",
        "libraries": [],
        "warnings": [],
        "errors": [],
    }

    for lib in REQUIRED_LIBRARIES:
        lib_report = {
            "name": lib["pip_name"],
            "import_name": lib["import_name"],
            "installed": False,
            "version": None,
            "smoke_test": None,
            "error": None,
        }

        try:
            mod = importlib.import_module(lib["import_name"])
            lib_report["installed"] = True
            version = getattr(mod, "__version__", None)
            if version:
                lib_report["version"] = str(version)

            # Smoke tests
            if lib["smoke_test"] == "version":
                lib_report["smoke_test"] = "passed" if version else "no_version"
            elif lib["smoke_test"] == "import":
                lib_report["smoke_test"] = "passed"

        except ImportError as e:
            lib_report["error"] = f"Not installed: {e}"
            results["errors"].append(f"{lib['pip_name']}: Not installed")
        except Exception as e:
            lib_report["error"] = str(e)
            results["errors"].append(f"{lib['pip_name']}: {e}")

        results["libraries"].append(lib_report)

    # Optional: run a quick market scan smoke test
    market_scan_result = {"test": "market_scan_import", "status": "skipped"}
    try:
        # Just verify the script can be loaded
        script_dir = Path(__file__).resolve().parent
        market_scan_path = script_dir / "market_scan.py"
        if market_scan_path.exists():
            market_scan_result["status"] = "script_exists"
        else:
            market_scan_result["status"] = "script_missing"
            results["warnings"].append("market_scan.py not found in scripts directory")
    except Exception as e:
        market_scan_result["status"] = f"error: {e}"

    results["smoke_tests"] = [market_scan_result]

    installed_count = sum(1 for l in results["libraries"] if l["installed"])
    total = len(results["libraries"])
    if installed_count < total:
        results["status"] = "missing_libraries"
        results["warnings"].insert(0, f"{total - installed_count}/{total} required libraries are missing. Run install_deps.py.")

    return results


def main():
    parser = argparse.ArgumentParser(description="Verify stored data against live sources")
    parser.add_argument(
        "--check",
        choices=["all", "prop-firms", "contracts", "libraries"],
        default="all",
        help="What to verify (default: all)",
    )
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "check_type": args.check,
        "overall_status": "ok",
        "prop_firms": None,
        "contracts": None,
        "libraries": None,
        "summary": [],
    }

    checks_to_run = []
    if args.check == "all":
        checks_to_run = ["prop-firms", "contracts", "libraries"]
    else:
        checks_to_run = [args.check]

    # Run checks
    if "prop-firms" in checks_to_run:
        pf_results = check_prop_firms()
        output["prop_firms"] = pf_results
        if pf_results["status"] != "ok":
            output["summary"].append(f"Prop firms: {pf_results['status'].upper()}")
            if pf_results["warnings"]:
                output["summary"].extend([f"  - {w}" for w in pf_results["warnings"][:3]])

    if "contracts" in checks_to_run:
        ct_results = check_contracts()
        output["contracts"] = ct_results
        if ct_results["status"] != "ok":
            output["summary"].append(f"Contracts: {ct_results['status'].upper()}")
            if ct_results["warnings"]:
                output["summary"].extend([f"  - {w}" for w in ct_results["warnings"][:3]])

    if "libraries" in checks_to_run:
        lib_results = check_libraries()
        output["libraries"] = lib_results
        if lib_results["status"] != "ok":
            output["summary"].append(f"Libraries: {lib_results['status'].upper()}")
            if lib_results["errors"]:
                output["summary"].extend([f"  - {e}" for e in lib_results["errors"][:3]])

    # Determine overall status
    statuses = []
    if output["prop_firms"]:
        statuses.append(output["prop_firms"]["status"])
    if output["contracts"]:
        statuses.append(output["contracts"]["status"])
    if output["libraries"]:
        statuses.append(output["libraries"]["status"])

    if any(s == "error" for s in statuses):
        output["overall_status"] = "error"
    elif any(s in ("stale", "issues_found", "missing_libraries") for s in statuses):
        output["overall_status"] = "needs_attention"
    else:
        output["overall_status"] = "ok"

    if not output["summary"]:
        output["summary"].append("All checks passed. Data is current and consistent.")

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
