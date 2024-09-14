from dataclasses import dataclass
from typing import Optional, List
import re
import math 

@dataclass
class TimedRow:
    start_time: int # seconds
    text: str

    def __eq__(self, other):
        return self.start_time == other.start_time and self.text == other.text


@dataclass
class TimedLyrics:
    rows: List[TimedRow]

    @classmethod
    def from_raw_data(cls, raw_data):
        pattern = re.compile(r'\[(\d{2}):(\d{2})\.(\d{2})\] (.+)')
        
        rows = []
        for match in pattern.findall(raw_data):
            minutes, seconds, centiseconds, text = match
            start_time = int(minutes) * 60 + int(seconds) + int(centiseconds) / 100
            rows.append(TimedRow(start_time=int(start_time), text=text))
        
        return cls(rows=rows)
    
    def __eq__(self, other):
        for i, row in enumerate(self.rows):
            if row != other.rows[i]:
                return False
        return True


@dataclass
class SongInformation:
    title: str
    lyrics: str
    album: str
    artist: str
    current_time: float
    timed_lyrics: Optional[TimedLyrics] = None

    @classmethod
    def from_json(cls, json_data):
        # Parse the JSON data and create a new instance of the class
        title = json_data.get('title')
        lyrics = json_data.get('lyrics')
        album = json_data.get('album')
        artist = json_data.get('artist')
        current_time = json_data.get('current_time')
        return cls(title, lyrics,album, artist ,current_time)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            
            return (
                self.title.lower() == other.title.lower() and
                self.album.lower() == other.album.lower() and
                self.artist.lower() == other.artist.lower() and
                math.fabs(self.current_time - other.current_time) < 1 and
                self.timed_lyrics == other.timed_lyrics and
                (self.lyrics == None or other.lyrics == None or self.lyrics.lower() == other.lyrics.lower()) 
            )
        return False
    
    def get_current_and_next_lines(self):
        if self.timed_lyrics is None:
            return None, None
        for i, row in enumerate(self.timed_lyrics.rows):
            if row.start_time > self.current_time:
                return self.timed_lyrics.rows[i - 1], row
        return None, None