#!/usr/bin/env python3
"""Canon-Mnemonic-Guard Dashboard Generator.

Reads ~/.hermes/self-reflection/ data, generates a standalone HTML dashboard
with embedded JSON data. Output: canon-mnemonic-guard-dashboard.html on Desktop.

Usage: python3 generate-dashboard.py [--output path.html]
"""
import json, os, glob, yaml, sys
from datetime import datetime, timezone

SR = os.path.expanduser('~/.hermes/self-reflection')
OUTPUT = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--output' else os.path.expanduser('~/Desktop/canon-mnemonic-guard-dashboard.html')

# This is a bridge script — see ~/.hermes/dashboard/generate.py for the full generator.
# To develop the dashboard, edit that file; this script delegates to it.
generator = os.path.expanduser('~/.hermes/dashboard/generate.py')
if not os.path.exists(generator):
    print("ERROR: Dashboard generator not found at ~/.hermes/dashboard/generate.py")
    print("Run: mkdir -p ~/.hermes/dashboard && cp this file ~/.hermes/dashboard/generate.py")
    sys.exit(1)

import importlib.util
spec = importlib.util.spec_from_file_location("generate", generator)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
