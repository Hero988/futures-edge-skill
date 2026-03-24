#!/usr/bin/env python3
"""
extract_tv_token.py - Log into TradingView via Playwright and extract auth_token.

Run once to get the token, which is saved to config.json for use by autopilot_scan.py.
The token typically lasts weeks/months before expiring.

Usage:
    python extract_tv_token.py
    python extract_tv_token.py --headless    (no browser window)
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path


def extract_token(headless=False):
    from playwright.sync_api import sync_playwright

    config_path = Path(__file__).resolve().parent.parent / "diary" / "config.json"
    if not config_path.exists():
        print("ERROR: config.json not found. Run first-time setup first.")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    username = config.get("tradingview_username")
    password = config.get("tradingview_password")
    if not username or not password:
        print("ERROR: TradingView credentials not found in config.json")
        sys.exit(1)

    print(f"Logging into TradingView as '{username}'...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Go to TradingView sign-in page
        page.goto("https://www.tradingview.com/#signin", wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Click "Email" tab if visible (TV shows social login buttons first)
        try:
            # Look for the email sign-in option
            email_buttons = page.locator("button, span, div").filter(has_text=re.compile(r"^Email$", re.IGNORECASE))
            if email_buttons.count() > 0:
                email_buttons.first.click()
                time.sleep(1)
        except Exception:
            pass

        # Try to find and fill the username field
        try:
            # TradingView uses various selectors for the login form
            username_field = page.locator('input[name="id_username"], input[name="username"], input[type="email"], input[type="text"][autocomplete="username"]').first
            username_field.fill(username)
            time.sleep(0.5)

            password_field = page.locator('input[name="id_password"], input[name="password"], input[type="password"]').first
            password_field.fill(password)
            time.sleep(0.5)

            # Click sign in button
            submit = page.locator('button[type="submit"], button[data-overflow-tooltip-text*="Sign"]').first
            submit.click()
            time.sleep(5)

        except Exception as e:
            print(f"Login form interaction failed: {e}")
            print("Trying alternative login flow...")

            # Alternative: direct POST login
            page.goto("https://www.tradingview.com/accounts/signin/", wait_until="networkidle", timeout=15000)
            time.sleep(2)

            for inp in page.locator("input").all():
                inp_type = inp.get_attribute("type") or ""
                inp_name = inp.get_attribute("name") or ""
                if inp_type == "text" or "user" in inp_name.lower() or "email" in inp_name.lower():
                    inp.fill(username)
                elif inp_type == "password":
                    inp.fill(password)

            page.locator("button[type='submit']").first.click()
            time.sleep(5)

        # Wait for login to complete - check for avatar or user menu
        print("Waiting for login to complete...")
        for _ in range(15):
            # Check if we're logged in by looking at page content
            content = page.content()
            if "auth_token" in content:
                break
            # Check cookies for sessionid
            cookies = context.cookies()
            session_cookies = [c for c in cookies if c["name"] == "sessionid" and "tradingview" in c.get("domain", "")]
            if session_cookies:
                break
            time.sleep(2)

        # Method 1: Extract auth_token from page source
        auth_token = None
        content = page.content()

        # Search for auth_token in script tags
        token_match = re.search(r'"auth_token"\s*:\s*"([^"]+)"', content)
        if token_match:
            auth_token = token_match.group(1)
            print(f"Found auth_token in page source: {auth_token[:20]}...")

        # Method 2: Try JavaScript evaluation
        if not auth_token:
            try:
                auth_token = page.evaluate("() => { try { return window.__initialData__?.user?.auth_token || null; } catch(e) { return null; } }")
                if auth_token:
                    print(f"Found auth_token via JS: {auth_token[:20]}...")
            except Exception:
                pass

        # Method 3: Navigate to a page that exposes the token
        if not auth_token:
            try:
                page.goto("https://www.tradingview.com/chart/", wait_until="networkidle", timeout=30000)
                time.sleep(3)
                content = page.content()
                token_match = re.search(r'"auth_token"\s*:\s*"([^"]+)"', content)
                if token_match:
                    auth_token = token_match.group(1)
                    print(f"Found auth_token on chart page: {auth_token[:20]}...")
            except Exception:
                pass

        # Method 4: Extract sessionid cookie (can be used as alternative auth)
        sessionid = None
        cookies = context.cookies()
        for c in cookies:
            if c["name"] == "sessionid" and "tradingview" in c.get("domain", ""):
                sessionid = c["value"]
                print(f"Found sessionid cookie: {sessionid[:20]}...")

        browser.close()

    if not auth_token and not sessionid:
        print("\nERROR: Could not extract auth_token or sessionid.")
        print("This usually means login failed (CAPTCHA, 2FA, or wrong credentials).")
        print("\nManual extraction:")
        print("1. Open TradingView in Chrome and log in")
        print("2. Press F12 (DevTools) > Application > Cookies > tradingview.com")
        print("3. Find 'sessionid' cookie and copy its value")
        print("4. Run: python extract_tv_token.py --manual-session YOUR_SESSION_ID")
        sys.exit(1)

    # Save to config
    if auth_token:
        config["tradingview_auth_token"] = auth_token
        print(f"\nauth_token saved to config.json")
    if sessionid:
        config["tradingview_sessionid"] = sessionid
        print(f"sessionid saved to config.json")

    config["token_extracted_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("\nDone! autopilot_scan.py will now use authenticated data.")
    return auth_token or sessionid


def manual_session(session_id):
    """Save a manually extracted sessionid."""
    config_path = Path(__file__).resolve().parent.parent / "diary" / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    config["tradingview_sessionid"] = session_id
    config["token_extracted_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"sessionid saved to config.json: {session_id[:20]}...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--manual-session", type=str, help="Manually provide sessionid cookie value")
    args = parser.parse_args()

    if args.manual_session:
        manual_session(args.manual_session)
    else:
        extract_token(headless=args.headless)
