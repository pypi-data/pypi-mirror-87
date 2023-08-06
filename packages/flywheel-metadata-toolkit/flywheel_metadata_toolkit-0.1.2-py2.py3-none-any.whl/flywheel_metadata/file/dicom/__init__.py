"""Dicom metadata module"""
import logging

import pydicom
from pydicom.datadict import add_private_dict_entries

from flywheel_metadata.file.dicom.fixer import fw_pydicom_config
from flywheel_metadata.file.dicom.private_dict import private_dictionaries

log = logging.getLogger(__name__)


def load_dicom(*args, decode=True, config=None, tracker=None, **kwargs):
    """
    Load and optionally decode Dicom dataset with Flywheel pydicom configuration.

    Args:
        *args: pydicom.dcmread args.
        decode (bool): decode the dataset if True (default=True).
        config (dict): the kwargs to be passed to the fw_pydicom_config manager (default=None).
        tracker (Tracker): A Tracker instance (default=None).
        **kwargs: pydicom.dcmread kwargs.

    Returns:
        pydicom.Dataset: a pydicom Dataset.
    """
    if not config:
        config = {}

    # Getting the encoding
    # Currently needed by the backslash_in_VM1_string_callback
    # TODO: revise once https://github.com/pydicom/pydicom/pull/1218 is merged
    try:
        dcm = pydicom.dcmread(*args, **kwargs, specific_tags=[])
    # Handle DicomDirs which will except if DirectoryRecordSequence is not defined
    except AttributeError:
        dcm = pydicom.dcmread(
            *args, **kwargs, specific_tags=["DirectoryRecordSequence"]
        )
    encoding = dcm.read_encoding or dcm._character_set

    with fw_pydicom_config(tracker=tracker, encoding=encoding, **config):
        dicom_ds = pydicom.dcmread(*args, **kwargs)
        if decode:
            dicom_ds.decode()

    return dicom_ds


def extend_private_dictionaries():
    """Extend pydicom private dictionaries with flywheel_metadata.file.dicom.private_dict"""
    for private_creator, tag_dict in private_dictionaries.items():
        new_dict_items = {}
        for t, val in tag_dict.items():
            # the 2 high bytes of the element part of the tag are ignored
            tag = int(t.replace("x", "0"), 16)
            new_dict_items[tag] = val[:3]
        add_private_dict_entries(private_creator, new_dict_items)
