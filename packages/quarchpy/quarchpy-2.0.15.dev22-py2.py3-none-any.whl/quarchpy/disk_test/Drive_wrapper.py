class DriveWrapper:
    """
    Allows drive to be parsed into object for use throughout Quarchpy

    """
    def __init__(self, identifier="", drive_type="", description="", drive_path=None, link_speed=None, lane_width=None,
                 all_info=None):
        """
                Constructor for quarchDevice, allowing the connection method of the device to be specified.

                Parameters
                ----------
                identifier_str : str

                    Identifier String: Different depending on drive type and OS being used

                    Examples:
                    05:00.0         - Standard PCIe identifier, Windows and Linux
                    /PHYSICALDRIVE0 - SAS identifier for Windows
                    ....

                drive_type : {'sas', 'pcie', 'unknown'}

                    Specifies the type of Drive in use:
                    pcie        -  PCIe (NVMe) Drives.
                                (Expected to have link speed and lane width)

                    sas         -  SAS (and SATA) Drives.
                                (No current way to verify / identify lane width and link speed)

                    unknown     -  Unknown device type.
                                ( Used for windows as no current known method to identify only SAS / SATA )

                description : str, required

                    Description provided of Drive - Drive manufacturer / drive specific

                lane_width : str, optional

                    Specified only for PCIe Modules. Reports found Lane width stat of drive
                    Output of LSCPI -vv command.

                link_speed : str, optional

                    Specified only for PCIe Modules. Reports found link speed stat of drive
                    Output of LSCPI -vv command.

                """

        self.identifier_str = identifier
        self.drive_type = drive_type
        self.description = description
        self.link_speed = link_speed
        self.lane_width = lane_width
        self.drive_path = drive_path
        self.all_info = all_info


