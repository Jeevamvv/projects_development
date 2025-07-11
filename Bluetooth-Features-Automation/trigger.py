import signal
import utils as convert
daemon = convert.Daemon()
Dbus_Process = daemon.d_bus_daemon()
Bluetoothd_process = daemon.bluetooth_d_daemon()
import constants as gl
import dbus.mainloop.glib
import gap
from logger_mod import *
import sys
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import os
from logger_mod import Logger
logger_obj = Logger()

import time 
from Classic_Bluetooth_Profile import opp, a2dp, hfp
from Classic_Bluetooth_Profile.opp import *
from Classic_Bluetooth_Profile.pbap import *
from Classic_Bluetooth_Profile.a2dp import *
from Classic_Bluetooth_Profile.hfp import *


bus = dbus.SystemBus()

# Code to select the adapter out of active adapters
returned_value = convert.check_active_dongles()
if returned_value == 0:
    log.info("=====  No active dongles attached to ports =====")
    sys.exit(1)
else:
    log.info(" Selected interface: {}".format(str(returned_value)))
    gl.ADAPTER_OBJ = returned_value

#  Code to check the paired devices and store them in list
gl.list_of_pair_device = convert.check_paired_device()

while True:

    log.info("*"*100)
    log.info("################### OPERATIONS #########################")
    log.info("0.  Properties")
    log.info("1.  Scan on")
    log.info("2.  Scan off")
    log.info("3.  Devices")
    log.info("4.  Power[ON/OFF]")
    log.info("5.  Register the agent")
    log.info("6.  Pair")
    log.info("7.  Check paired Devices")
    log.info("8.  Check Connected Devices")
    log.info("9.  Connect")
    log.info("10. Disconnect")
    log.info("11. Remove Device")
    log.info("12. Discoverable on")
    log.info("13. Discoverable off")
    log.info("14. Trusted")
    log.info("15. Register Agent as Default")
    log.info("16. Print UUID's ")
    log.info("17. Controller Supported UUID's")
    log.info("18. Set Pairable Timeout")
    log.info("19. Get Pairable Timeout")
    log.info("20. Set Discoverable Timeout")
    log.info("21. Get Discoverable Timeout")
    log.info("22. opp file transfer file ")
    log.info("23. phone contact details ")
    log.info("24. A2DP Profile and A2DP Media Control ")
    log.info("25. HFP Profile testing.  ")
    log.info("30. Exit")
    log.info("*"*100)

    try:
        val = int(input("Enter your Choise.......  "))
    except ValueError:
        log.info(" Invalid Choise, ValueError  ")
        continue
    except NameError:
        log.info(" Invalid Choise, NameError ")
        continue
    else:
        log.info("#"*100)
    finally:
        log.debug(" User is trying to access the D-Bus Api's ")
	
    if val == 0:
        # Properties of adapter.
        ref = gap.GapLib()
        while(True):
            log.info("*"*100)
            log.info("1. Powered")
            log.info("2. Address")
            log.info("3. Address_Type")
            log.info("4. Alias")
            log.info("5. Name")
            log.info("6. Class")
            log.info("7. DiscoverableTimeout")
            log.info("8. PairableTimeout")
            log.info("9. Exit")

            dict = {1:"powered", 2: "address", 3: "address_type", 4: "alias", 5: "name",
                          6: "class_of_device", 7: "discoverabletimeout", 8: "pairabletimeout"}

            try:
                ch = int(input("Enter your choise : "))
                if ch == 9:
                    break
                if ch <= 0 or ch > 9:
                    log.info(" Invalid choise, please enter the choise within the range")
                    continue
            except Exception:
                log.info("*"*100)
                log.info("  Invalid Entry ")
                continue
            else:
                log.info("#"*100)

            log.info(getattr(ref,dict[ch],"No Such Attribute Found! "))

    if val == 1:
        # Code for scan
        log.debug("  User started scan operation ")
        Gap_obj = gap.GapLib()
        value = input("Do you want to set scan duration [y/n] ").strip().lower()

        if value == "y":
            time = int(input("Enter the duration.."))
            gl.list_of_scanned_devices = Gap_obj.start_scan(time)
            if gl.list_of_scanned_devices == False:
                continue
        else:
            Gap_obj.start_scan()
            continue

        for key, value in  gl.list_of_scanned_devices.items():
            log.info("Name:       {}".format(key.encode('utf-8')))
            log.info("Bd_address: {}".format(value.encode('utf-8')))
            log.info("*" * 100)

    if val == 2:
        # To stop the scan
        log.debug("  User selected to stop the scan operation")
        Gap_obj = gap.GapLib()

        gl.list_of_scanned_devices = Gap_obj.stop_scan()
        if gl.list_of_scanned_devices == False:
            continue

        for key, value in gl.list_of_scanned_devices.items():
            log.info("Name:       {}".format(key.encode('utf-8')))
            log.info("Bd_address: {}".format(value.encode('utf-8')))
            log.info("*" * 100)

    if val == 3:
        # Scanned Devices
        log.debug("  User trying to access the scanned devices ")
        return_dictionary = gl.list_of_scanned_devices

        length = len(return_dictionary)
        if length == 0:
            log.info("======= No devices =========")
            continue
        else:
            log.info("Length:- ".format(length))
            for key,value in return_dictionary.items():
                log.info("Name:       {}".format(key.encode('utf-8')))
                log.info("Bd_address: {}".format(value.encode('utf-8')))
                log.info("*"*100)

    if val == 4:
        # Power [ON/OFF]

        val = input("Do you want to turn [ON/OFF]").lower()
        if val == "on":
            try:
                adapter_proxy = bus.get_object(gl.BUS_NAME,gl.ADAPTER_OBJ)
                interface_proxy = dbus.Interface(adapter_proxy,"org.freedesktop.DBus.Properties")
                    
                value = dbus.Boolean(1)
                log.debug("  User trying to power on the adapter ")
                interface_proxy.Set("org.bluez.Adapter1", "Powered", value)
                log.info(" Power of the adapter set to 1")
                log.info(" Successfully Turned On Radio.. ")
                log.info("*"*100)
            except Exception as e:
                log.critical(" Failed to power ON the adapter")
                log.critical(e)

        elif val == "off":
            try:
                adapter_proxy = bus.get_object(gl.BUS_NAME,gl.ADAPTER_OBJ)
                interface_proxy = dbus.Interface(adapter_proxy,"org.freedesktop.DBus.Properties")
                value = dbus.Boolean(0)
                log.debug("  User trying to power off the adapter ")
                interface_proxy.Set("org.bluez.Adapter1", "Powered", value)
                log.info("  Power of the adapter is set to 0 ")
                log.info(" Successfully Turned off the radio")
                log.info("*"*100)
            except Exception as e:
                log.critical(e)
                log.info(" Failed to power OFF the adapter")

    if val == 5:
    # Agent Code
        path = "/test/agent"
        capability = "NoInputNoOutput"  # Correct capability string

        try:
            p_obj = bus.get_object(gl.BUS_NAME, "/org/bluez")
            agent_manager = dbus.Interface(p_obj, "org.bluez.AgentManager1")
            agent_manager.RegisterAgent(path, capability)
            log.info("Agent registered successfully")
        except Exception as e:
            log.critical(f"Exception during agent registration: {e}")
            log.debug("Failed to register the agent")

    if val == 6:
        # Pair
        log.debug(" User selected pair operation")
        name = input("Enter the name: ").strip()
        ref = gap.GapLib()
        return_value = ref.pair(name)
        if return_value == False:
            log.info(" No such name found! ")
            continue

    if val == 7:
        # Display Paired device
        log.debug(" User selected to display the list of paired devices")
        ref = gap.GapLib()

        returned_list = ref.device_paired()
        if type(returned_list) == bool:
            if returned_list == False:
                log.info(" No paired Devices! ")
                continue

        for i in returned_list:
            log.info(i)

    if val == 8:
        # To check current connected device
        log.debug(" User selected to check the current connected device")

        ref = gap.GapLib()
        list_of_paired_devices = ref.device_paired()
        if type(list_of_paired_devices) == bool:
            if list_of_paired_devices == False:
                log.info(" No Active Connection Found! ")
                continue

        check = 0
        for bd_address in list_of_paired_devices:
            path = convert.convert_colon_underscore_with_path(bd_address,gl.ADAPTER_OBJ)
            proxy_obj = bus.get_object(gl.SERVICE_NAME, path)
            interface = dbus.Interface(proxy_obj,gl.D_BUS_PROPERTIES)
            try:
                ret = interface.Get(gl.DEVICE_INTERFACE,"Connected")
            except Exception as e:
                log.critical(e)
                break
            if ret == 1:
                check = 1
                address = interface.Get(gl.DEVICE_INTERFACE,"Address")
                name = interface.Get(gl.DEVICE_INTERFACE,"Name")
                log.info(" Connected Device :-  ")
                log.info("Address: {}".format(str(address)))
                log.info("Name   : {}".format(str(name)))
        if check == 0:
            log.info(" NO Active connection found ")
				   
    if val == 9:
        # Connect
        daemon = convert.Daemon()
        gl.pulseaudio_daemon = daemon.pulseaudio()
        log.debug(" User selected connect option ")
        ref = gap.GapLib()
        returned_paired_list = ref.device_paired()
        if returned_paired_list == 0:
            log.info(" NO paired devices to connect! ")
            continue

        tmp_var = 1
        for device in returned_paired_list:
            log.info("{}. {}".format(tmp_var,str(device)))
            tmp_var = tmp_var + 1

        choise = int(input("Enter your choise...."))
        bd_address = returned_paired_list[choise-1]
        return_value = ref.connect(bd_address)
        if return_value == True:
            log.info("*"*100)
            log.info(" Connected Successfully! ")

        if return_value == False:
            log.info("*"*100)
            log.info(" Failed to Connect! ")

    if val == 10:
        # Disconnect
        log.debug(" User selected Disconnect option ")

        ref = gap.GapLib()
        returned_value = ref.disconnect()
        if returned_value == True:
            log.info(" Disconnected Successfully ")
        if returned_value == False:
            log.info(" Failed Disconnect! ")

    if val == 11:
        # Remove Paired Device
        log.debug("  User selected to remove paired devices ")
        ref = gap.GapLib()
        list_of_pair_device = ref.device_paired()

        if type(list_of_pair_device) == bool:
            if list_of_pair_device == False:
                log.info(" NO paired devices! ")
                continue

        tmp_var = 1
        for devices in list_of_pair_device:
            log.info("{}. {}".format(tmp_var,str(devices)))
            tmp_var = tmp_var + 1

        choise = int(input(" Enter your choise .."))
        bd_address = list_of_pair_device[choise-1]
        return_value = ref.remove_device(bd_address)
        if return_value == True:
            log.info(" Device Removed Successfully! ")
        if return_value == False:
            log.info(" Failed to Remove the Device ")

    if val == 12:
        # Discoverable On
        log.debug("  User selected discoverable on option")
        ref = gap.GapLib()
        return_value = ref.start_discovery()
        if return_value == True:
            log.info(" Set to Discoverable Mode!.. ")
        if return_value == False:
            log.info("  Failed to Set Discoverable On ")

    if val == 13:
        # Discoverable OFF
        log.debug(" User selected discoverable OFF option")
        ref = gap.GapLib()
        return_value = ref.stop_discovery()
        if return_value == True:
            log.info(" Stopped  Discoverable Mode!.. ")
        if return_value == False:
            log.info(" Failed to Set Discoverable OFF  ")

    if val == 14:
        # Trust the Paired-Device
        log.debug(" User selected the option trust the device")
        ref = gap.GapLib()
        list_of_pair_device = ref.device_paired()

        res = len(list_of_pair_device)
        if res  == 0:
            log.info(" No devices are paired ")
            continue

        tmp_var = 1
        for devices in list_of_pair_device:
            log.info("{}. {}".format(tmp_var,str(devices)))
            tmp_var = tmp_var + 1

        choise = int(input(" Enter your choise to trust the device .."))
        bd_address = list_of_pair_device[choise-1]
        path = convert.convert_colon_underscore_with_path(bd_address,gl.ADAPTER_OBJ)
        device_proxy = bus.get_object(gl.BUS_NAME,path)
        interface = dbus.Interface(device_proxy,gl.D_BUS_PROPERTIES)
        try:
            data = dbus.Boolean(1)
            interface.Set(gl.DEVICE_INTERFACE,"Trusted",data)
            log.info("  Device: {} Trusted Successfully ".format(bd_address))
            res =  interface.Get(gl.DEVICE_INTERFACE,"Trusted")
            log.info("===================Result=========================== ")
            log.info(res)
        except Exception as e:
            log.critical(e)
            log.info(" Failed to trust the device")
            continue
    
    if val == 15:
        # Set Agent as Default
        log.debug(" User selected the option set agent as default")
        bluez_obj_prxy = bus.get_object(gl.BUS_NAME,"/org/bluez")
        interface = dbus.Interface(bluez_obj_prxy,"org.bluez.AgentManager1")
        try:
            path = "/test/agent"
            interface.RequestDefaultAgent(path)
            log.info(" Agent set as Default")
        except Exception as e:
            log.critical(e)
            log.info("  Failed to set the agent as Default-agent ")
            continue

    if val == 16:
        # Check supported UUID's in the list of Paired-Devices
        log.debug(" User selected the option check supported UUID's")

        ref = gap.GapLib()
        list_of_pair_device = ref.device_paired()

        if type(list_of_pair_device) == bool:
            if list_of_pair_device == False:
                log.info(" No Device are Paired!  ")
                continue

        tmp_var = 1

        for devices in list_of_pair_device:
            log.info("{}. {}".format(tmp_var,str(devices)))
            tmp_var = tmp_var + 1

        choise = int(input(" Enter your choise  .."))
        bd_address = list_of_pair_device[choise-1]
        path = convert.convert_colon_underscore_with_path(bd_address,gl.ADAPTER_OBJ)
        log.info(" path: {}".format(path))
        device_proxy = bus.get_object(gl.SERVICE_NAME,path)
        device_interface = dbus.Interface(device_proxy,gl.D_BUS_PROPERTIES)
        try:
            UUID = device_interface.Get("org.bluez.Device1","UUIDs")
        except Exception as e:
            log.critical(e)
            continue
        log.info("====== List of Supported UUID in Device======")
        dummy_string = convert.add_uuid_with_names(UUID)
        
        for key,value in dummy_string.items():
            log.info("profile: {} : {}".format(str(key), str(value)))
        log.info("*"*100)

    if val == 17:
        # Controller Supported UUID's
        log.debug("  User selected the option show controller supported UUID ")
            
        device_proxy = bus.get_object(gl.SERVICE_NAME,gl.ADAPTER_OBJ)
        device_interface = dbus.Interface(device_proxy,gl.D_BUS_PROPERTIES)
        UUID = device_interface.Get(gl.ADAPTER_INTERFACE,"UUIDs")
        log.info("====== List of Supported UUID in Device====== ")

        dummy_string = convert.add_uuid_with_names(UUID)
        for key,value in dummy_string.items():
            log.info("Profile: {}  : {}".format(str(key),str(value)))
        log.info("*"*100)

    if val == 18:
        # Set Pairable Timeout
        log.debug(" User selected the option set pairable Timeout")
        ref = gap.GapLib()
        time = int(input(" Enter the Time to Set..."))
        return_value = ref.set_pairable_timeout(time)
        if return_value == True:
            log.info(" Pairable Time is Set Successfully.")
        if return_value == False:
            log.info(" Failed to Set pairableTimeOut ")

    if val == 19:
        # Get Pairable Timeout
        log.debug("  User selected the option Get pairable Timeout")
        ref = gap.GapLib()
        return_value = ref.get_pairable_timeout()
        if return_value:
            log.info(" Pairable Timeout Duration is: {}".format(str(return_value)))
        if return_value == False:
            log.info(" Failed to Fetch pairableTimeOut Duration ")

    if val == 20:
        # Set Discoverable Timeout
        log.debug(" User selected the option set Discoverable Timeout")
        ref = gap.GapLib()
        time = int(input(" Enter the Time to Set..."))
        return_value = ref.set_Discoverable_timeout(time)
        if return_value == True:
            log.info(" Discoverable Time is Set Successfully ")
        if return_value == False:
            log.info(" Failed to Set DiscoverableTimeOut ")

    if val == 21:
        # Get Discoverable Timeout
        log.debug(" User selected the option Get Discoverable Timeout")
        ref = gap.GapLib()
        return_value = ref.get_Discoverable_timeout()
        if return_value:
            log.info(" Discoverable Time out Duration is:{}".format(str(return_value)))
        if return_value == False:
            log.info(" Failed to Fetch DiscoverableTimeOut Duration ")

    if val == 22:
        # OPP profile file send from source to destination.
        log.debug("User selected the option to send OPP profile file from source to destination.")

        if not gl.list_of_pair_device:
            log.info("No paired devices found. Please pair a device first.")
        else:
            device_address = gl.list_of_pair_device[0]  # Auto-select first paired device
            log.info(f"Using paired device for OPP transfer: {device_address}")
        
            try:
                file_path = input("Enter full path of file to send (ex. /home/engineer/a.py ): ").strip()
                print(f"DEBUG_INFO: entered file path = {file_path}")
                if os.path.exists(file_path):
                    opp.send_file_via_opp(device_address, file_path)
                else:
                    log.error("File does not exist. Please provide a valid file.")
            except Exception as e:
                log.error(f"Error during OPP file transfer: {e}")

    if val == 23:
        log.debug("User selected phone contact fetch via PBAP.")
        device_address = input("Enter the connected device Bluetooth address (e.g. D4:CB:CC:86:9D:8C): ").strip()
        output_file = input("Enter the output Excel file path (e.g. /home/engineer/contacts.xlsx): ").strip()

        from Classic_Bluetooth_Profile.pbap import fetch_contacts
        success = fetch_contacts(device_address, output_file)

        if success:
            print(f"✅ Contacts successfully exported to {output_file}")
        else:
            print("❌ Failed to export contacts.")

    if val == 24:
        #A2DP Profile and A2DP Media Control Test Menu
        log.debug("User selected the option to A2DP Profile and A2DP Media Control Test Menu")

        # Initialize volume_level from current system volume (0-100), scale it to 0-10
      #  volume_level = a2dp.get_volume() // 10

        while True:
            log.info("*" * 100)
            log.info("🎵 A2DP Media Control Test Menu 🎵")
            log.info("1. 🎶  Select Player box MUSIC CONTROL")
            log.info("2. 🎶  Select OFFLINE MUSIC CONTROL")
            log.info("3. 🎶  Select Online MUSIC CONTROL")
            log.info("4. 🚪 Exit A2DP Media Test")
        
            try:
                choice = int(input("Enter your choice: ").strip())
            except ValueError:
                log.warning("Invalid input. Please enter a number between 1-7.")
                continue

            if choice == 1:
                log.info("🎶 Select Player box MUSIC CONTROL")
                a2dp.Player_Box_MUSIC_CONTROL_Control()
            elif choice == 2:
                log.info("🎶 Select OFFLINE MUSIC CONTROL")
                a2dp.list_and_play_local_music()
            elif choice == 3:
                log.info("🎶 Select Online MUSIC CONTROL")
                a2dp.Online_Play_Music_Control()
            elif choice == 4:
                log.info("Exiting A2DP Media Test Menu...")
                break
            else:
                log.warning("Invalid choice. Try again.")

    if val == 25:
        log.debug("User selected the option to HFP Profile and Call Control Test Menu")

        while True:
            log.info("*" * 100)
            log.info("📞 HFP Telephony Test Menu 📞")
            log.info("1. Connect and Play Music (Device switch)")
            log.info("2. Incoming Call ➝ Accept")
            log.info("3. Incoming Call ➝ Reject")
            log.info("4. Three-Way Calling")
            log.info("5. Reject Incoming Call Without Accepting")
            log.info("6. Outgoing Call ➝ Then Hold")
            log.info("7. Outgoing Call ➝ Airplane Mode")
            log.info("8. Call Ongoing ➝ Incoming ➝ Reject")
            log.info("9. 🚪 Exit HFP Test Menu")

            try:
                choice = int(input("Enter your choice: ").strip())
            except ValueError:
                log.warning("Invalid input. Please enter a number between 1-9.")
                continue

            import Classic_Bluetooth_Profile.hfp as hfp  # Make sure this file contains the test functions

            if choice == 1:
                hfp.simulate_music_switch()
            elif choice == 2:
                hfp.simulate_incoming_call(accept=True)
            elif choice == 3:
                hfp.simulate_incoming_call(accept=False)
            elif choice == 4:
                hfp.simulate_three_way_call()
            elif choice == 5:
                hfp.simulate_call_rejection()
            elif choice == 6:
                hfp.simulate_outgoing_call_with_hold()
            elif choice == 7:
                hfp.simulate_airplane_mode_termination()
            elif choice == 8:
                hfp.simulate_call_interrupt_and_reject()
            elif choice == 9:
                log.info("Exiting HFP Telephony Test Menu...")
                break
            else:
                log.warning("Invalid choice. Try again.")

    if val == 30:
        # Exit
        Dbus_Process.kill()
        os.killpg(os.getpgid(Bluetoothd_process.pid),signal.SIGTERM)
        if gl.pulseaudio_daemon != "NULL":
            os.killpg(os.getpgid(gl.pulseaudio_daemon.pid),signal.SIGTERM)
        sys.exit(1)

   