#!/usr/bin/env python
'''
This example runs the calibration process for a HD PPM
It products a calibrated PPM and a calibration file for later use

########### VERSION HISTORY ###########

05/04/2019 - Andy Norrie     - First Version

########### INSTRUCTIONS ###########

1- Connect the PPM on LAN and power up
2- Connect the Keithley 2460 until on LAN, power up and check its IP address
3- Connect the calibration switch unit to the output ports of the PPM and Keithley

####################################
'''

# Global resources
from time import sleep,time
import datetime
import logging,os
import sys

# Quarch device control
from quarchpy.device import *

# Calibration control
#from quarchpy.calibration import *
from quarchpy.calibration.keithley_2460_control import *
from quarchpy.calibration.QTL1944 import *
from quarchpy.calibration.QTL2347 import *
from quarchpy.calibration.calibrationConfig import *
# UI functions
from quarchpy.user_interface import *
# TestCenter functions
from quarchpy.utilities import TestCenter

# Devices that will show up in the module scan dialog
scanFilterStr = ["QTL1999", "QTL1995", "QTL1944", "QTL2312","QTL2098"]

# Performs a standard calibration of the PPM
def runCalibration (loadAddress=None, calPath=None, moduleAddress=None, logLevel="warning", calAction=None, extra_args=None):

    myPpmDevice = None

    try:
        # Display the app title to the user
        printText("********************************************************")
        printText("          Quarch Technology Calibration System")
        printText("          (C) 2019-2020, All rights reserved")
        printText("          V" + quarchpy.calibration.calCodeVersion)
        printText("********************************************************")
        printText("")

        # Process parameters
        calPath = get_check_valid_calPath(calPath)
        setup_logging(logLevel)

        calibrationResources["moduleString"] = moduleAddress
        calibrationResources["loadString"] = loadAddress

        #


        while True:

            if myPpmDevice == None:

                # Connect to the module
                while True:

                    # If no address specified, the user must select the module to calibrate
                    if (calibrationResources["moduleString"] == None):
                        deviceString = userSelectDevice(scanFilterStr=scanFilterStr, nice=True,message="Select device for calibration")
                        # quit if necessary
                        if deviceString == 'quit':
                            printText("no module selected, exiting...")
                            sys.exit(0)
                        else:
                            calibrationResources["moduleString"] = deviceString               

                    try:
                        printText("Selected Module: " + calibrationResources["moduleString"])
                        myPpmDevice = quarchDevice(calibrationResources["moduleString"])
                        break
                    except:
                        printText("Failed to connect to "+str(calibrationResources["moduleString"]))
                        calibrationResources["moduleString"] = None

                serialNumber = myPpmDevice.sendCommand("*SERIAL?")
                success = False
                # Identify and create a power module object
                if ('1944' in serialNumber):
                    # create HD Power Module Object
                    dut = QTL1944(myPpmDevice)
                    success = True
                elif ('2098' in serialNumber):
                    # this is a Power Analysis Module, we need to detect the fixture
                    fixtureId = myPpmDevice.sendCommand("read 0xA401")
                    if ('2347' in fixtureId):
                        dut = QTL2347(myPpmDevice)
                        success = True
                    if ('2525' in fixtureId):
                        dut = QTL2525(myPpmDevice)
                        success = True
                if (success == False):
                    raise ValueError("ERROR - Serial number not recogised as a valid power module")

                # If we're in testcenter setup the test
                if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
                    # Set up database logging
                    TestCenter.setup("Quarch_Internal", "Internal","Login=-","Password=-")
                    # Store the serial number from the DUT scan for logging and verification
                    TestCenter.testPoint ("Quarch_Internal.StoreSerial","Serial="+dut.calObjectSerial);
                    idnStr=str(dut.idnStr).replace("\r\n","|")
                    TestCenter.testPoint ("Quarch_Internal.StoreDutActualIdn","Idn="+idnStr)

            # If no calibration action is selected, request one
            if (calAction == None):
                if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
                    exit()
                else:
                    calAction = show_action_menu(calAction)
            if (calAction == 'quit'):
                sys.exit(0)
            elif ('calibrate' in calAction) or ('verify' in calAction):

                # get CalibrationTime
                calTime = datetime.datetime.now()

                # open report for writing and write system header
                fileName = calPath + "\\" + dut.filenameString + "_" + calTime.strftime("%d-%m-%y_%H-%M") + "-" + calAction + ".txt"
                printText("")
                printText("Report file: " + fileName)
                reportFile = open(fileName, "a+",encoding='utf-8')
                reportFile.write("\n")
                reportFile.write("Quarch Technology Calibration Report\n" if "cal" in str(calAction).lower() else "Quarch Technology Verification Report\n")
                reportFile.write("\n")
                reportFile.write("---------------------------------\n")
                reportFile.write("\n")
                reportFile.write("System Information:\n")
                reportFile.write("\n")
                try:
                    reportFile.write("QuarchPy Version: " + str(pkg_resources.get_distribution("quarchpy").version) + "\n")
                except:
                    reportFile.write("QuarchPy Version: unknown\n")
                reportFile.write("Calibration Version: " + str(quarchpy.calibration.calCodeVersion) + "\n")
                reportFile.write("Calibration Time: " + str(calTime.replace(microsecond=0)) + "\n")
                reportFile.write("\n")
                reportFile.write("---------------------------------\n")
                reportFile.write("\n")
                reportFile.flush()

                # get required instruments etc
                reportFile.write("Device Specific Information:\n")
                reportFile.write("\n")
                reportFile.write(dut.specific_requirements())
                reportFile.write("\n")
                reportFile.write("---------------------------------\n")
                reportFile.write("\n")
                reportFile.flush()
    
                # Perform the Calibration or Verification
                result = dut.calibrateOrVerify(calAction,reportFile)

                reportFile.close()

            # End of Loop
            if 'calibrate' in calAction:
                # if we have passed calibration, move on to verification
                if result is True:
                    calAction = 'verify'
                else:
                    if User_interface.instance == "testcenter":
                        TestCenter.testPoint("Quarch_Internal.storeMessage", "Message=Calibration Failed, Verification skipped.")
                        TestCenter.testPoint ("Quarch_Internal.ResultDialog","Test=Calibration and Verification: v" + str(quarchpy.calibration.calCodeVersion), "Notes=Calibration and Verification Passed")
                        return
                    else:
                        printText("Not verifying this module because calibration failed")
                        calAction = None
            elif 'verify' in calAction:
                # return is needed for testcenter
                if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
                    return
                # otherwise go back to menu
                else:
                    calAction = None
            elif 'select' in calAction:
                calAction = None
                myPpmDevice.closeConnection()
                myPpmDevice = None
                calibrationResources["moduleString"] = None
            else:
                calAction = None

    except Exception as thisException:
        try:
            dut.close_all()
            myPpmDevice.closeConnection()
        # Handle case where exception may have been thrown before instrument was set up
        except:
            pass
        logging.error(thisException)

        raise thisException


