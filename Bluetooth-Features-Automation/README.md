
---

# 🔵 Bluetooth-Features Automation Suite

This project is a comprehensive automation suite for testing **Bluetooth features**, including both **Classic Bluetooth** and **Bluetooth Low Energy (BLE)** profiles. It automates testing of key Bluetooth profiles such as A2DP, HFP, OPP, and PBAP, along with utilities for GAP operations, logging, and execution flow control.

---

## 📁 Project Structure

```
Bluetooth-Features/
├── Bluetooth_Low_Energy/          # (Placeholder) Scripts related to BLE testing
├── BT_logs/                       # Stores captured Bluetooth logs (e.g., btmon, hcidump)
├── Classic_Bluetooth_Profile/     # Classic Bluetooth profile implementations
│   ├── a2dp.py                    # A2DP automation (media control, local/online playback)
│   ├── hfp.py                     # HFP automation (call handling, AT command parsing)
│   ├── opp.py                     # OPP automation (file transfer over Bluetooth)
│   └── pbap.py                    # PBAP automation (phonebook access, contact export)
├── constants.py                   # Constants and common config values
├── Debug_error_info/              # Logging directory for debug, info, and error logs
│   ├── debug.log
│   ├── error.log
│   └── info.log
├── gap.py                         # GAP-level operations (scan, pair, connect, discover)
├── logger_mod.py                  # Custom logger module for consistent log output
├── run.py                         # Entry point to run the entire test suite
├── trigger.py                     # CLI interface to select and run test cases
├── utils.py                       # Utility functions used across modules
└── README.md                      # This documentation file
```

---

## 🚀 Features Implemented

### ✅ Classic Bluetooth Profiles

* **A2DP (Advanced Audio Distribution Profile)**

  * Connect/disconnect A2DP device
  * Online music control (`playerctl`): play, pause, next, previous, volume
  * Offline music playback using `mpv` with FIFO pipe

* **HFP (Hands-Free Profile)**

  * Call handling automation
  * AT command and URC response capture (via `btmon`, `hcidump`)

* **OPP (Object Push Profile)**

  * Push files from host to paired mobile device over Bluetooth

* **PBAP (Phone Book Access Profile)**

  * Pull contacts (Name & Number) from paired mobile
  * Export contacts to Excel file

### ✅ GAP (Generic Access Profile)

* Discover Bluetooth devices
* Pair/unpair with devices
* Connect/disconnect
* Display available services

### ✅ Logging

* Unified logging system (`info.log`, `error.log`, `debug.log`)
* Logs saved in `Debug_error_info/` folder for easy access

### ✅ Trigger Interface

* `trigger.py` allows interactive CLI to select and run specific test cases

---

## 🛠️ Requirements

Ensure the following dependencies are installed:

```bash
sudo apt install bluez bluez-tools pulseaudio playerctl mpv python3-pip
pip install openpyxl
```

---

## 🧪 How to Run

1. **Connect Bluetooth device**
   Pair and connect your target device using `bluetoothctl` or script automation.

2. **Start Test Flow**

```bash
python3 run.py
```

Or run the trigger manually:

```bash
python3 trigger.py
```

3. **Select Test Option**
   The CLI will present options like:


################## OPERATIONS #########################

0.  Properties
1.  Scan on
2.  Scan off
3.  Devices
4.  Power[ON/OFF]
5.  Register the agent
6.  Pair
7.  Check paired Devices
8.  Check Connected Devices
9.  Connect
10. Disconnect
11. Remove Device
12. Discoverable on
13. Discoverable off
14. Trusted
15. Register Agent as Default
16. Print UUID's 
17. Controller Supported UUID's
18. Set Pairable Timeout
19. Get Pairable Timeout
20. Set Discoverable Timeout
21. Get Discoverable Timeout
22. opp file transfer file 
23. phone contact details 
24. A2DP Profile and A2DP Media Control 
25. HFP Profile testing.  
30. Exit
****************************************************************************************************
Enter your Choise......




---

## 📌 Future Enhancements (Planned)

* BLE profile testing (`Bluetooth_Low_Energy/`)
* Wifi Automation Testing.
* More robust error handling and exception coverage.
* UI-based control panel for selecting and viewing test results.

---

