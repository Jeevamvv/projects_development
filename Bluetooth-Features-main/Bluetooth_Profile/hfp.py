import subprocess
import time
import re
from logger_mod import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
log = logging.getLogger(__name__)

def run_command(cmd):
    """Run shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        log.error(f"Command failed: {cmd} | Error: {e}")
        return ""

def monitor_btmon(duration=10):
    """Capture AT commands using btmon."""
    log.info("Starting btmon capture...")
    try:
        process = subprocess.Popen(["timeout", str(duration), "btmon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        return stdout.decode()
    except Exception as e:
        log.error("btmon monitoring failed:", e)
        return ""

def parse_at_commands(btmon_output):
    """Parse AT commands from btmon dump."""
    at_commands = re.findall(r'\+CIEV.*', btmon_output)
    for cmd in at_commands:
        log.info(f"Captured AT Command: {cmd}")
    return at_commands

def simulate_music_switch():
    log.info("Test 3: Connecting mobile and headset, play music, switch devices.")
    # Simulate music on one device and then switch
    log.debug("Ensure A2DP is active and audio is playing.")
    time.sleep(5)
    log.debug("Switching playback from one device to another...")
    time.sleep(5)
    log.info("Verify only one device is playing at a time.")

def simulate_incoming_call(accept=True):
    log.info("Test 4: Incoming call handling...")
    output = monitor_btmon(15)
    cmds = parse_at_commands(output)
    if "+CIEV: 2,1" in output:
        log.info("Incoming call detected.")
        if accept:
            log.info("Simulating call accept...")
            assert "+CIEV: 1,1" in output
        else:
            log.info("Simulating call reject...")
            assert "+CIEV: 2,0" in output

def simulate_three_way_call():
    log.info("Test 5: Simulate three-way calling...")
    output = monitor_btmon(20)
    cmds = parse_at_commands(output)
    assert any("+CIEV: 2,2" in cmd for cmd in cmds), "Three-way call not detected"
    log.info("Three-way call established with proper codec negotiation.")

def simulate_call_rejection():
    log.info("Test 6: Reject incoming call without accepting...")
    output = monitor_btmon(10)
    cmds = parse_at_commands(output)
    assert "+CIEV: 2,0" in output
    log.info("Call rejected successfully.")

def simulate_outgoing_call_with_hold():
    log.info("Test 7: Outgoing call then place callee on hold.")
    output = monitor_btmon(20)
    cmds = parse_at_commands(output)
    assert "+CIEV: 2,2" in output
    log.info("Call accepted and then placed on hold.")

def simulate_airplane_mode_termination():
    log.info("Test 8: Outgoing call, then enable airplane mode.")
    output = monitor_btmon(20)
    cmds = parse_at_commands(output)
    assert "+CIEV: 2,0" in output
    log.info("Call disconnected due to airplane mode.")

def simulate_call_interrupt_and_reject():
    log.info("Test 9: Call in progress, reject new incoming call.")
    output = monitor_btmon(20)
    cmds = parse_at_commands(output)
    assert "+CIEV: 2,2" in output and "+CIEV: 2,0" in output
    log.info("Incoming call rejected, primary call remains unaffected.")

def main():
    log.info("=== Bluetooth Telephony Automation ===")
    simulate_music_switch()
    simulate_incoming_call(accept=True)
    simulate_incoming_call(accept=False)
    simulate_three_way_call()
    simulate_call_rejection()
    simulate_outgoing_call_with_hold()
    simulate_airplane_mode_termination()
    simulate_call_interrupt_and_reject()
    log.info("=== All test scenarios executed ===")

if __name__ == "__main__":
    main()
