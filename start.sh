#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # Find the absolute folder
LOGFILE="$SCRIPT_DIR/sfc_scheduler.log"                      # For error message

while true; do
    python3 "$SCRIPT_DIR/tuo_script.py" >> "$LOGFILE" 2>&1
done
