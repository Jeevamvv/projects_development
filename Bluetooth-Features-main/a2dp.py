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
