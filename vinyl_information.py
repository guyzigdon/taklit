from __future__ import annotations

from dataclasses import dataclass

@dataclass
class VinylInformation:
    artist: str
    album_name: str

    @classmethod
    def from_raw_information(cls, raw_information: str) -> VinylInformation:
        raw_fields = raw_information.split("\n")
        artist = VinylInformation._parse_field(raw_fields[0])
        album = VinylInformation._parse_field(raw_fields[1])
        return cls(artist, album)
    
    @staticmethod
    def _parse_field(field: str) -> str:
        return field.split(":")[1].strip()
