from holon.writing import autocomplete
from pydantic import BaseModel


@autocomplete
class Header(BaseModel):
    field_name: str
    reference: str
