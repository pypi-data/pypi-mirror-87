from .client import ArchiverDataClient
from .utils import iso_to_epoch
from .utils import epoch_to_iso
from .utils import parse_dt
from .utils import datetime_with_timezone
from .utils import is_dst
from .utils import standardize_datetime
from .utils import printlog

def dformat(*args, **kws):
    """Return ISO8601 format of date time.

    Input up to 7 arguments as year, month, day, hour, minute, second,
    millisecond, it is recommended always input year, month, day, hour,
    minute, second and millisecond as 0 if not input.
    """
    return standardize_datetime(args, **kws)


FRIBArchiverDataClient = ArchiverDataClient(
    "http://epicsarchiver0.ftc:17668")


__all__ = [
    "iso_to_epoch", "epoch_to_iso",
    "parse_dt",
    "datetime_with_timezone",
    "is_dst",
    "standardize_datetime",
    "dformat",
    "printlog"
]
