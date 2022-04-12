import logging
from typing import List

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from endpoints.depends import get_warehouse_repository, get_current_user
from models.user import User
from models.warehouse import WarehouseIn
from repositories.warehouses import WarehouseRepository

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', response_model=List[WarehouseIn])
async def read_warehouses(
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        limit: int = 100,
        skip: int = 0,
        current_user: User = Depends(get_current_user)):
    logger.info(f"read warehouse")
    return await warehouses.get_all(limit=limit, skip=skip)


@router.post('/add', response_model=WarehouseIn)
async def entry_of_opening_balances(
        warehouse: WarehouseIn,
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        current_user: User = Depends(get_current_user)):
    if current_user.type == 'buyers':
        logger.info(f"{current_user.login} - forbidden to buyers")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='forbidden to buyers')
    if warehouse.amount < 0:
        logger.info(f"{current_user.login} - negative balances is not allowed")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='negative balances is not allowed')
    try:
        product = await warehouses.entry_of_opening_balances(w=warehouse)
        logger.info(f"{current_user.login} - entry of opening balances")
        return product
    except UniqueViolationError:
        logger.info(f"{current_user.login} - this product exists")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='this product exists')


@router.put('/put', response_model=WarehouseIn)
async def update(
        w: WarehouseIn,
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        current_user: User = Depends(get_current_user)):
    if current_user.type == 'buyers':
        logger.info(f"{current_user.login} - forbidden to buyers")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='forbidden to buyers')
    product = await warehouses.get_by_product(product=w.product)
    if product is None:
        logger.info(f"{current_user.login} - this product is out of warehouse")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product is out of warehouse')
    warehouse = await warehouses.update(id=product.id, w=w, amount=product.amount)
    logger.info(f"{current_user.login} - this product is of warehouse")
    return warehouse


@router.put('/buy', response_model=WarehouseIn)
async def buy_product(
        w: WarehouseIn,
        warehouses: WarehouseRepository = Depends(get_warehouse_repository),
        current_user: User = Depends(get_current_user)):
    if current_user.type == 'sellers':
        logger.info(f"{current_user.login} - forbidden to sellers")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='forbidden to sellers')
    try:
        product = await warehouses.get_by_product(product=w.product)
    except ValidationError:
        logger.info(f"{current_user.login} - this product not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product not found')
    if product.amount == 0:
        logger.info(f"{current_user.login} - this product not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product not found')
    if w.amount >= product.amount:
        logger.info(f"{current_user.login} - not enough product in warehouse")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not enough product in warehouse')
    if product is None:
        logger.info(f"{current_user.login} - this product is out of warehouse")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this product is out of warehouse')
    warehouse = await warehouses.buy_product(id=product.id, w=w, amount=product.amount)
    logger.info(f"{current_user.login} - buys this product")
    return warehouse
