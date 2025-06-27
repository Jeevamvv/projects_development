# hfp.py

import subprocess
import time
import logging
from logger_mod import *

# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

# Modify this to match your RFCOMM port
RFCOMM_PORT = "/dev/rfcomm0"

# Utility function to run Linux commands
def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log.error(f"Command failed: {cmd}\nError: {e.stderr}")
        return None

# Utility function to send AT commands to phone
def send_at_command(at_cmd):
    try:
        with open(RFCOMM_PORT, 'w') as rfcomm:
            rfcomm.write(at_cmd + '\r')
        log.info(f"📡 Sent AT command: {at_cmd}")
    except Exception as e:
        log.error(f"Failed to send AT command: {e}")

# 1. Connect and play music
def connect_and_play_music():
    log.info("🔗 Connecting to device and playing music via A2DP...")
    # Replace with your device MAC address
    run_command("bluetoothctl connect D4:CB:CC:86:9D:8C")
    time.sleep(2)
    run_command("playerctl play")
    log.info("🎵 Music playback started")

# 2. Incoming Call ➝ Accept
def incoming_call_accept():
    log.info("📞 Accepting incoming call...")
    send_at_command("ATA")
    log.info("✅ Call accepted")

# 3. Incoming Call ➝ Reject
def incoming_call_reject():
    log.info("📞 Rejecting incoming call...")
    send_at_command("AT+CHUP")
    log.info("❌ Call rejected")

# 4. Three-Way Calling
def three_way_calling():
    log.info("📞 Handling three-way call scenario...")
    send_at_command("AT+CHLD=1")  # End active, accept held
    time.sleep(1)
    send_at_command("AT+CHLD=2")  # Hold active, accept other
    time.sleep(1)
    log.info("🔁 Switched between calls")

# 5. Reject Incoming Call Without Accepting
def reject_without_accepting():
    log.info("📵 Rejecting incoming call directly...")
    send_at_command("AT+CHUP")
    log.info("❌ Call rejected directly")

# 6. Outgoing Call ➝ Then Hold
def outgoing_call_then_hold():
    log.info("📲 Dialing outgoing call and putting on hold...")
    send_at_command("ATD1234567890;")  # Replace with test number
    time.sleep(3)
    send_at_command("AT+CHLD=2")  # Hold active call
    log.info("📴 Outgoing call held")

# 7. Outgoing Call ➝ Airplane Mode
def outgoing_call_airplane_mode():
    log.info("📲 Dialing call and simulating airplane mode...")
    send_at_command("ATD1234567890;")
    time.sleep(2)
    log.warning("⚠️ Simulate turning on airplane mode on phone")
    time.sleep(3)
    log.info("📵 Airplane mode enabled (call dropped)")

# 8. Call Ongoing ➝ Incoming ➝ Reject
def call_ongoing_incoming_reject():
    log.info("📞 Making outgoing call and rejecting second incoming...")
    send_at_command("ATD1234567890;")
    time.sleep(3)
    log.info("📲 Simulate second incoming call on mobile now...")
    time.sleep(2)
    send_at_command("AT+CHLD=0")  # Reject held call
    log.info("❌ Second call rejected")

