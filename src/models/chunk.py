import os
import sys

from dataclasses import dataclass
from typing import Optional

@dataclass
class SemanticChunk:
    chunk_id : str
    section_id : str
    section_title : str
    content : str
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    token_count: Optional[int] = None