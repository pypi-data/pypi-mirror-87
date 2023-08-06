from typing import Tuple
from typing import NewType
from typing import NamedTuple



class KastenPacked(bytes):
    """Raw Kasten bytes that have not yet been passed through a KastenGenerator"""


class KastenChecksum(bytes):
    """hash or checksum of a Kasten object"""

