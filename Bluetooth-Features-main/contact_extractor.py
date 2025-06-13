# import os
# import subprocess
# import openpyxl
# #from logger_mod import setup_logger
# from datetime import datetime


# from logger_mod import Logger
# log = Logger().setup_logger()

# def fetch_contacts_and_save_to_excel(bt_address):
#     try:
#         contact_vcf = "/tmp/contacts.vcf"
#         log.info(f"Pulling contacts from device {bt_address}")

#         # Use obexftp to fetch vcf via PBAP - adjust folder if needed
#         result = subprocess.run([
#             "obexftp", "--nopath", "--noconn", "--uuid", "PBAP",
#             "--bluetooth", bt_address, "--channel", "9",  # 9 is often PBAP
#             "--get", "telecom/pb.vcf"
#         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         if result.returncode != 0:
#             log.error(f"Failed to fetch contacts: {result.stderr.decode()}")
#             return

#         # Save pulled contact file
#         with open(contact_vcf, "wb") as f:
#             f.write(result.stdout)

#         log.info("Parsing VCF and writing to Excel...")
#         save_to_excel(contact_vcf, bt_address)

#     except Exception as e:
#         log.exception(f"Error fetching contacts: {e}")

# def save_to_excel(vcf_path, device_name):
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.title = "Phone Contacts"
#     ws.append(["Name", "Number"])

#     with open(vcf_path, "r") as file:
#         name, number = "", ""
#         for line in file:
#             if line.startswith("FN:"):
#                 name = line.strip().replace("FN:", "")
#             elif line.startswith("TEL:"):
#                 number = line.strip().replace("TEL:", "")
#                 ws.append([name, number])

#     filename = f"Phone_Contacts_{device_name.replace(':', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
#     wb.save(filename)
#     log.info(f"Saved contacts to {filename}")



# def get_connected_device_address():
#     """
#     Checks for the currently connected Bluetooth device using bluetoothctl.
#     Returns the MAC address of the connected device, or None if not found.
#     """
#     try:
#         # Get list of paired devices
#         result = subprocess.run(
#             ["bluetoothctl", "paired-devices"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         devices = [line.split()[1] for line in result.stdout.splitlines() if line.startswith("Device")]

#         # Check each paired device for connection status
#         for device in devices:
#             info = subprocess.run(
#                 ["bluetoothctl", "info", device],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )
#             if "Connected: yes" in info.stdout:
#                 log.info(f"Connected device detected: {device}")
#                 return device

#         log.warning("No connected Bluetooth device found.")
#         return None

#     except Exception as e:
#         log.exception(f"Error while detecting connected Bluetooth device: {e}")
#         return None





###############################################





import os
import subprocess
import openpyxl
from datetime import datetime
from logger_mod import Logger

log = Logger().setup_logger()

def fetch_contacts_and_save_to_excel(bt_address):
    try:
        contact_vcf = "/tmp/contacts.vcf"
        log.info(f"Pulling contacts from device {bt_address}")

        # Corrected: Use channel 19 (you saw it in the scan), and don't specify UUID
        result = subprocess.run([
            "obexftp", "--nopath", "--noconn",
            "--bluetooth", bt_address,
            "--channel", "19",  # Use channel from SDP info
            "--get", "telecom/pb.vcf"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            log.error(f"Failed to fetch contacts: {result.stderr.decode()}")
            return

        # Save contact file
        with open(contact_vcf, "wb") as f:
            f.write(result.stdout)

        log.info("Parsing VCF and writing to Excel...")
        save_to_excel(contact_vcf, bt_address)

    except Exception as e:
        log.exception(f"Error fetching contacts: {e}")

def save_to_excel(vcf_path, device_name):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Phone Contacts"
    ws.append(["Name", "Number"])

    with open(vcf_path, "r") as file:
        name, number = "", ""
        for line in file:
            if line.startswith("FN:"):
                name = line.strip().replace("FN:", "")
            elif line.startswith("TEL:"):
                number = line.strip().replace("TEL:", "")
                ws.append([name, number])

    filename = f"Phone_Contacts_{device_name.replace(':', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb.save(filename)
    log.info(f"Saved contacts to {filename}")

def get_connected_device_address():
    try:
        result = subprocess.run(
            ["bluetoothctl", "paired-devices"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        devices = [line.split()[1] for line in result.stdout.splitlines() if line.startswith("Device")]

        for device in devices:
            info = subprocess.run(
                ["bluetoothctl", "info", device],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if "Connected: yes" in info.stdout:
                log.info(f"Connected device detected: {device}")
                return device

        log.warning("No connected Bluetooth device found.")
        return None

    except Exception as e:
        log.exception(f"Error while detecting connected Bluetooth device: {e}")
        return None
