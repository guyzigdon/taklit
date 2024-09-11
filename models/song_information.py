from dataclasses import dataclass

@dataclass
class SongInformation:
    title: str
    lyrics: str
    current_time: str
    @classmethod
    def from_json(cls, json_data):
        # Parse the JSON data and create a new instance of the class
        title = json_data.get('title')
        lyrics = json_data.get('lyrics')
        current_time = json_data.get('current_time')
        return cls(title, lyrics, current_time)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.title.lower() == other.title.lower() and
                self.lyrics.lower() == other.lyrics.lower() and
                self.current_time.lower() == other.current_time.lower()
            )
        return False