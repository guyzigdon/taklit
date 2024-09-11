from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

@dataclass
class VinylInformation:
    artist: str
    album_name: str
    genre: str
    year: int
    tracklist: list[str] = None

    @classmethod
    def from_raw_information(cls, raw_information: Dict) -> VinylInformation:
        return cls(
            artist=raw_information["artist"],
            album_name=raw_information["album"],
            genre=raw_information["genre"],
            year=int(raw_information["year"]),
            tracklist=raw_information.get("tracklist"),
        )
    
    def __eq__(self, other: VinylInformation) -> bool:
        # compare case insensitive and each element of tracklist
        return (
            self.artist.lower() == other.artist.lower()
            and self.album_name.lower() == other.album_name.lower()
            and self.genre.lower() == other.genre.lower()
            and self.year == other.year
            and all(
                track.lower() == other_track.lower()
                for track, other_track in zip(self.tracklist, other.tracklist)
            )
        )    
