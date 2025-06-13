
import os
import subprocess
import re
from logger_mod import Logger

log = Logger().setup_logger()

def get_opp_channel(address):
    try:
        result = subprocess.run(
            ["sdptool", "browse", address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        opp_section = re.search(r"Service Name: OBEX Object Push.*?Channel: (\d+)", result.stdout, re.DOTALL)
        if opp_section:
            return opp_section.group(1)
    except Exception as e:
        log.error(f"Failed to get OPP channel: {e}")
    return None

def send_file_via_opp(dest_address, file_path):
    """
    Sends a file via Bluetooth OPP to a paired and connected device.
    """
    try:
        log.info(f"Sending '{file_path}' to device: {dest_address}")

        channel = get_opp_channel(dest_address)
        if not channel:
            log.error("Could not determine OBEX OPP channel from device.")
            return

        result = subprocess.run(
            ['obexftp', '--nopath', '--noconn', '--uuid', 'none',
             '--bluetooth', dest_address, '--channel', channel, '--put', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            log.info("File sent successfully via OPP.")
        else:
            log.error(f"File transfer failed with error: {result.stderr.strip()}")

    except Exception as e:
        log.error(f"Exception during OPP file transfer: {e}")
