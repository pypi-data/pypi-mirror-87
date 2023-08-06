

"""Compile Kasten elements into a packed (msgpack) sequence.

KastenPacked sequences are prepared sequences used by Kasten instances and
their generators to apply rules and validation to Kasten.

Note that encryption and signing are not handled by anything in kasten, only
hash authentication is dependending on the generator used.

Packed bytes structure:
0: type: str: 4bytesmax
1: enc-mode: int: 0, 1, 2 (0=plaintext, 1=asymmetic, 2=symmetric).
2. Timestamp: int
encrypted with specified mode:
 3. signer: bytes (max 256bits)
 4. signature: bytes (max 256bits)
 5. app_metadata: arbitrary JSON
\n
data: bytes
"""
from math import floor
from time import time

from msgpack import packb

from kasten import exceptions

from kasten.types import KastenPacked
"""
Copyright (C) <2020>  Kevin Froman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def pack(data: bytes, data_type: '',
         enc_mode: 'KastenEncryptionModeID',
         signer: bytes = None, signature: bytes = None,
         app_metadata: 'KastenSerializeableDict' = None,
         timestamp: int = None
         ) ->  KastenPacked:
    """Create KastenPacked bytes sequence but do not ID or run through generator"""

    # Ensure data type does not exceed 4 characters
    if not data_type or len(data_type) > 4:
        raise exceptions.InvalidKastenTypeLength

    # Ensure encryption mode is in [0, 100)
    try:
        enc_mode = int(enc_mode)
    except (TypeError, ValueError):
        raise exceptions.InvalidEncryptionMode
    if not enc_mode >= 0 or enc_mode >= 100:
        raise exceptions.InvalidEncryptionMode

    try:
        data = data.encode('utf8')
    except AttributeError:
        pass
    if timestamp is None:
        timestamp = floor(time())
    timestamp = int(timestamp)

    kasten_header = [data_type, enc_mode, timestamp]
    if signer:
        if signature is None:
            raise ValueError("Signer specified without signature")
        kasten_header.extend((signer, signature))
    if app_metadata is not None:
        kasten_header.append(app_metadata)

    kasten_header = packb(kasten_header) + b'\n'
    return kasten_header + data
