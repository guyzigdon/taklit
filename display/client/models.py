from typing import Optional

from pydantic import BaseModel


class GlobalData(BaseModel):
    album: Optional[str] = None
    artist: Optional[str] = None
