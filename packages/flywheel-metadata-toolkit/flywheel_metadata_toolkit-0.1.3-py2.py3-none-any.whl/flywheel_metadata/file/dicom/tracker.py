from copy import copy

from pydicom.dataelem import RawDataElement


class RawDataElementTracker(RawDataElement):
    """A subclass of RawDataElement that adds some tracking capabilities by
    subclassing specific methods"""

    def __new__(cls, *args):  # __new__ because immutable namedtuple
        cls._original = None
        cls._final = None
        cls._events = []
        cls.set_original(*args)
        return super(RawDataElementTracker, cls).__new__(cls, *args)

    @classmethod
    def set_original(cls, *args):
        cls._original = RawDataElement(*args)

    @classmethod
    def set_final(cls, *args):
        cls._final = RawDataElement(*args)

    def _replace(self, **kwargs):
        for k, v in kwargs.items():
            self._events.append(f"Replace {k}: {getattr(self, k)} -> {v}")
        return super(RawDataElementTracker, self)._replace(**kwargs)

    def export(self):
        """Export _original, _final and _events attributes as dict"""
        return {
            "original": self._original,
            "final": self._final,
            "events": self._events,
        }


class Tracker:
    """A class to track Dicom data elements and collect tracker events"""

    def __init__(self, config=None):
        self.rde_traces = []
        self.config = config

    def track(self, raw_elem):
        """Starts tracking raw_elem and returns a RawDataElementTracker"""
        return RawDataElementTracker(*list(raw_elem._asdict().values()))

    def release(self, rdet):
        """Stops tracking raw_elem and returns a RawDataElement"""
        rdet.set_final(*list(rdet._asdict().values()))
        self.rde_traces.append(rdet.export())
        return RawDataElement(*list(rdet._asdict().values()))

    def clean(self):
        """Clear empty events"""
        self.rde_traces = [
            rde_trace for rde_trace in self.rde_traces if rde_trace["events"]
        ]

    def __str__(self):
        strings = []
        for trace in self.rde_traces:
            if trace["events"]:
                events = "\n" + "\n".join([f"\t{e}" for e in trace["events"]])
            else:
                events = "None"
            block = (
                f"- original: {trace['original']}\n"
                f"  events: {events} \n"
                f"  final: {trace['final']}\n"
            )
            strings.append(block)

        return "\n".join(strings)
