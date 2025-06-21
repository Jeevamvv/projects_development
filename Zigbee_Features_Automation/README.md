
---

## 📘 Zigbee Features Automation

This project automates the testing of Zigbee device features using Python. It is tailored to interact with Zigbee modules (such as XBee or Nordic-based solutions) to validate core functionalities like cluster communication, attribute control, device binding, and network diagnostics. It is structured with modular test scripts, a reusable core library, and configuration-driven logic.

---

### 📂 Project Structure

```
Zigbee_Features_Automation/
├── Calling_Scripts/
│   └── test_xbee.py          # Main test runner script
├── Library_Files/
│   ├── clusters.py           # Definitions and helpers for Zigbee clusters
│   └── libnordic_6.py        # Core communication logic with the Zigbee hardware
├── config.yaml               # Config file for test parameters
├── constants.json            # Constants and cluster definitions
├── conftest.py               # Pytest fixture setup
```

---

### ⚙️ Features

* ✅ **Cluster-based testing** – Automates standard Zigbee clusters like On/Off, Temperature, Light Level, etc.
* ✅ **Command execution** – Sends commands to end devices and reads responses.
* ✅ **Device communication** – Supports serial communication with Zigbee modules (XBee/Nordic).
* ✅ **Configurable** – Centralized config file (`config.yaml`) for defining test targets and parameters.
* ✅ **Extensible** – Add new tests by modifying or extending the `clusters.py` and test scripts.

---

### 🚀 Getting Started

#### Prerequisites

* Python 3.8+
* Pytest
* A Zigbee development board (XBee/Nordic recommended)
* USB-Serial adapter (if using UART)
* Required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

#### Run Tests

```bash
cd Zigbee_Features_Automation
pytest Calling_Scripts/test_xbee.py
```

Modify `config.yaml` to define the Zigbee device under test and target clusters.

---

### 🧪 Example Test Logic (from `test_xbee.py`)

```python
# Sample logic snippet
def test_on_off_cluster():
    send_on_command()
    assert device_status() == 'on'
    send_off_command()
    assert device_status() == 'off'
```

---

### 🛠 Configuration

Update `config.yaml` with values like:

```yaml
device_port: "/dev/ttyUSB0"
baudrate: 115200
clusters:
  - on_off
  - temperature
  - level_control
```

Cluster definitions and their command structures are stored in `constants.json`.

---

### 📚 Libraries Overview

* `libnordic_6.py`: Handles the serial communication with the Zigbee device.
* `clusters.py`: Contains implementations for sending cluster-specific commands.
* `constants.json`: Acts as a cluster and command dictionary used throughout the framework.

---

### 👨‍💻 Contributing

You can add new cluster tests by:

1. Defining new entries in `constants.json`
2. Adding logic in `clusters.py`
3. Creating a test function in `test_xbee.py`

---

### 📄 License

This project is open-sourced under the MIT License.

---
