'''
Implements basic SAS information parsing, so that we can identify and check the
status of SAS/SATA devices on the host
'''

import subprocess
import platform
import time
import os
import re
import sys
import ctypes
# from abc import ABC, abstractmethod
import abc
ABC = abc.ABCMeta('ABC', (object,), {})
from quarchpy.user_interface import*

# Class for others to 'extend'
class abstractSASDet(ABC):

    @abc.abstractmethod
    def getSasDeviceList(self):
        pass


    @abc.abstractmethod
    def sortList(self, err, out):
        pass

    @abc.abstractmethod
    def is_admin_mode(self):
        pass

    def sortDeviceInfo(self, err, out, deviceInfo, devicesToScan):
        # Handle error output
        if (err):
            raise ValueError("lspci error: " + err.decode('utf-8'))
        out = out.decode('utf-8')

        # Split the output into blocks of each device (paragraph)
        blocks = out.split('\r\n\r\n')
        for desc in blocks:
            lnkStatSpeed = None
            lnkStatWidth = None
            lnkCapsSpeed = None
            lnkCapsWidth = None

            # Get the slot path of the current device
            pos = desc.find(' ')
            currDevice = desc[:pos]

            # Parse each potential section, handle missing sections and continue
            try:
                # Parse out link status
                strPos = desc.find('LnkSta:')
                statusText = desc[strPos:]
                matchObj = re.search('Speed (.*?),', statusText)
                lnkStatSpeed = matchObj.group(0)
            except:
                pass
            try:
                matchObj = re.search('Width (.*?),', statusText)
                lnkStatWidth = matchObj.group(0)
            except:
                pass
            try:
                # Parse out link capacity
                strPos = desc.find('LnkCap:')
                statusText = desc[strPos:]
                matchObj = re.search('Speed (.*?),', statusText)
                lnkCapsSpeed = matchObj.group(0)
            except:
                pass
            try:
                matchObj = re.search('Width (.*?),', statusText)
                lnkCapsWidth = matchObj.group(0)
            except:
                pass

            # Limit the devices to return, as requested
            if (devicesToScan == "all" or currDevice in devicesToScan):
                # If the device information does not already exists, create the extra stub
                if (currDevice not in deviceInfo):
                    deviceInfo[currDevice] = {}

                # Fill in the additional details
                deviceInfo[currDevice]["link_status:speed"] = lnkStatSpeed
                deviceInfo[currDevice]["link_status:width"] = lnkStatWidth
                deviceInfo[currDevice]["link_capability:speed"] = lnkCapsSpeed
                deviceInfo[currDevice]["link_capability:width"] = lnkCapsWidth
                deviceInfo[currDevice]["present"] = "true"

        # Check for any requested devices, which we did not find.  These must be marked as not present (rather than skipped)
        if (devicesToScan != "all"):
            blocks = devicesToScan.split('|')
            for currDevice in blocks:
                if currDevice not in deviceInfo:
                    deviceInfo[currDevice]["present"] = "false"

        # return the updated info structure
        return deviceInfo


