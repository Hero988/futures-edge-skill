"""
Sound notification system for Futures Edge autopilot.
Uses winsound (Python stdlib on Windows) — zero dependencies.

Usage:
    python notify_sound.py --event trade_signal
    python notify_sound.py --event t1_hit
    python notify_sound.py --event close_warning
    python notify_sound.py --event kill_switch
    python notify_sound.py --event action_needed

Events:
    trade_signal   - EMA crossover detected, trade plan ready (plays 3x chime)
    t1_hit         - T1/T2 target reached, user action needed
    close_warning  - <30 min until close deadline
    kill_switch    - Kill switch activated or critical error
    action_needed  - Generic "look at the screen" notification
    scan_quiet     - No signal (silent — no sound)
"""

import sys
import argparse
import winsound
import time
import os

SOUNDS = {
    "trade_signal": {
        "file": r"C:\Windows\Media\Windows Notify Calendar.wav",
        "repeat": 3,
        "delay": 0.4,
        "fallback_alias": "SystemExclamation",
    },
    "t1_hit": {
        "file": r"C:\Windows\Media\tada.wav",
        "repeat": 2,
        "delay": 0.3,
        "fallback_alias": "SystemAsterisk",
    },
    "close_warning": {
        "file": r"C:\Windows\Media\Windows Exclamation.wav",
        "repeat": 2,
        "delay": 0.5,
        "fallback_alias": "SystemExclamation",
    },
    "kill_switch": {
        "file": r"C:\Windows\Media\Windows Critical Stop.wav",
        "repeat": 3,
        "delay": 0.3,
        "fallback_alias": "SystemHand",
    },
    "action_needed": {
        "file": r"C:\Windows\Media\Windows Notify Email.wav",
        "repeat": 2,
        "delay": 0.4,
        "fallback_alias": "SystemExclamation",
    },
    "scan_quiet": None,
}


def play_sound(event: str):
    if event == "scan_quiet" or event not in SOUNDS or SOUNDS[event] is None:
        return

    config = SOUNDS[event]
    sound_file = config["file"]
    repeat = config["repeat"]
    delay = config["delay"]

    for i in range(repeat):
        try:
            if os.path.exists(sound_file):
                winsound.PlaySound(sound_file, winsound.SND_FILENAME)
            else:
                winsound.PlaySound(config["fallback_alias"], winsound.SND_ALIAS)
        except Exception:
            try:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except Exception:
                pass
        if i < repeat - 1:
            time.sleep(delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play trading notification sounds")
    parser.add_argument("--event", required=True, choices=list(SOUNDS.keys()),
                        help="Event type to play sound for")
    args = parser.parse_args()
    play_sound(args.event)
    print(f"SOUND:{args.event}")
