import logging
import pytest
import time


from Zigbee_Project.config.clusters import ClusterControls
from Zigbee_Project.config.conftest import data
from Zigbee_Project.config.clusters import IdentifyModeCluster
from Zigbee_Project import logger
from Zigbee_Project.libs import zigbee_constants

log = logger.Logger()


class Test_Cases:

    @pytest.mark.skip
    def test_tc_0001(self, data):
        """Test case to configure device role as coordinator
           and get short address of the same.
        """
        coordinator = data.coordinator_object_list[0]
        coordinator.connect()
        coordinator.start_wireshark(duration=100)
        coordinator.set_nvram_disabled()
        coordinator.set_panid(panid=data.pan_id_list[0])
        coordinator.get_panid()
        coordinator.set_device_coordinator()
        coordinator.start_bdb()
        coordinator.zdo_eui64()
        coordinator.zdo_short()
        coordinator.stop_wireshark()


    def test_tc_0002(self, data):
        """Test case to configure device role as router
           and get short address of the same and closing the
           coordinator and router.
        """
        router = data.router_object_list[0]
        router.connect()
        router.start_wireshark(duration=100)
        router.set_nvram_disabled()
        router.set_device_router()
        router.start_bdb()
        router.zdo_eui64()
        router.zdo_short()
        coordinator = data.coordinator_object_list[0]
        router.close()
        coordinator.close()
        router.stop_wireshark()

    @pytest.mark.skip
    def test_tc_003(self, data):
        """Test case for performing ping for coordinator and router
           and sending the write command for Identify mode cluster between
           devices and reading cluster information(Identify_time Remaining).
        """
        coordinator = data.coordinator_object_list[0]
        router = data.router_object_list[0]
        cluster_controls = ClusterControls(router.serial_port,
                                           router.baud_rate_nordic)
        cluster_controls.connect()
        router.start_wireshark(duration=100)
        cluster_controls.zcl_ping(dev_id=data.coordinator_dev_id_list[0],
                                  command_type='ping', payload="30")
        identify_mode_cluster_c = IdentifyModeCluster()
        temp = " ".join([f"{data.coordinator_dev_id_list[0]}"] +
                        identify_mode_cluster_c.get_cluster_info())
        cluster_controls.zcl_write(temp)
        temp1 = " ".join([f"{data.coordinator_dev_id_list[0]}"]
                         + identify_mode_cluster_c.get_cluster_info_read())
        cluster_controls.zcl_read(temp1)
        cluster_controls.close()

        cluster_controls = ClusterControls(coordinator.serial_port,
                                           coordinator.baud_rate_nordic)
        cluster_controls.connect()
        cluster_controls.zcl_ping(dev_id=data.router_dev_id_list[0],
                                  command_type='ping1', payload="30")

        identify_mode_cluster_r = IdentifyModeCluster()
        temp = " ".join([f"{data.router_dev_id_list[0]}"] +
                        identify_mode_cluster_r.get_cluster_info())
        cluster_controls.zcl_write(temp)
        temp1 = " ".join([f"{data.router_dev_id_list[0]}"]
                         + identify_mode_cluster_c.get_cluster_info_read())
        cluster_controls.zcl_read(temp1)
        cluster_controls.close()
        router.stop_wireshark()
