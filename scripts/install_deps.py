#!/usr/bin/env python3
"""
install_deps.py - Install required packages for Futures Edge skill.
For each package, tries importing first; if ImportError, pip installs it.
Outputs JSON status report to stdout.
"""

import sys
import os
import json
import subprocess
import importlib

# Force UTF-8 for smartmoneyconcepts unicode star character
os.environ["PYTHONIOENCODING"] = "utf-8"

PACKAGES = [
    {"import_name": "tradingview_screener", "pip_name": "tradingview-screener"},
    {"import_name": "tvDatafeed", "pip_name": "git+https://github.com/rongardF/tvdatafeed.git", "pip_display": "tvdatafeed (from GitHub)"},
    {"import_name": "backtesting", "pip_name": "backtesting"},
    {"import_name": "smartmoneyconcepts", "pip_name": "smartmoneyconcepts", "extra_flags": ["--no-deps"]},
    {"import_name": "pandas", "pip_name": "pandas"},
    {"import_name": "numpy", "pip_name": "numpy"},
]


class SafeJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles special types."""
    def default(self, obj):
        try:
            import numpy as np
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
        except ImportError:
            pass
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return super().default(obj)


def check_and_install(pkg):
    """Try importing; if that fails, pip install and retry."""
    import_name = pkg["import_name"]
    pip_name = pkg["pip_name"]
    display_name = pkg.get("pip_display", pip_name)
    result = {
        "package": display_name,
        "import_name": import_name,
        "already_installed": False,
        "installed": False,
        "version": None,
        "error": None,
    }

    # First try importing
    try:
        mod = importlib.import_module(import_name)
        result["already_installed"] = True
        result["installed"] = True
        version = getattr(mod, "__version__", None)
        if version:
            result["version"] = str(version)
        return result
    except ImportError:
        pass

    # Not installed -- pip install it
    try:
        cmd = [sys.executable, "-m", "pip", "install"]
        extra_flags = pkg.get("extra_flags", [])
        cmd.extend(extra_flags)
        cmd.append(pip_name)
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if proc.returncode != 0:
            result["error"] = proc.stderr.strip() or proc.stdout.strip()
            return result

        # Verify the import now works
        importlib.invalidate_caches()
        mod = importlib.import_module(import_name)
        result["installed"] = True
        version = getattr(mod, "__version__", None)
        if version:
            result["version"] = str(version)
    except subprocess.TimeoutExpired:
        result["error"] = "pip install timed out after 120 seconds"
    except ImportError as e:
        result["error"] = f"pip install succeeded but import still fails: {e}"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    output = {
        "status": "ok",
        "python_version": sys.version,
        "python_executable": sys.executable,
        "packages": [],
        "summary": {"total": len(PACKAGES), "success": 0, "failed": 0, "already_installed": 0},
    }

    for pkg in PACKAGES:
        res = check_and_install(pkg)
        output["packages"].append(res)
        if res["installed"]:
            output["summary"]["success"] += 1
            if res["already_installed"]:
                output["summary"]["already_installed"] += 1
        else:
            output["summary"]["failed"] += 1

    if output["summary"]["failed"] > 0:
        output["status"] = "partial_failure"

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
