'''
Implements a cross platform system for scanning and querying system resources.

########### VERSION HISTORY ###########

06/05/2019 - Andy Norrie    - First version

####################################
'''

import logging
import platform as pt
import os
from sys import platform
import sys
import time

from quarchpy.disk_test.dtsComms import DTSCommms
from quarchpy.disk_test.dtsGlobals import dtsGlobals
from quarchpy.user_interface import *
from quarchpy.disk_test.Drive_wrapper import DriveWrapper

# from quarchpy.disk_test.driveTestCore import notifyChoiceOption, sendMsgToGUI, checkChoiceResponse, setChoiceResponse

# to make input function back compatible with Python 2.x
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

# defining this here means we will never have to differentiate
if platform == "win32":
    from quarchpy.disk_test.lspci import WindowsLSPCI as lspci
    from quarchpy.disk_test.sasFuncs import WindowsSAS as sasDET


else:
    from quarchpy.disk_test.lspci import LinuxLSPCI as lspci
    from quarchpy.disk_test.sasFuncs import LinuxSAS as sasDET


class HostInformation:
    # creating new (private) class instance
    __mylspci = lspci()
    __mySAS = sasDET()
    internalResults = {}

    def __init__(self):
        self.comms = DTSCommms()
        self.device_list = []

    '''
    Lists physical drives on the system, returning them in the form "{drive-type:identifier=drive description}"
    '''

    def list_physical_drives(self, drive_type, search_params=None):
        filter_drives = True

        # Get any additional parameters for the search
        if search_params is not None:
            if "filter_drives" in search_params:
                filter_drives = search_params["filter_drives"]

        # PCIE devices are returned with an identifier number as the PCIe slot ID
        if drive_type.lower() == "pcie":
            pcie_scan_data = self.__mylspci.getPcieDeviceList()
            # Loop through PCIe results, pick only those matching the class code of a storage controller ([01xx]
            for pcie_name, pcie_device in pcie_scan_data.items():
                if "[01" in pcie_device["class"]:
                    # Add the device address and description to the dictionary
                    drive = DriveWrapper(identifier=pcie_device["slot"], drive_type="pcie", drive_path="No path",
                                         description=pcie_device["vendor"] + ", " + pcie_device["device"],
                                         all_info=pcie_device)
                    self.device_list.append(drive)

        elif drive_type.lower() == "sas" or drive_type.lower() == "sata":
            sas_scan_data = self.__mySAS.getSasDeviceList()
            for sas_name, sas_device in sas_scan_data.items():
                # windows interpretation
                if platform == "win32":
                    if "description" in sas_device:
                        # windows version of sas
                        if "Disk drive" in sas_device["description"]:

                            drive = DriveWrapper(identifier=sas_device["name"], drive_type="Unknown",
                                                 description=sas_device["model"], drive_path=sas_device["deviceid"],
                                                 all_info=sas_device)
                            self.device_list.append(drive)

                elif platform == "linux" or platform == "linux2":
                    if "ubuntu" in pt.version().lower():
                        # {'ST1000LM024 HN-M': {'Device_id': '[2:0:0:0]', 'disk': 'disk', 'vendor': 'ATA',
                        # 'Model': 'ST1000LM024 HN-M', 'Rev': '0001', 'drive_path': '/dev/sda', 'storage_size': '1.00TB'},
                        drive = DriveWrapper(identifier=sas_device["Model"], drive_type="sas",
                                             description="{0} : {1} {2}".format(sas_device["vendor"],
                                                                                sas_device["Model"], sas_device["Rev"]),
                                             drive_path=sas_device["drive_path"], all_info=sas_device)
                        self.device_list.append(drive)

                    else:

                        drive = DriveWrapper(identifier=sas_device["name"], drive_type="sas",
                                             description="{0} : {1}".format(sas_device["vendor"], sas_device["model"]),
                                             drive_path=sas_device["name"], all_info=sas_device)
                        self.device_list.append(drive)



    '''
    Returns a dictionary of status elements for the given device.
    '''

    def get_device_status(self, device_id):
        # If a PCIe device
        if device_id.find("pcie") == 0:
            # Get the status of the PCIe device and return it
            return self.__mylspci.getPcieDeviceDetailedInfo(devicesToScan=device_id)
        else:
            # currently would be in form sas:nameofDrive
            return self.__mySAS.getSasDeviceDetailedInfo(devicesToScan=device_id)

    '''
    Verifies that the PCIe link stats are the same now as they were at the start of the test

    driveId=ID string of the drive to test
    '''

    def verify_drive_link(self, driveId, expected_speed=None, mapping_mode=None):
        # Get the expected stats
        if not expected_speed:
            expected_speed = self.internalResults[driveId + "_linkSpeed"]
        if "auto" in str(expected_speed).lower():
            expected_speed = self.internalResults[driveId + "_linkSpeed"]

        # Get the current stats
        linkSpeed, linkWidth = self.__mylspci.getPcieLinkStatus(driveId, mapping_mode)

        expected_speed = str(expected_speed).strip()

        changeDetails = "Was: " + expected_speed + " Now: " + linkSpeed

        self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "Debug", changeDetails,
                                                              sys._getframe().f_code.co_name, uId=""))

        # if the speed and width is the same
        return str(linkSpeed) == str(expected_speed)

    def verify_drive_lane_width(self, driveId, expected_width=None, mapping_mode=None):
        # Get the expected stats
        if not expected_width:
            expected_width = self.internalResults[driveId + "_linkWidth"]
        if "auto" in str(expected_width).lower():
            expected_width = self.internalResults[driveId + "_linkWidth"]

        # Get the current stats
        linkSpeed, linkWidth = self.__mylspci.getPcieLinkStatus(driveId, mapping_mode)

        expected_width = str(expected_width).strip()

        changeDetails = "Was: " + expected_width + " Now: " + linkWidth

        self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "Debug", changeDetails,
                                                              sys._getframe().f_code.co_name, uId=""))

        # if the speed and width is the same
        return str(linkWidth) == str(expected_width)


    '''
    Checks if the given device string is visible on the bus
    '''

    def isDevicePresent(self, deviceStr, mappingMode, driveType):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        device_list = []
        # Get current device list
        if "pcie" in str(driveType).lower():
            device_list = self.__mylspci.getPcieDevices(mappingMode)
        else:
            device_list = self.__mySAS.getSasDeviceList()

        os.chdir(cwd)

        # Loop through devices and see if our module is there
        for device in device_list:
            if str(deviceStr).strip() in str(device).strip():
                return True

        return False

    def getDriveList(self, mappingMode):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        # Get current device list
        deviceList = self.__mylspci.getPcieDevices(mappingMode)
        deviceList += self.__mySAS.getSasDeviceList()
        # printText(deviceList)
        os.chdir(cwd)
        return deviceList

    '''
        Checks if the specified device exists in the list
        '''

    def devicePresentInList(self, deviceList, deviceStr):
        for pciStr in deviceList:
            if deviceStr in pciStr:
                return True
        return False

    def get_sas_drive_det_cmd(self):
        return sasDET.return_device_det_cmd()

    def pick_drive_target(self, drive_type, resourceName=None, ret_value=False, mappingMode=None, report_dict=[]):

        # Resetting the choice and any drives previously found
        dtsGlobals.choiceResponse = None
        self.device_list.clear()

        # Check to see if the pcieMappingMode resource string is set
        if not mappingMode:
            mappingMode = False
        deviceStr = "NO_DEVICE_STRING"
        # deviceList = self.__mylspci.getPcieDevices(mappingMode)
        device_dict_sas = None
        device_dict_pcie = None
        device_dict = None

        # Return dictionary of the drives
        self.get_drives(drive_type)

        self.comms.sendMsgToGUI(self.comms.create_request_gui(title="user selection",
                                                              description="Choose drive connected to quarch module",
                                                              window_type="SelectionGrid", window_mode="drive",
                                                              dict_of_drives=self.device_list))

        while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
            time.sleep(0.25)

        if dtsGlobals.choiceResponse is None:
            return 0

        choice = str(dtsGlobals.choiceResponse)
        # printText("choice from user was : " + choice)

        selection = choice.split("::")
        # order should be choiceResponse::xyz
        selection = selection[1]

        # rescan is the only responce we dont want printed at the moment. If others are needed make a global list.
        if "rescan" not in selection:
            printText("Response from drive selection was : " + selection.replace("\n", "").replace("\r", ""),
                      fillLine=True, terminalWidth=80)
        logging.debug("Response from drive selection was : " + choice)
        # exit on 'choice-abort' or if user stopped tests
        if "choice-abort" in selection or dtsGlobals.continueTest is False:
            printText("No item selected, test aborted. Waiting for new test start..\n")
            return None
        elif "rescan" in selection:
            return self.pick_drive_target(drive_type, resourceName=resourceName, ret_value=ret_value)

        # Validate selection
        found = False
        device_obj = None

        for drive in self.device_list:
            if selection.strip() == drive.identifier_str:
                device_obj = drive
                found = True
                break

        if not found:
            return 0

        if "pcie" in drive_type:
            linkSpeed, linkWidth = self.__mylspci.getPcieLinkStatus(deviceStr, mappingMode)
        else:
            linkSpeed = None
            linkWidth = None

        ret_dict = {"key_return": device_obj.identifier_str, "value_return": device_obj}

        report_dict["drive"] = device_obj.__str__()

        return ret_dict

    def store_initial_drive_stats(self, drive, mapping_mode=False):
        if str(drive.drive_type).lower() == "pcie":
            self.internalResults[drive.identifier_str + "_linkSpeed"], self.internalResults[
                drive.identifier_str + "_linkWidth"] = self.__mylspci.getPcieLinkStatus(drive.identifier_str, mapping_mode)

    def get_drive_from_choice(self, selection, report_dict=[]):
        # Validate selection
        found = False
        device_obj = None

        for drive in self.device_list:
            if selection.strip() == drive.identifier_str:
                device_obj = drive
                found = True
                break

        if not found:
            return None

        report_dict["drive"] = device_obj.description
        report_dict["Conn_type"] = device_obj.drive_type
        report_dict["drive_path"] = device_obj.drive_path

        return device_obj

    def get_drives(self, drive_type):
        self.device_list = []

        if "all" in drive_type:
            self.list_physical_drives("sas")
            self.list_physical_drives("pcie")

        else:
            self.list_physical_drives(drive_type)

        if not self.device_list:
            printText("ERROR - No devices found to display")

        return

    '''
    Checks if the script is runnin under admin permissions
    '''

    def checkAdmin(self):
        if self.__mylspci.is_admin_mode() == False:
            logging.critical("Not in Admin mode\nExiting Program")
            quit()

    def getPcieLinkStatus(self, deviceStr, mappingMode):
        return self.__mylspci.getPcieLinkStatus(deviceStr, mappingMode)


