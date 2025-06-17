import subprocess
import time
from logger_mod import *

def connect_a2dp(device_mac):
    """
    Connect to Bluetooth device for A2DP.
    """
    try:
        log.info(f"Connecting to A2DP device: {device_mac}")
        subprocess.run(["bluetoothctl", "connect", device_mac], check=True)
        time.sleep(2)
        log.info(f"Successfully connected to {device_mac}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to connect to device: {device_mac}\n{e}")
        return False

def disconnect_a2dp(device_mac):
    """
    Disconnect from Bluetooth device.
    """
    try:
        log.info(f"Disconnecting from A2DP device: {device_mac}")
        subprocess.run(["bluetoothctl", "disconnect", device_mac], check=True)
        time.sleep(1)
        log.info(f"Disconnected from {device_mac}")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to disconnect from device: {device_mac}\n{e}")

def play_media():
    """
    Play media using playerctl (Linux only).
    """
    try:
        log.debug("Sending play command via playerctl...")
        subprocess.run(["playerctl", "play"], check=True)
        log.info("Media playback started.")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to play media.\n{e}")

def pause_media():
    """
    Pause media using playerctl.
    """
    try:
        log.debug("Sending pause command via playerctl...")
        subprocess.run(["playerctl", "pause"], check=True)
        log.info("Media paused.")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to pause media.\n{e}")

def skip_track():
    """
    Skip to the next media track.
    """
    try:
        log.debug("Sending next track command via playerctl...")
        subprocess.run(["playerctl", "next"], check=True)
        log.info("Skipped to next track.")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to skip track.\n{e}")

def simulate_call_interrupt():
    """
    Simulate a call interruption by pausing media, waiting, and resuming.
    """
    try:
        log.info("Simulating incoming call interruption...")
        pause_media()
        log.info("Simulating call duration...")
        time.sleep(5)  # Simulate 5-second call
        play_media()
        log.info("Resumed media after simulated call.")
    except Exception as e:
        log.error(f"Failed during call simulation.\n{e}")

def get_volume():
    """
    Get the current system volume (0-100 scale).
    """
    try:
        output = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode()
        # Output format: 'Volume: front-left: 65536 / 100% / 0.00 dB, ...'
        for line in output.splitlines():
            if "Volume:" in line:
                percent = line.split('/')[1].strip().replace('%', '')
                log.debug(f"Current system volume: {percent}%")
                return int(percent)
    except Exception as e:
        log.error(f"Failed to get volume: {e}")
        return 0  # Fallback default

def set_volume(level):
    """
    Set the system volume.
    Level is expected in range 0 to 10. It will be converted to 0-100%.
    """
    try:
        volume_percent = max(0, min(level * 10, 100))  # Clamp between 0-100
        log.debug(f"Setting system volume to {volume_percent}%")
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{volume_percent}%"], check=True)
        log.info(f"System volume set to {volume_percent}%")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to set volume.\n{e}")

def previous_track():
    """
    Go to the previous media track.
    """
    try:
        log.debug("Sending previous track command via playerctl...")
        subprocess.run(["playerctl", "previous"], check=True)
        log.info("Went to previous track.")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to go to previous track.\n{e}")



