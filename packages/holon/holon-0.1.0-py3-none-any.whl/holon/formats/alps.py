from enum import Enum
from typing import Dict, ForwardRef, List, Literal, Optional, Union
from pydantic import BaseModel, root_validator
from holon.writing import autocomplete


class Format(Enum):
    TEXT = "text"
    HTML = "html"
    ASCIIDOC = "asciidoc"
    MARKDOWN = "markdown"


class DescriptorType(Enum):
    SEMANTIC = "semantic"
    SAFE = "safe"
    UNSAFE = "unsafe"
    IDEMPOTENT = "idempotent"


@autocomplete
class Doc(BaseModel):
    text: str
    href: Optional[str] = None
    format: Format = Format.TEXT


@autocomplete
class Ext(BaseModel):
    href: str


@autocomplete
class Link(BaseModel):
    rel: str
    href: str


@autocomplete
class Descriptor(BaseModel):
    """
    A 'descriptor' element defines the semantics of specific data
    elements or state transitions that MAY exist in an associated
    representation.
    """

    id: Optional[str] = None
    name: Optional[str] = None
    doc: Optional[Doc] = None
    rel: Optional[str] = None
    rt: Optional[str] = None
    type: DescriptorType = DescriptorType.SEMANTIC
    descriptors: List["Descriptor"] = []
    links: List[Link] = []

    @root_validator
    def check_id_name(cls, value):
        if value["id"] is None and value["name"] is None:
            raise Value("You must set either the id or name of a descriptor")
        return value


Descriptor.update_forward_refs()


@autocomplete
class ALPS(BaseModel):
    version: Literal["1.0"] = "1.0"
    title: Optional[str] = None
    doc: Optional[Doc] = None
    links: List[Link] = []
    descriptors: List[Descriptor] = []
