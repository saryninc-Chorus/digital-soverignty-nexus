import time
import subprocess
import os
from datetime import datetime

# --- CONFIGURATION ---
TARGET_SCRIPT = "oracle_gui.py"
LOG_FILE = "daisy_incident_log.txt"
CHECK_INTERVAL = 5 # Seconds

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [DAISY GUARDIAN] {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def start_oracle():
    log_event(f"Initializing {TARGET_SCRIPT}...")
    # This starts the Oracle in the background
    return subprocess.Popen(["streamlit", "run", TARGET_SCRIPT])

def monitor():
    log_event("🛡️ GUARDIAN PROTOCOL ACTIVE. Watching the Oracle...")
    process = start_oracle()

    while True:
        # Check if the Oracle is still breathing
        if process.poll() is not None:
            # The process has died.
            log_event("⚠️ ALERT: Oracle Process Terminated (Entropy Spike).")
            log_event("♻️ ACTION: Executing Resurrection Protocol...")
            
            # Restart immediately
            process = start_oracle()
            log_event("✅ STATUS: Oracle Restored.")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        log_event("Guardian Deactivated by Sovereign Command.")
