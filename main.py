import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.settings import settings
from db.base import database
from endpoints import users, auth, warehouses

app = FastAPI(title='WareHouse API')
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(warehouses.router, prefix='/warehouses', tags=['warehouses'])


@app.get("/", response_class=RedirectResponse)
async def redirect_fastapi():
    return "/docs#/"


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.server_host, port=settings.server_port, reload=True)
