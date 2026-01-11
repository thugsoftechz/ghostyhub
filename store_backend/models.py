from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class PackageType(str, Enum):
    GAME = "game"
    EMULATOR = "emulator"
    TOOL = "tool"
    THEME = "theme"
    DRIVER = "driver"

class PackageManifest(BaseModel):
    id: str
    name: str
    version: str
    type: PackageType
    description: str
    runtime: Optional[str] = None
    permissions: List[str] = []
    signature: str
    price_usd: float = 0.0
    developer: str
    download_url: str

class SearchResult(BaseModel):
    packages: List[PackageManifest]
    total: int
