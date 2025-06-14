from Zigbee_Project.libs.lib_nordic import SerialCommunication


class ClusterControls(SerialCommunication):
    """Class representing cluster controls for serial communication.
       Inherits from the SerialCommunication class.
    Methods:
        zcl_ping: Sends a ZCL command to a device with the specified
                  device ID, command type, and payload.
        zcl_write: ZCL write command.
        zcl_read: ZCL read command.
    """

    def zcl_ping(self, dev_id, command_type, payload):
        """Send a ZCL command to a device.

        Args:
            dev_id (str): The device ID to send the command to.
            command_type (str): The command type ('ping' or 'ping1').
            payload (str): The payload to include in the command.

        Returns:
            None
        """
        command = self.constants.get(f'zcl_{command_type}', {}).get(command_type, '')
        command = ' '.join([command, dev_id, payload])
        self.write_command(command)

    def zcl_write(self, values):
        """ZCL Write command.
        Args:
            values (str): The values for write command.
        Returns:
            None
        """
        command = self.constants.get('zcl_write', {}).get('write', '')
        command = ' '.join([command, values])
        self.write_command(command)

    def zcl_read(self, values1):
        """ZCL read command.
        Args:
           values1 (str): The values for read command.
        Returns:
           None
        """
        command = self.constants.get('zcl_read', {}).get('read', '')
        command = ' '.join([command, values1])
        self.write_command(command)


class IdentifyModeCluster:
    """Class representing the Identify Mode cluster.

    Methods:
       get_cluster_info(): Returns the cluster information for the device.
       ep(): Returns the endpoint.
       get_cluster_id(): Returns the cluster ID.
       get_profile(): Returns the profile.
       get_attribute_id(): Returns the attribute ID.
       get_attribute_type(): Returns the attribute type.
       get_attribute_value(): Returns the attribute value.
    """

    def __init__(self):
        self._ep = "64"
        self._cluster_id = "0x0003"
        self._profile = "0x0104"
        self._attribute_id = "0x0000"
        self._attribute_type = "0x21"
        self._attribute_value = "0x1E"

    def get_cluster_info(self):
        """Cluster information of device.

        Returns:
            list: List of cluster information of the  device.
        """
        cluster_info_c = [
            self.ep(),
            self.get_cluster_id(),
            self.get_profile(),
            self.get_attribute_id(),
            self.get_attribute_type(),
            self.get_attribute_value()
        ]
        return cluster_info_c

    def get_cluster_info_read(self):
        """Cluster information for zcl_read command.
        Returns:
            List of cluster information for zcl_read command.
        """
        cluster_info_read = [
            self.ep(),
            self.get_cluster_id(),
            self.get_profile(),
            self.get_attribute_id()
        ]
        return cluster_info_read

    def ep(self):
        """Return the endpoint.
        Returns:
            str: The endpoint.
        """
        return self._ep

    def get_cluster_id(self):
        """Return the cluster ID.
        Returns:
            str: The cluster ID.
        """
        return self._cluster_id

    def get_profile(self):
        """Return the profile.
        Returns:
            str: The profile.
        """
        return self._profile

    def get_attribute_id(self):
        """Return the attribute ID.
        Returns:
            str: The attribute ID.
        """
        return self._attribute_id

    def get_attribute_type(self):
        """Return the attribute type.
        Returns:
            str: The attribute type.
        """
        return self._attribute_type

    def get_attribute_value(self):
        """Return the attribute value.
        Returns:
            str: The attribute value.
        """
        return self._attribute_value
