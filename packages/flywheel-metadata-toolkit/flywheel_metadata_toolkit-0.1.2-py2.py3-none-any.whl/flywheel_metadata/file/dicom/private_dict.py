"""Module to add private tags to pydicom private dictionaries"""


# Additional private tags - formatted as pydicom private_dictionaries
# TODO: submit to pydicom
private_dictionaries = {
    "SIEMENS MI RWVM SUV": {
        "0041xx01": ("CS", "1", "SUV Decay Correction Method", ""),  # noqa
    },
    "SIEMENS PET DERIVED": {
        "0075xx01": ("US", "1", "Volume Index", ""),
        "0075xx02": ("IS", "1", "Time Slice Duration", ""),
        "0075xx03": ("SQ", "1", "Frame Reference Time Sequence", ""),
    },
    "SIEMENS MED RTSTRUCT": {
        "0063xx32": ("DS", "3", "GTV Marker Position", ""),
    },
    "SIEMENS MED PT MU MAP": {
        "0071xx01": ("UI", "1", "SOP Class of Source", ""),
        "0071xx02": ("UI", "1", "Related Mu Map Series", ""),
    },
    "SIEMENS MED PT": {
        "0071xx21": ("UI", "1", "Reference To Registration", ""),
        "0071xx22": ("DT", "1", "Decay Correction DateTime", ""),
        "0071xx23": ("US", "16", "Registration Matrix", ""),
        "0071xx24": ("CS", "1", "Table Motion", ""),
        "0071xx25": ("FD", "1", "Lumped Constant", ""),
        "0071xx26": ("CS", "1", "Histogramming Method", ""),
    },
    "SIEMENS MED ORIENTATION RESULT": {
        "0027xx05": ("CS", "1", "Cardiac Orientation Value", ""),
    },
    "SIEMENS MED MI": {
        "0067xx01": ("LT", "1", "MI Scan ID", ""),
        "0067xx02": ("LO", "1", "Scanner Console Generation", ""),
        "0067xx03": ("OB", "1-n", "Recon Parameters", ""),
        "0067xx04": ("LO", "1", "Group Reconstruction ID", ""),
        "0067xx05": ("LO", "1", "Device IVK", ""),
        "0067xx14": ("LO", "1", "Raw Data Description", ""),
        "0067xx16": ("UI", "1-n", "Raw Data Series Instance UIDs", ""),
        "0067xx17": ("UI", "1-n", "Raw Data Referenced Series Instance UIDs", ""),
    },
    "SIEMENS MED MEASUREMENT": {
        "0027xx01": ("DS", "3", "Percist Cylinder Position", ""),
        "0027xx02": ("DS", "3", "Percist Cylinder Axis", ""),
        "0027xx03": ("DS", "1", "Percist Cylinder Radius", ""),
        "0027xx04": ("LT", "1", "Isocontour Threshold", ""),
        "0027xx05": ("LO", "1", "Auto Created", ""),
        "0027xx06": ("CS", "1", "Finding Creation Mode", ""),
        "0027xx07": ("DS", "1", "Pet Segmentation Threshold", ""),
        "0027xx08": ("DS", "12", "Change Rate", ""),
        "0027xx09": ("DS", "1", "Volume Doubling Time", ""),
        "0027xx10": ("OB", "1-n", "Change Rates", ""),
    },
    "SIEMENS MED BRAIN ORIENTATION DATA": {
        "0027xx06": ("CS", "1", "Brain Orientation Value", ""),
    },
}
