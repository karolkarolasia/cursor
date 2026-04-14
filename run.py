#!/usr/bin/env python3
"""Entry point: python run.py <tool> [json_params]"""
import sys
from core.runner import run_cli

if __name__ == "__main__":
    sys.exit(run_cli())
