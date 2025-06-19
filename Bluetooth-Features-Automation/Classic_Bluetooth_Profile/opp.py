import os
import subprocess
import re
from logger_mod import *

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
            channel = opp_section.group(1)
            log.debug(f"Found OPP channel: {channel}")
            return channel
        else:
            log.warning("Could not find OPP channel in SDP response.")
    except Exception as e:
        log.error(f"Failed to get OPP channel: {e}")
    return None

def send_file_via_opp(dest_address, file_path):
    """
    Sends a file via Bluetooth OPP to a paired and connected device.
    """
    try:
        log.info(f"Sending '{file_path}' to device: {dest_address}")

        if not os.path.isfile(file_path):
            log.error(f"File does not exist: {file_path}")
            return

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

        output = result.stdout.strip() + "\n" + result.stderr.strip()

        if "Sending" in output and "Disconnecting" in output:
            log.info("File sent successfully via OPP.")
            log.debug(f"Full obexftp output:\n{output}")
        else:
            log.error("File transfer may have failed.")
            log.error(f"obexftp output:\n{output}")

    except Exception as e:
        log.error(f"Exception during OPP file transfer: {e}")
