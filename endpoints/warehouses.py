from typing import List

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from endpoints.depends import get_warehouse_repository, get_current_user
from models.user import User
from models.warehouse import WarehouseIn
from repositories.warehouses import WarehouseRepository

router = APIRouter()


@router.get('/', response_model=List[WarehouseIn])
async def read_warehouses(
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        limit: int = 100,
        skip: int = 0,
        current_user: User = Depends(get_current_user)):
    return await warehouses.get_all(limit=limit, skip=skip)


@router.post('/add', response_model=WarehouseIn)
async def entry_of_opening_balances(
        warehouse: WarehouseIn,
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        current_user: User = Depends(get_current_user)):
    if current_user.type == 'buyers':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='forbidden to buyers')
    if warehouse.amount < 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='negative balances is not allowed')
    try:
        product = await warehouses.entry_of_opening_balances(w=warehouse)
        return product
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='this product exists')


@router.put('/put', response_model=WarehouseIn)
async def update(
        w: WarehouseIn,
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        current_user: User = Depends(get_current_user)):
    if current_user.type == 'buyers':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='forbidden to buyers')
    product = await warehouses.get_by_product(product=w.product)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product is out of warehouse')
    warehouse = await warehouses.update(id=product.id, w=w, amount=product.amount)
    return warehouse


@router.put('/buy', response_model=WarehouseIn)
async def buy_product(
        w: WarehouseIn,
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        current_user: User = Depends(get_current_user)):
    if current_user.type == 'sellers':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='forbidden to sellers')
    try:
        product = await warehouses.get_by_product(product=w.product)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product not found')
    if product.amount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product not found')
    if w.amount >= product.amount:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not enough product in warehouse')
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product is out of warehouse')
    warehouse = await warehouses.buy_product(id=product.id, w=w, amount=product.amount)
    return warehouse
