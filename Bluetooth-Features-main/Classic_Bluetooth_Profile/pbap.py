#!/usr/bin/env python3
"""
PBAP (Phone Book Access Profile) contact fetcher using obexftp and sdptool.
"""

import subprocess
import os
import pandas as pd
from logger_mod import *

def parse_vcf(vcf_file):
    """Basic VCF parser: extract names and numbers from .vcf file."""
    names = []
    numbers = []
    with open(vcf_file, 'r') as f:
        contact = {}
        for line in f:
            line = line.strip()
            if line.startswith("FN:"):
                contact["FN"] = line[3:]
            elif line.startswith("TEL"):
                contact["TEL"] = line.split(":")[-1]
            elif line == "END:VCARD":
                names.append(contact.get("FN", ""))
                numbers.append(contact.get("TEL", ""))
                contact = {}
    return names, numbers

def fetch_contacts(bt_address, output_excel):
    """
    Fetch PBAP contacts using obexftp and export to Excel.
    """
    try:
        log.info(f"📞 Starting PBAP contact fetch from device {bt_address}")

        tmp_dir = "/tmp/pbap_contacts"
        os.makedirs(tmp_dir, exist_ok=True)
        os.chdir(tmp_dir)

        # STEP 1: Get PBAP channel using sdptool
        log.info("🔍 Discovering PBAP channel using sdptool...")
        result = subprocess.run(["sdptool", "browse", bt_address], capture_output=True, text=True)
        pbap_channel = None
        pbap_found = False  # ✅ Fix for UnboundLocalError
        for line in result.stdout.splitlines():
            if "Phonebook Access" in line:
                pbap_found = True
            if pbap_found and "Channel:" in line:
                pbap_channel = line.strip().split()[-1]
                break

        if not pbap_channel:
            log.error("❌ Could not find PBAP channel on the device.")
            return False

        log.info(f"✅ PBAP channel found: {pbap_channel}")

        # STEP 2: Fetch pb.vcf using obexftp
        vcf_file_path = os.path.join(tmp_dir, "pb.vcf")
        if os.path.exists(vcf_file_path):
            os.remove(vcf_file_path)

        log.info("📂 Fetching pb.vcf from telecom folder...")
        result = subprocess.run([
            "obexftp",
            "--nopath",
            "--noconn",
            "--uuid", "none",
            "--bluetooth", bt_address,
            "--channel", pbap_channel,
            "--get", "telecom/pb.vcf"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            log.error(f"❌ Failed to fetch pb.vcf:\n{result.stderr}")
            return False

        if not os.path.exists(vcf_file_path):
            log.error("❌ pb.vcf not found after fetch.")
            return False

        # STEP 3: Parse and export to Excel
        names, numbers = parse_vcf(vcf_file_path)
        df = pd.DataFrame({"Name": names, "Number": numbers})
        df.to_excel(output_excel, index=False)
        log.info(f"✅ Exported {len(df)} contacts to {output_excel}")
        return True

    except Exception as e:
        log.exception("❌ Exception in fetch_contacts: " + str(e))
        return False
