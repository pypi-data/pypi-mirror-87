from enum import Enum
from holon.headers import Header
from holon.http import HTTPMessage, HTTPMethod
from holon.media_types import MediaType
from holon.principles import Principle
from holon.writing import autocomplete
from holon.ietf.rfc2119 import Keyword
from pydantic import BaseModel
from typing import List, Optional


@autocomplete
class PrincipleRule(BaseModel):
    keyword: Keyword
    principle: Principle


@autocomplete
class HeaderRule(BaseModel):
    keyword: Keyword
    header: Header
    http_method: Optional[HTTPMethod] = None
    message_type: Optional[HTTPMessage] = None


@autocomplete
class MediaTypeRule(BaseModel):
    keyword: Keyword
    media_type: MediaType
    message_type: Optional[HTTPMessage] = None


@autocomplete
class APIDesignSystem(BaseModel):
    principles: Optional[List[PrincipleRule]] = []
    headers: Optional[List[HeaderRule]] = []
    media_types: Optional[List[MediaTypeRule]] = []
