from wifi_utils import get_nm_interface, get_device_by_type
from logger_mod import logger
import time




from wifi_utils import get_nm_interface, get_device_by_type
from logger_mod import logger
import time



def scan_wifi(max_retries=5):
    nm = get_nm_interface()
    device = get_device_by_type(nm)

    if not device:
        logger.error("Wi-Fi device not found")
        return []

    for attempt in range(max_retries):
        try:
            device.RequestScan({})
            logger.info("Scan requested. Waiting for results...")
            time.sleep(3)

            aps = device.GetAccessPoints()
            networks = []

            for ap in aps:
                ssid = bytearray(ap.Ssid).decode(errors="ignore")
                strength = ap.Strength
                networks.append((ssid, strength))

            logger.info(f"Found {len(networks)} Wi-Fi networks.")
            return sorted(networks, key=lambda x: x[1], reverse=True)

        except Exception as e:
            if "Scanning not allowed" in str(e):
                logger.warning("Scan in progress...retrying")
                time.sleep(2)
                continue
            else:
                logger.error(f"Scan failed: {e}")
                break

    logger.error("Failed to complete scan after retries.")
    return []





def connect_wifi(ssid, password=None):
    nm = get_nm_interface()
    device = get_device_by_type(nm)

    if not device:
        logger.error("Wi-Fi device not found")
        return False

    conn_settings = {
        '802-11-wireless': {'ssid': ssid.encode(), 'mode': 'infrastructure'},
        'connection': {'id': ssid, 'type': '802-11-wireless', 'uuid': ''},
        'ipv4': {'method': 'auto'},
        'ipv6': {'method': 'ignore'}
    }

    if password:
        conn_settings['802-11-wireless-security'] = {
            'key-mgmt': 'wpa-psk',
            'psk': password
        }

    try:
        conn = nm.AddAndActivateConnection(conn_settings, device, "/")
        logger.info(f"Connected to SSID: {ssid}")
        return True
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False

def list_saved_networks():
    nm = get_nm_interface()
    conns = nm.ListConnections()
    return [c.GetSettings()['connection']['id'] for c in conns]

def remove_saved_network(ssid):
    nm = get_nm_interface()
    for c in nm.ListConnections():
        if c.GetSettings()['connection']['id'] == ssid:
            c.Delete()
            logger.info(f"Removed saved network: {ssid}")
            return True
    logger.warning(f"No saved network found for SSID: {ssid}")
    return False