class WindowsSAS(abstractSASDet):
    def __init__(self):
        self.device_detection_command = "wmic diskdrive list full"
        pass

    def return_device_det_cmd(self):
        return self.device_detection_command

    def is_admin_mode(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    '''
    Get basic information on all PCIe devices on the system.  Returned as a dictionary of dictionaries
    {nn:nn.n: {ELEMENT:DATA}}
    This is a fast way to scan the bus and see what is there before possible interrogating devices in more detail (device status and similar)
    '''

    def getSasDeviceList(self):

        # lspciPath = os.path.join(os.getcwd(), "pciutils", "lspci.exe")

        # call lspci to get a list of all devices and basic details in parable form
        proc = subprocess.Popen(["wmic", "diskdrive", "list", "full"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()
        retValues = self.sortList(err, out)

        # {"\\\\.\\PYHYSICALDRIVE0" : { "KEY":"VAL", "KEY2":"VAL2" }
        return retValues

    def sortList(self, err, out):
        SasDevices = {}

        unsorted = bytes(out).decode()

        deviceList = unsorted.split("\r\n\r\r")
        # printText(len(deviceList))

        for dev in deviceList:
            if str(dev).strip() == "":
                continue
                # printText("New Device: \r" +  dev)
            newDevice = {}
            for line in iter(dev.splitlines()):
                pos = line.find('=')
                if (pos != -1):
                    # Add the dictionary item
                    newDevice[line[:pos].lower()] = line[pos + 1:].strip()

            if ("name" in newDevice):
                SasDevices[newDevice["name"]] = newDevice

        return SasDevices


class LinuxSAS(abstractSASDet):
    def __init__(self):
        self.device_detection_command = "lsscsi -t -s -L"
        pass

    def return_device_det_cmd(self):
        return self.device_detection_command

    def is_admin_mode(self):
        if os.getuid() == 0:
            return True
        else:
            return False

    '''
    Get basic information on all PCIe devices on the system.  Returned as a dictionary of dictionaries
    {nn:nn.n: {ELEMENT:DATA}}
    This is a fast way to scan the bus and see what is there before possible interrogating devices in more detail (device status and similar)
    '''

    def getSasDeviceList(self):

        if "ubuntu" in platform.version().lower():
            # call lspci to get a list of all devices and basic details in parable form
            proc = subprocess.Popen(["lsscsi", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Execute the process
            out, err = proc.communicate()

            # will supply a dictionary
            return self.sortListUbuntu(err, bytes(out))
        else:
            # call lspci to get a list of all devices and basic details in parable form
            proc = subprocess.Popen(["lsscsi", "-t", "-s", "-L"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Execute the process
            out, err = proc.communicate()

            # will supply a dictionary
            return self.sortList(err, bytes(out))

    def sortList(self, err, out):
        SasDevices = {}
        unsorted = bytes(out).decode()

        deviceList = re.split("\[", unsorted)
        for dev in deviceList:

            if str(dev).strip() == "":
                continue
            # replace the missing bracket
            dev = "[" + dev

            newDevice = {}
            for line in iter(dev.splitlines()):
                pos = line.find('=')
                if (pos != -1):
                    # Add the dictionary item
                    newDevice[line[:pos].lower().strip()] = line[pos + 1:].strip()
                else:
                    details = re.split(r'\s{2,}', dev.strip())
                    iterator = 0
                    for detailString in details:
                        newDevice[self.getDictKey(iterator)] = detailString.strip()
                        iterator = iterator + 1

            if "sas" in newDevice["transport"].lower() or "sata" in newDevice["transport"].lower():
            # if any(x in ["sas", "sata"] for x in newDevice["transport"].lower()):
                # SasDevices[newDevice["Conn_Type"]] = newDevice
                SasDevices[newDevice["name"]] = newDevice

        # print(SasDevices)

        return SasDevices


    def getDictKey(self, iteratorValue):
        return {
            0 : "Spec",
            1 : "Disk_Type",
            2 : "Conn_Type",
            3 : "name",
            4 : "size"
        }.get(iteratorValue,"unknownDetail")

    def sortListUbuntu(self, err, out):

        SasDevices = {}
        unsorted = bytes(out).decode()

        deviceList = re.split("\[", unsorted)
        for dev in deviceList:

            if str(dev).strip() == "":
                continue
            # replace the missing bracket
            dev = "[" + dev

            newDevice = {}
            for line in iter(dev.splitlines()):
                # [5:0:0:0]    disk    VendorCo ProductCode      2.00  /dev/sdc   4.02GB

                # Removing any device with /dev/nvmex
                if "nvme" in str(line).lower():
                    continue

                details = line.strip().split(" ")
                details = [f for f in details if str(f) !=""]

                newDevice["Device_id"] = details[0]
                newDevice["disk"] = details[1]
                newDevice["vendor"] = details[2]
                newDevice["Model"] = " ".join(details[3:len(details) - 3])
                newDevice["Rev"] = details[len(details) - 3]
                newDevice["drive_path"] = details[len(details) - 2]
                newDevice["storage_size"] = details[len(details) - 1]
                SasDevices[newDevice["Model"]] = newDevice

        return SasDevices
