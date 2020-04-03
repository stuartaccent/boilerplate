from app.db import database


async def on_startup():
    await database.connect()


async def on_shutdown():
    await database.disconnect()
