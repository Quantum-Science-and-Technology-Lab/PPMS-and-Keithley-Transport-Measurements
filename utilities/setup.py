import MultiPyVu as mpv
from enum import Enum, auto

class MVUInstrumentList(Enum):
    DYNACOOL = auto()
    PPMS = auto()
    PPMSMVU = auto()
    VERSALAB = auto()
    MPMS3 = auto()
    OPTICOOL = auto()
    na = auto()


mpv.instrument.InstrumentList = MVUInstrumentList
