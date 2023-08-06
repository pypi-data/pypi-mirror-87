"""Fixer callbacks for pydicom"""
from contextlib import contextmanager
from copy import copy

import pydicom
from pydicom import config as pydicom_config
from pydicom.datadict import dictionary_VR
from pydicom.datadict import get_entry
from pydicom.multival import MultiValue
from pydicom.charset import default_encoding
from pydicom.util.fixer import fix_mismatch_callback
from pydicom import values


def backslash_in_VM1_string_callback(raw_elem, encodings=None):
    """A callback function to fix the value of RawDataElement with VM=1 and VR of type
    string that contains the an invalid ``\\`` character (``\\`` is the array delimiter
    in Dicom standard).
    """
    if not encodings:
        encodings = [default_encoding]
    elif isinstance(encodings, str):
        encodings = [encodings]

    # Only fix VM for tag supported by get_entry
    try:
        vr, vm, _, _, _ = get_entry(raw_elem.tag)
    except KeyError:
        return raw_elem

    # only fix if VR matches
    if vr == raw_elem.VR and vm == "1":
        # only fix if is a VR string
        if vr not in [
            "UT",
            "ST",
            "LT",
            "FL",
            "FD",
            "AT",
            "OB",
            "OW",
            "OF",
            "SL",
            "SQ",
            "SS",
            "UL",
            "OB/OW",
            "OW/OB",
            "OB or OW",
            "OW or OB",
            "UN",
            "US",
        ]:
            value = pydicom.values.convert_value(raw_elem.VR, raw_elem)
            if isinstance(value, MultiValue) and len(value) > 1:
                # replace \\ byte with /
                for encoding in encodings:
                    try:
                        raw_elem = raw_elem._replace(
                            value=raw_elem.value.decode(encoding)
                            .replace("\\", "/")
                            .encode(encoding)
                        )
                        break
                    except Exception:
                        continue

    return raw_elem


def handle_none_VR(raw_elem):
    """Mirror the handling of pydicom DataElement_from_raw when VR is None but set
    VR = 'UN' for public tag that are not in the pydicom dictionary instead of raising
    a KeyError."""
    VR = raw_elem.VR
    if VR is None:
        try:
            VR = dictionary_VR(raw_elem.tag)
        except KeyError:
            # just read the bytes, no way to know what they mean
            if raw_elem.tag.is_private:
                # for VR for private tags see PS3.5, 6.2.2
                if raw_elem.tag.is_private_creator:
                    VR = "LO"
                else:
                    VR = "UN"

            # group length tag implied in versions < 3.0
            elif raw_elem.tag.element == 0:
                VR = "UL"
            else:
                VR = "UN"
        raw_elem = raw_elem._replace(VR=VR)

    # Testing that conversion can be performed with new VR,
    # If not, set it to OB
    try:
        values.convert_value(raw_elem.VR, raw_elem)
    except Exception:
        raw_elem = raw_elem._replace(VR="OB")

    return raw_elem


def handle_un_VR(raw_elem):
    """Mirror the handling of pydicom DataElement_from_raw function when VR is UN but set
    VR = 'OB' when decoding value with inferred VR raises."""
    VR = raw_elem.VR
    if (
        VR == "UN"
        and not raw_elem.tag.is_private
        and pydicom_config.replace_un_with_known_vr
    ):
        # handle rare case of incorrectly set 'UN' in explicit encoding
        # see also DataElement.__init__()
        if (
            raw_elem.length == 0xFFFFFFFF
            or raw_elem.value is None
            or len(raw_elem.value) < 0xFFFF
        ):
            try:
                VR = dictionary_VR(raw_elem.tag)
                raw_elem = raw_elem._replace(VR=VR)
            except KeyError:
                pass

        # Testing that conversion can be performed with new VR,
        # If not,  set it to OB
        try:
            values.convert_value(raw_elem.VR, raw_elem)
        except Exception:
            raw_elem = raw_elem._replace(VR="OB")

    return raw_elem


