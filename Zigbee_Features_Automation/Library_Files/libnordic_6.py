import json
import logging
import os
import re
import serial
import subprocess
import time


class SerialCommunication:
    """Class for serial communication with a device."""

    def __init__(self, serial_port, baud_rate_nordic):
        """Initialize the SerialCommunication object.
        Args:
            serial_port (str): The serial port to be connected.
            baud_rate_nordic (int): The baud rate for the serial communication.
        """
        self.serial_port = serial_port
        self.baud_rate_nordic = baud_rate_nordic
        self.serial_port_connection = None
        self.wireshark_process = None
        self.constants = self.load_constants()

    @staticmethod
    def load_constants():
        """Load the constants from the JSON file.
        Returns:
            dict: The constants loaded from the JSON file.
        """
        try:
            parent_dir = os.getcwd()
            constants_path = f"{parent_dir}/config/constants.json"
            if os.path.exists(constants_path):
                with open(constants_path) as fd:
                    constants = json.load(fd)
                    return constants
            else:
                return {}
        except Exception as e:
            logging.error("Failed to read constants from JSON file: %s", str(e))
            return {}

    def connect(self):
        """Connect to the serial port."""
        try:
            self.serial_port_connection = serial.Serial(
                self.serial_port, self.baud_rate_nordic, timeout=1)
            if self.serial_port_connection.is_open:
                logging.info("Device connected to the serial port")
            time.sleep(2)
        except Exception as e:
            logging.error("Failed to connect to the serial port: %s", str(e))

    def set_nvram_disabled(self):
        """Set the NVRAM disabled using the defined command in constants."""
        command = self.constants.get('NVRAM', {}).get('disable_nvram', '')
        self.write_command(command)

    def set_panid(self, panid):
        """Set the PAN ID using the defined command in constants.
        Args:
            panid (str): The PAN ID to set.
        """
        command = self.constants.get('PAN', {}).get('panid', '')
        command = ' '.join([command, panid])
        self.write_command(command)

    def get_panid(self):
        """Get the PAN ID using the defined command in constants."""
        command = self.constants.get('get_panid', {}).get('panid', '')
        self.write_command(command)

    def set_device_coordinator(self):
        """Set the device as a coordinator using the defined
           command in constants.
        """
        command = self.constants.get('coordinator', {}).get('set_role', '')
        self.write_command(command)

    def set_device_router(self):
        """Set the device as a router using the defined command
           in constants.
        """
        command = self.constants.get('router', {}).get('set_role', '')
        self.write_command(command)

    def start_bdb(self):
        """Start the BDB (Base Device Behavior) using the defined
           command in constants.
        """
        command = self.constants.get('START', {}).get('start', '')
        self.write_command(command)

    def zdo_eui64(self):
        """Get the ZDO EUI64 using the defined command in constants."""
        command = self.constants.get('zdo_eui64', {}).get('get_eui64', '')
        self.write_command(command)

    def zdo_short(self):
        """Get the ZDO short address using the defined command in constants.
        Returns:
            str: The retrieved ZDO short address.
        """
        command = self.constants.get('zdo_short', {}).get('get_short', '')
        return self.write_command(command)

    def write_command(self, command):
        """Write a command to the serial port.
        Args:
            command (str): The command to write.
        Returns:
            str: The response received from the serial port.
        """
        try:
            if self.serial_port_connection and self.serial_port_connection.is_open:
                temp1 = f"{command}\r\n"
                temp = temp1.encode("utf-8")
                self.serial_port_connection.write(temp)
                logging.info("Command written: %s", command)
                output = self.read_response(timeout=2)
                return output
            else:
                logging.error("Serial port is not open")
        except Exception as e:
            logging.error("Failed to write command: %s", str(e))

    def read_response(self, timeout=2):
        """Read the response from the serial port.
        Args:
            timeout (float): The timeout for reading the response.
        Returns:
            str: The response received from the serial port.
        """
        try:
            response = ''
            start_time = time.time()
            while True:
                if self.serial_port_connection.in_waiting:
                    response += self.serial_port_connection.read_until()\
                        .decode('utf-8')
                elif time.time() - start_time > timeout:
                    break
            response = re.sub(r'\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|uart:~\$',
                              '', response).strip()
            logging.info("Response received: %s", response)
            if ("Done" in response) or (
                    "Joined network successfully" in response):
                logging.info("Command Execution successful")
            elif "Stack already started" in response:
                logging.info("Device already configured")
            else:
                logging.info("Command Execution failed")
        except Exception as e:
            logging.error("Failed to read response: %s", str(e))
        return None

    def start_wireshark(self, duration):
        """ Starts Wireshark in the background and begins capturing packets.
        Args:
            duration: Time duration in which logs should capture.

        Returns:
            pcap file in which captured logs are saved.
        """
        try:
            timestamp = time.strftime("%y%m%d_%H%M%S", time.localtime())
            output_file = f"/tmp/capture_{timestamp}.pcap"
            cmd = ['tshark', '-i', 'nRF Sniffer for 802.15.4', '-f',
                   'IEEE 802.15.4 TAP', '-a', f'duration:{duration}',
                   '-w', output_file]
            self.wireshark_process = subprocess.Popen(
                 cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            logging.info("Wireshark started")
            logging.info("Capture file: %s", output_file)
            return output_file
        except Exception as e:
            logging.error("Failed to start Wireshark: %s", str(e))

    def stop_wireshark(self):
        """ Method to Stop the Wireshark process.
        Returns:
            None
        """
        try:
            if hasattr(self, 'wireshark_process'):
                self.wireshark_process.terminate()
                self.wireshark_process.wait()
                logging.info("Wireshark stopped")
        except Exception as e:
            logging.error("Failed to stop Wireshark: %s", str(e))

    def close(self):
        """Close the serial port connection."""
        try:
            if self.serial_port_connection:
                self.serial_port_connection.close()
                logging.info("Serial port connection closed")
        except Exception as e:
            logging.error("Failed to close serial port connection: %s", str(e))
