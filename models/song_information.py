from pydantic import BaseModel, Field
from typing import Optional, List
import re
import math 
import time

class TimedRow(BaseModel):
    start_time: int # seconds
    text: str

    def __eq__(self, other):
        return self.start_time == other.start_time and self.text == other.text


class TimedLyrics(BaseModel):
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
    
    @classmethod
    def from_spotify_lyrics(cls, lyrics):
        return cls(rows=[TimedRow(start_time=int(line['startTimeMs'])/1000, text=line['words']) for line in lyrics['lines']])
    
    def __eq__(self, other):
        for i, row in enumerate(self.rows):
            if row != other.rows[i]:
                return False
        return True


class SongInformation(BaseModel):
    data_type: str = "song"
    title: str
    album: str
    artist: str
    current_time: float
    lyrics: Optional[str] = None
    timed_lyrics: Optional[TimedLyrics] = None
    live_lyrics: Optional[str] = None
    detection_time: Optional[int] = Field(default_factory=lambda: int(time.time()))

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
    
    def set_current_and_next_lines(self):
        if self.timed_lyrics is None:
            self.live_lyrics = None
            return
        for i, row in enumerate(self.timed_lyrics.rows):
            if row.start_time > self.current_time:
                self.live_lyrics = [self.timed_lyrics.rows[i - 1].text, row.text]
                return