from typing import Optional

from pydantic import BaseModel


class Warehouse(BaseModel):
    id: Optional[str] = None
    product: str
    amount: int


class WarehouseIn(BaseModel):
    product: str
    amount: int