def setup_logging(logLevel):
    # check log file is present or writeable
    numeric_level = getattr(logging, logLevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % logLevel)
    logging.basicConfig(level=numeric_level)


def get_check_valid_calPath(calPath):
    inputOK = False
    while inputOK is False:
        if (calPath is None):
            calPath = os.path.expanduser("~")
            calPath = requestDialog("Enter Report Path",
                                    "Enter the desired save path for the calibration report. Leave blank to defaut to [" + calPath + "] :",
                                    desiredType="path", defaultUserInput=os.path.expanduser("~"))

        if (os.path.isdir(calPath) == False):
            printText("Supplied calibration path is invalid: " + calPath)
            inputOK = False
            calPath = None
        else:
            inputOK = True
    return calPath


def show_action_menu(calAction):
    actionList = []
    actionList.append(["Calibrate","Calibrate the power module"])
    actionList.append(["Verify","Verify existing calibration on the power module"])
    actionList.append(["Select","Select a different power module"])
    actionList.append(["Quit","Quit"])
    calAction = listSelection("Select an action", "Please select an action to perform", actionList, nice=True, tableHeaders=["Option", "Description"], indexReq=True)
    return calAction[1].lower()

# Returns a resource from the previous calibration. This is the mechanism for getting results and similar back to
# a higher level automated script.
def getCalibrationResource (resourceName):
    try:
        return calibrationResources[resourceName]
    except Exception as e:
        printText("Failed to get calibration resource : " +str(resourceName))
        printText("Exception : " + str(e))
        return None

def main(argstring):
    import argparse
    # Handle expected command line arguments here using a flexible parsing system
    parser = argparse.ArgumentParser(description='Calibration utility parameters')
    parser.add_argument('-a', '--action', help='Calibration action to perform', choices=['calibrate', 'verify'], type=str.lower)
    parser.add_argument('-m', '--module', help='IP Address or netBIOS name of power module to calibrate', type=str.lower)
    parser.add_argument('-i', '--instr', help='IP Address or netBIOS name of calibration instrument', type=str.lower)
    parser.add_argument('-p', '--path', help='Path to store calibration logs', type=str.lower)
    parser.add_argument('-l', '--logging', help='Level of logging to report', choices=['warning', 'error', 'debug'], type=str.lower,default='warning')
    parser.add_argument('-u', '--userMode',  help=argparse.SUPPRESS,choices=['console','testcenter'], type=str.lower,default='console') #Passes the output to testcenter instead of the console Internal Use
    args, extra_args = parser.parse_known_args(argstring)
    
    # Create a user interface object
    thisInterface = User_interface(args.userMode)

    # Call the main calibration function, passing the provided arguments
    return runCalibration(loadAddress=args.instr, calPath=args.path, moduleAddress=args.module, logLevel=args.logging, calAction=args.action, extra_args=extra_args)

#Command to run from terminal.
#python -m quarchpy.calibration -mUSB:QTL1999-01-002 -acalibrate -i192.168.1.210 -pC:\\Users\\sboon\\Desktop
if __name__ == "__main__":
    #main (["-mTCP:1999-01-002", "-averify",  "-pC:\Users\Public\Documents\calibrationReports"])
    main (sys.argv[1:])