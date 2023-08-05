from holon.writing import autocomplete
from pydantic import BaseModel


@autocomplete
class MediaType(BaseModel):
    name: str
    reference: str