def converter_exception_callback(raw_elem, **kwargs):
    """A callback function to catch NotImplementedError when raw_elem contains an
    invalid VR."""

    if raw_elem.VR is None:
        return handle_none_VR(raw_elem)

    if raw_elem.tag == 0x00080005 and raw_elem.VR == "UN":
        # Handle special case when 0x00080005 (Specific Character Set) is UN which
        # prohibits decoding text VR.
        raw_elem = raw_elem._replace(VR="CS")
        return raw_elem

    try:
        raw_elem = fix_mismatch_callback(raw_elem, **kwargs)
    except NotImplementedError:
        # Handle invalid VR for which a converters are not defined
        if raw_elem.tag in [0xFFFEE0DD]:
            # 0xFFFEE0DD is a sequence delimiter with VR='NONE' in pydicom,
            # To handle the edge case where an extra sequence delimiter is
            # found in the DataSet setting its VR to OB to avoid conversion (setting
            # it to UN or None will raise because VR inference will happen downstream).
            raw_elem = raw_elem._replace(VR="OB")
        else:
            raw_elem = raw_elem._replace(VR="UN")
            raw_elem = handle_un_VR(raw_elem)

    return raw_elem


def fw_data_element_callback(raw_elem, tracker=None, **kwargs):
    # Retrieve pertinent kwargs
    callback = kwargs.pop("callback", None)
    fix_vr_mismatch = kwargs.pop("fix_vr_mismatch", True)
    fix_vm1_strings = kwargs.pop("fix_vm1_strings", True)
    with_VRs = kwargs.pop("with_VRs", list())
    encodings = kwargs.get("encoding", [default_encoding])
    if isinstance(encodings, str):
        encodings = [encodings]

    if tracker:
        raw_elem = tracker.track(raw_elem)

    if fix_vr_mismatch:
        raw_elem = converter_exception_callback(raw_elem, with_VRs=with_VRs)

    # currently not applying multiple fixes
    # (e.g. unknown VR and backslash in VM1 string)
    if fix_vm1_strings:
        raw_elem = backslash_in_VM1_string_callback(raw_elem, encodings=encodings)
    if callable(callback):
        raw_elem = callback(raw_elem, **kwargs)

    if tracker:
        raw_elem = tracker.release(raw_elem)

    return raw_elem


@contextmanager
def fw_pydicom_config(use_fw_callback=True, data_element_callback=None, **kwargs):
    """A contextmanager that temporarily sets pydicom.config attributes.

    Args:
        use_fw_callback (bool): whether to use the fw_data_elem_callback_function
            as pydicom.config.data_element_callback (default True). The function
            fixes the following:
                1) RawDataElements elements with invalid VR.
                2) RawDataElements with unknown public tag.
                3) RawDataElements elements that are not translatable with their provided VRs.
                4) RawDataElements with a DICOM dictionary VM and string vr containing ``\\``.
        data_element_callback: a callable function to be run on all DataElements.
            If use_fw_callback is set to True, this function will be
            called after the other pre-defined callbacks, otherwise this function
            will be set as pydicom.config.data_element_callback
        **kwargs: kwargs to be set as pydicom.config.data_element_callback_kwargs and
            as pydicom.config attributes.

    Returns:
        No return value. The callback function will return either
        the original RawDataElement instance, or one with a fixed VR or value.
    """
    pydicom_backup_config = dict()

    if use_fw_callback or callable(data_element_callback):
        # Define the data_element_callback and the data_element_callback_kwargs
        # to be pass to pydicom.config
        callback_kwargs = {
            k: v for k, v in kwargs.items() if not hasattr(pydicom_config, k)
        }
        if use_fw_callback:
            kwargs["data_element_callback"] = fw_data_element_callback
            # Set defaults
            callback_kwargs["with_VRs"] = callback_kwargs.get(
                "with_VRs", ["PN", "DS", "IS"]
            )
            if callable(data_element_callback):
                callback_kwargs["callback"] = data_element_callback
        elif callable(data_element_callback):
            kwargs["data_element_callback"] = data_element_callback

        kwargs["data_element_callback_kwargs"] = callback_kwargs

    # update pydicom.config
    for key, value in kwargs.items():
        if hasattr(pydicom_config, key):
            config_value = getattr(pydicom_config, key)
            if value != config_value:
                pydicom_backup_config[key] = config_value
                setattr(pydicom_config, key, value)
    try:
        yield

    finally:
        # restore pydicom config
        for key, value in pydicom_backup_config.items():
            setattr(pydicom_config, key, value)
