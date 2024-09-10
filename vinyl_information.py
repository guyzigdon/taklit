from __future__ import annotations

from dataclasses import dataclass

@dataclass
class VinylInformation:
    artist: str
    album_name: str
    genre: str
    year: int

    @classmethod
    def from_raw_information(cls, raw_information: str) -> VinylInformation:
        raw_fields = raw_information.split("\n")
        artist = VinylInformation._parse_field(raw_fields[0])
        album = VinylInformation._parse_field(raw_fields[1])
        genre = VinylInformation._parse_field(raw_fields[2])
        year = int(VinylInformation._parse_field(raw_fields[3]))
        return cls(artist, album, genre, year)
    
    @staticmethod
    def _parse_field(field: str) -> str:
        return field.split(":")[1].strip()
