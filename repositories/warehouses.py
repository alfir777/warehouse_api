from typing import List

from db.warehouses import warehouses
from models.warehouse import Warehouse, WarehouseIn
from .base import BaseRepository


class WarehouseRepository(BaseRepository):
    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Warehouse]:
        query = warehouses.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def entry_of_opening_balances(self, w: WarehouseIn) -> Warehouse:
        warehouse = Warehouse(
            product=w.product,
            amount=w.amount,
        )
        values = {**warehouse.dict()}
        values.pop('id', None)
        query = warehouses.insert().values(**values)
        warehouse.id = await self.database.execute(query)
        return warehouse

    async def update(self, id: str, w: WarehouseIn, amount: int) -> Warehouse:
        product = Warehouse(
            product=w.product,
            amount=w.amount + amount
        )
        values = {**product.dict()}
        values.pop('id', None)
        query = warehouses.update().where(warehouses.c.id == int(id)).values(**values)
        product.id = await self.database.execute(query)
        return product

    async def buy_product(self, id: str, w: WarehouseIn, amount: int) -> Warehouse:
        product = Warehouse(
            product=w.product,
            amount=amount - w.amount
        )
        values = {**product.dict()}
        values.pop('id', None)
        query = warehouses.update().where(warehouses.c.id == int(id)).values(**values)
        product.id = await self.database.execute(query)
        return product

    async def delete(self, id: int):
        query = warehouses.delete().where(warehouses.c.id == id)
        return await self.database.execute(query=query)

    async def get_by_product(self, product: str) -> Warehouse:
        query = warehouses.select().where(warehouses.c.product == product)
        product = await self.database.fetch_one(query)
        return Warehouse.parse_obj(product)
