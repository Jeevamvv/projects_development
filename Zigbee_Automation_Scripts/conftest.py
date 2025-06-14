import logging
import os
import pytest
import sys
import yaml

from Zigbee_Project import logger
log = logger.Logger()



class Parser:
    
    """Class to read config file and creating objects for the classes
       in libraries.
    """

    def __init__(self):
        self.destination_router = None
        self.dest_coordinator = None
        self.destination_coordinator = None
        self.serial_port = None
        self.manufacturer = None
        self.router_object_list = None
        self.coordinator_object_list = None
        self.baud_rate = None
        self.router_count = None
        self.coordinator_count = None
        self.path = None
        self.coordinator = None
        self.router = None
        self.baud_rate_nordic = None
        self.pan_id_list = None
        self.coordinator_dev_id_list = None
        self.router_dev_id_list = None
        self.read_config()

    def read_config(self):
        """To read config file and instantiate coordinator, router 
            device objects and to pass serial port and baud rate as
           parameters to the classes.
        """
        self.path = "config/config.yaml"
        if os.path.exists(self.path):
            with open("config/config.yaml", "r") as fd:
                config = yaml.safe_load(fd)
                self.coordinator = config["input_value"]["coordinator"]
                self.coordinator_count = config["input_value"][
                    "coordinator_count"]
                
                self.router = config["input_value"]["router"]
                self.router_count = config["input_value"]["router_count"]
                self.baud_rate = config["input_value"]["baud_rate"]
                
                self.coordinator_object_list = []
                self.router_object_list = []
                self.router_dev_id_list = []
                
                self.coordinator_dev_id_list = []
                self.pan_id_list = []
                self.baud_rate_nordic = config["input_value"][
                    "baud_rate_nordic"]

                for i in range(0, self.coordinator_count):
                    self.serial_port = self.coordinator[f"coordinator_{i}"][
                        "serial_port"]
                    self.manufacturer = self.coordinator[f"coordinator_{i}"][
                        "manufacturer"]
                    
                    if self.manufacturer == "NORDIC":
                        module = __import__("lib_nordic")
                        class_obj = getattr(module, "SerialCommunication")
                        self.coordinator_object_list.append(
                            class_obj(self.serial_port, self.baud_rate_nordic))
                        self.destination_coordinator = self.coordinator[
                            f"coordinator_{i}"]["dev_id"]
                        self.coordinator_dev_id_list.append(
                            self.destination_coordinator)
                        self.dest_coordinator = self.coordinator[
                            f"coordinator_{i}"]["pan_id"]
                        self.pan_id_list.append(self.dest_coordinator)
                    else:
                        logging.info("Please specify proper manufacturer")
                    if (len(self.coordinator)) < self.coordinator_count:
                        logging.info(f"Please enter the details for all"
                                     f" {self.coordinator_count} coordinators")
                        sys.exit(1)

                for i in range(0, self.router_count):
                    self.serial_port = self.router[f"router_{i}"]["serial_port"]
                    self.manufacturer = self.router[f"router_{i}"]["manufacturer"]
                    
                    if self.manufacturer == "NORDIC":
                        module = __import__("lib_nordic")
                        class_obj = getattr(module, "SerialCommunication")
                        self.router_object_list.append(
                            class_obj(self.serial_port, self.baud_rate_nordic))
                        self.destination_router = self.router[f"router_{i}"]["dev_id"]
                        self.router_dev_id_list.append(self.destination_router)
                    else:
                        logging.info("Please specify proper manufacturer")
                    if (len(self.router)) < self.router_count:
                        logging.info(
                            f"Please enter the details for all"
                            f" {self.router_count}routers")
                        sys.exit(1)


class TearDown:
    """Class representing post condition of the fixture data. """

    def __init__(self):
        pass

    def post_condition(self, data):
        """ Post condition to be executed after the execution of test cases. """

        logging.info("End of Testcases")


class Setup:
    """Class representing pre-condition of the fixture data."""

    def __init__(self):
        pass

    def pre_condition(self, data):
        """Pre--condition to be executed before the execution of
           test cases.
        """

        logging.info("started test case execution")
        test_name = os.environ.get('PYTEST_CURRENT_TEST').split(' ')[0]
        logging.info("test name is ", test_name)
        testcase_name = log.get_function_name(test_name)
        log.logger(testcase_name)


@pytest.fixture(scope="session")
def data():
    """The fixture to parse the data inside parser class. """
    local_object = Parser()
    pre_condition_obj = Setup()
    post_condition_obj = TearDown()
    pre_condition_obj.pre_condition(local_object)
    yield local_object
    post_condition_obj.post_condition(local_object)
