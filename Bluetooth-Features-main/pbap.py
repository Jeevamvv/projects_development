# pbap.py
import os
import subprocess
import re
import csv
from openpyxl import Workbook
from logger_mod import *

def fetch_contacts(device_address, output_path="contacts.xlsx"):
    """
    Fetches contacts from a Bluetooth device using PBAP and saves to an Excel file.
    """
    try:
        log.info(f"Fetching contacts from {device_address}")
        
        # Use obexftp or custom pbap client to pull vcf contact file (simulated here)
        vcf_path = "/tmp/contacts.vcf"
        pull_cmd = [
            "obexftp",
            "--bluetooth", device_address,
            "--channel", "9",  # Default PBAP channel (may vary)
            "--get", "telecom/pb.vcf"
        ]
        result = subprocess.run(pull_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            log.error(f"Failed to pull contact file: {result.stderr}")
            return False

        log.info("Successfully pulled vCard file. Parsing...")
        return parse_and_save_contacts(vcf_path, output_path)

    except Exception as e:
        log.error(f"Exception during contact fetch: {e}")
        return False


def parse_and_save_contacts(vcf_path, output_path):
    """
    Parses a vCard file and saves contacts (name + number) to Excel.
    """
    if not os.path.exists(vcf_path):
        log.error("vCard file not found.")
        return False

    contacts = []

    with open(vcf_path, 'r') as file:
        name, number = None, None
        for line in file:
            line = line.strip()
            if line.startswith("FN:"):
                name = line[3:]
            elif line.startswith("TEL:") or "TEL;" in line:
                number = re.sub(r"TEL.*?:", "", line)
                if name and number:
                    contacts.append((name, number))
                    name, number = None, None

    if not contacts:
        log.warning("No contacts found.")
        return False

    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Number"])
    for name, number in contacts:
        ws.append([name, number])
    
    wb.save(output_path)
    log.info(f"Contacts saved to {output_path}")
    return True
