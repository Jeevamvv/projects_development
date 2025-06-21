from pydbus import SystemBus

def get_nm_interface():
    bus = SystemBus()
    nm = bus.get("org.freedesktop.NetworkManager")
    return nm

def get_device_by_type(nm, device_type=2):
    bus = SystemBus()
    for dev_path in nm.GetDevices():
        dev_obj = bus.get("org.freedesktop.NetworkManager", dev_path)
        if dev_obj.DeviceType == device_type:
            return dev_obj
    return None
