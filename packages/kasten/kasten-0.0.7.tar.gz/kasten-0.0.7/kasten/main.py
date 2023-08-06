"""Main Kasten object, does nothing but provide access to packed Kasten bytes and call a specified generator function"""
from msgpack import unpackb

from .types import KastenChecksum
from .types import KastenPacked
from .generator import pack
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

class Kasten:
    def __init__(self,
                 id: KastenChecksum,
                 packed_bytes: KastenPacked,
                 generator: 'KastenBaseGenerator',  # noqa
                 auto_check_generator = True):  # noqa
        if auto_check_generator:
            generator.validate_id(id, packed_bytes)
        self.id = id
        self.generator = generator
        header, data = packed_bytes.split(b'\n', 1)
        header = unpackb(header, strict_map_key=True)
        self.header = header
        self.data = data

    def check_generator(self, generator=None):
        packed = self.get_packed()
        if generator is None:
            self.generator.validate_id(self.id, packed)
        else:
            generator(self.id, packed)

    # Getters are gross, but they are used here to preserve space

    def get_packed(self) -> KastenPacked:
        return pack.pack(self.data, self.get_data_type(),
                         self.get_encryption_mode(),
                         timestamp=self.get_timestamp())

    def get_data_type(self) -> str: return self.header[0]

    def get_encryption_mode(self): return self.header[1]

    def get_timestamp(self): return self.header[2]
