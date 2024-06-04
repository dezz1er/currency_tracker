from pydantic import BaseModel
from typing import Annotated


class Currency(BaseModel):
    amount: Annotated[int | float, 'Amount money to exchange']
    convert_from: str
    convert_to: str
