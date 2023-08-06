"""Included generators to generate and validate Kasten objects"""
from hashlib import sha3_384
from mimcvdf import vdf_create, vdf_verify

from kasten.types import KastenPacked
from kasten.types import KastenChecksum
from kasten.exceptions import InvalidID

from ..main import Kasten
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


class KastenBaseGenerator:
    """Generators are used by Kasten to generate and verify Kasten object checksums and do any desired preperation on the data."""
    @classmethod
    def generate(cls, packed_bytes: KastenPacked) -> Kasten:
        return Kasten(sha3_384(packed_bytes).digest(), packed_bytes, cls,
                      auto_check_generator=False)

    @staticmethod
    def validate_id(hash: KastenChecksum, packed_bytes: KastenPacked) -> None:
        if not sha3_384(packed_bytes).digest() == hash:
            raise InvalidID
        return None


class KastenMimcGenerator:
    @classmethod
    def generate(cls, packed_bytes: KastenPacked, rounds: int = 5000) -> Kasten:
        return Kasten(vdf_create(packed_bytes, rounds, dec=True).to_bytes(64, "big"), packed_bytes, cls, auto_check_generator=False)

    @staticmethod
    def validate_id(hash: KastenChecksum, packed_bytes: KastenPacked, rounds = 5000) -> None:
        if not vdf_verify(packed_bytes, hash, rounds):
            raise InvalidID
        return None
