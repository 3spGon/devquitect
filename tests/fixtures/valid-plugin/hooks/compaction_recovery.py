#!/usr/bin/env python3
"""Fixture hook handler."""

import json
import sys

if __name__ == "__main__":
    json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart"}}, sys.stdout)
