import xml.etree.ElementTree as ET
from quarchpy.disk_test.Custom_test_variable import CustomVariable

'''
Class to define a test point to be executed
'''


class testLine:
    '''
    Init function taking all parameters
    '''

    def __init__(self):

        # Responses to python requests
        self.user_choice = None
        self.qcs_version = None
        self.qpy_version_valid = None
        self.request_stop = None

        self.custom_variable_dict = {}
        self.is_c_var_response = False
        self.function_complete = None

        # Commands send to python
        self.lineType = None
        self.testName = None
        self.moduleName = None
        self.paramList = {}
        self.pickled_data = None

    '''
    Use an XML tree to init the testLine object.  Throws an exception of the required
    elements are not available.  Additional elements will be ignored
    '''

    def initFromXml(self, xmlTree):

        # Verify expected root node
        if xmlTree.tag != "Request":
            raise ValueError("XML tree does not contain the required root value (RemoteCommand)")

        # Get main command details
        # self.idNumber = xmlTree.find('LineNumber').text
        self.lineType = xmlTree.find('LineType').text
        self.testName = xmlTree.find('Function').text
        self.moduleName = xmlTree.find('Module').text
        self.pickled_data = None

        # Get parameter list
        newItem = xmlTree.iter()
        newItem2 = []
        for elem in newItem:
            if 'key' in elem.tag or 'value' in elem.tag:
                newItem2.append(elem.text)
                # printText (elem.text)

            if 'pickled_data' in elem.tag:
                self.pickled_data = xmlTree.find('pickled_data').text

        skipElement = ""
        # if there's any entries in the list
        if newItem2:
            for x, elem in enumerate(newItem2):
                if skipElement == x:
                    continue
                self.paramList.update({elem: newItem2[x + 1]})
                skipElement = x + 1

        # for k, v in self.paramList.items():
        #    printText(k, v)

        # Validate command data
        # if (self.idNumber == None):
        #    raise ValueError ("Remote command 'ID' not set")
        if self.lineType is None:
            raise ValueError("Remote command 'type' not set")
        if self.testName is None:
            raise ValueError("Remote command 'name' not set")
        if self.moduleName is None:
            raise ValueError("Remote command 'module' not set")
        # if (self.moduleName == None):
        #    raise ValueError ("Remote command 'module' not set")
        # if (len(self.paramList) == 0):
        #    raise ValueError ("Remote command 'parameters' not set")

    def parse_response(self, xml_tree):

        newItem = xml_tree.iter()

        for elem in newItem:
            if 'user_choice' in elem.tag:
                self.user_choice = xml_tree.find('user_choice').text
            if 'qcs_version_response' in elem.tag:
                self.qcs_version = xml_tree.find('qcs_version_response').text
            if 'qpy_version_valid' in elem.tag:
                self.qpy_version_valid = xml_tree.find('qpy_version_valid').text
            if 'request_stop' in elem.tag:
                self.request_stop = xml_tree.find('request_stop').text
            if 'function_complete' in elem.tag:
                self.function_complete = bool(xml_tree.find('function_complete').text)

            if "custom_variable_list" in elem.tag:
                self.is_c_var_response = True
                key = None
                value = None
                for sub_elem in elem:
                    # sub_elem = xml_tree.find('custom_variable_list')
                    if "name" in sub_elem.tag:
                        key = sub_elem.text
                    if "customVal" in sub_elem.tag:
                        value = sub_elem.text
                        if "auto" in str(value).lower():
                            # Resetting the variable so it uses default value
                            value = None
                if key and value:
                    self.custom_variable_dict[key] = value
