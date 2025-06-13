
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


# import os
# import subprocess
# import re
# from logger_mod import Logger

# log = Logger().setup_logger()

# def get_opp_channel(address):
#     try:
#         result = subprocess.run(
#             ["sdptool", "browse", address],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         log.debug(f"SDP browse output:\n{result.stdout}")  # New log for troubleshooting

#         # Updated regex for better match (case insensitive and spacing tolerant)
#         match = re.search(r"Service Name:\s*OBEX Object Push.*?Channel:\s*(\d+)", result.stdout, re.IGNORECASE | re.DOTALL)
#         if match:
#             channel = match.group(1)
#             log.debug(f"Found OPP channel: {channel}")
#             return channel
#         else:
#             log.warning("Could not find OPP channel in SDP response.")
#     except Exception as e:
#         log.error(f"Failed to get OPP channel: {e}")
#     return None


# def send_file_via_opp(dest_address, file_path):
#     try:
#         log.info(f"Sending '{file_path}' to device: {dest_address}")
#         if not os.path.isfile(file_path):
#             log.error(f"File does not exist: {file_path}")
#             return False

#         channel = get_opp_channel(dest_address)
#         if not channel:
#             log.error("Could not determine OBEX OPP channel from device.")
#             return False

#         result = subprocess.run(
#             ['obexftp', '--nopath', '--noconn', '--uuid', 'none',
#              '--bluetooth', dest_address, '--channel', channel, '--put', file_path],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         output = result.stdout.strip() + "\n" + result.stderr.strip()

#         if "Sending" in output and "Disconnecting" in output:
#             log.info("File sent successfully via OPP.")
#             log.debug(f"Full obexftp output:\n{output}")
#             return True
#         else:
#             log.error("File transfer may have failed.")
#             log.error(f"obexftp output:\n{output}")
#             return False

#     except Exception as e:
#         log.error(f"Exception during OPP file transfer: {e}")
#         return False

# # ---------------- TEST CASES ----------------
# def test_case_1(address):
#     file_path = input("Enter path of file to send (e.g. /home/user/test.txt): ").strip()
#     send_file_via_opp(address, file_path)

# def test_case_2(address):
#     file_path = input("Enter path of unsupported file (e.g. /home/user/test.sh): ").strip()
#     send_file_via_opp(address, file_path)

# def test_case_3(address):
#     file_path = input("Enter path of large file (>10MB): ").strip()
#     send_file_via_opp(address, file_path)

# def test_case_4(address):
#     file_path = input("Enter file to send and manually cancel transfer from mobile: ").strip()
#     send_file_via_opp(address, file_path)
#     print("➡ Please manually cancel transfer on mobile and observe result.")

# def test_case_5(address):
#     print("➡ Ensure device is NOT paired before testing.")
#     file_path = input("Enter file path to test sending without pairing: ").strip()
#     send_file_via_opp(address, file_path)

# def test_case_6(address):
#     print("➡ Ensure mobile storage is full before testing.")
#     file_path = input("Enter file to send when storage is full: ").strip()
#     send_file_via_opp(address, file_path)

# def test_case_7(address):
#     print("➡ Disable file sharing/receiving on phone before testing.")
#     file_path = input("Enter file path to send: ").strip()
#     send_file_via_opp(address, file_path)

# # ---------------- MAIN MENU ----------------
# def main():
#     print("\U0001F4C2 Bluetooth OPP Test Cases")
#     address = input("Enter destination Bluetooth MAC address (e.g. D4:CB:CC:86:9D:8C): ").strip()

#     test_cases = {
#         "1": ("Send normal file", test_case_1),
#         "2": ("Send unsupported file type", test_case_2),
#         "3": ("Send large file >10MB", test_case_3),
#         "4": ("Cancel transfer midway (manual)", test_case_4),
#         "5": ("Send without pairing", test_case_5),
#         "6": ("Send when storage is full", test_case_6),
#         "7": ("Send when OPP is disabled", test_case_7)
#     }

#     while True:
#         print("\nSelect Test Case:")
#         for key, (desc, _) in test_cases.items():
#             print(f"  {key}. {desc}")
#         print("  q. Quit")

#         choice = input("Enter choice: ").strip()
#         if choice == 'q':
#             break
#         elif choice in test_cases:
#             print(f"\nRunning: {test_cases[choice][0]}")
#             test_cases[choice][1](address)
#         else:
#             print("Invalid choice. Try again.")

# if __name__ == "__main__":
#     main()
