from enum import Enum
from typing import Dict, ForwardRef, List, Literal, Optional, Union
from pydantic import BaseModel, root_validator
from holon.writing import autocomplete


@autocomplete
class Principle(BaseModel):
    title: str
    information: str


robustness = Principle(
    title="Robustness Principle",
    information="https://en.wikipedia.org/wiki/Robustness_principle",
)

# TODO: Further reading on downside
# https://tools.ietf.org/id/draft-thomson-postel-was-wrong-03.html

yagni = Principle(
    title="YAGNI", information="https://martinfowler.com/bliki/Yagni.html"
)

# TODO: find good link for these
design_first = Principle(title="Design First", information="TODO")
code_first = Principle(title="Code First", information="TODO")
api_first = Principle(title="API First", information="TODO")
