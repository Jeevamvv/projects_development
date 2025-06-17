# pbap.py
import os
import subprocess
import xml.etree.ElementTree as ET
import pandas as pd
from logger_mod import *

def fetch_contacts(bt_address, output_excel):
    """
    Fetch contact list via PBAP and export to Excel file.
    """
    try:
        log.info(f"Starting PBAP contact fetch from device {bt_address}")

        # Mount OBEX FTP (simulate PBAP using obexftp or similar tool)
        # You might need to install obexftp: sudo apt-get install obexftp

        # Create temp vcf directory
        tmp_dir = "/tmp/pbap_contacts"
        os.makedirs(tmp_dir, exist_ok=True)

        # Try fetching phonebook.vcf via obexftp
        # You must be already connected and paired with the device
        result = subprocess.run([
            "obexftp", "--nopath", "--noconn", "--uuid", "PBAP",
            "--bluetooth", bt_address, "--channel", "9",  # Channel may vary
            "--get", "telecom/pb.vcf"
        ], cwd=tmp_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            log.error("Failed to fetch phonebook.vcf: " + result.stderr)
            return False

        # Parse the vCard file
        vcf_path = os.path.join(tmp_dir, "pb.vcf")
        if not os.path.exists(vcf_path):
            log.error("pb.vcf not found after fetch.")
            return False

        names = []
        numbers = []

        with open(vcf_path, "r") as f:
            name = ""
            number = ""
            for line in f:
                if line.startswith("FN:"):
                    name = line.strip().replace("FN:", "")
                elif line.startswith("TEL"):
                    number = line.split(":")[1].strip()
                    names.append(name)
                    numbers.append(number)

        # Save to Excel
        df = pd.DataFrame({"Name": names, "Number": numbers})
        df.to_excel(output_excel, index=False)
        log.info(f"Exported {len(df)} contacts to {output_excel}")
        return True

    except Exception as e:
        log.exception("Exception in fetch_contacts: " + str(e))
        return False
