import aiosqlite


async def get(req):
    try:
        async with aiosqlite.connect("database.db") as db:
            cursor = await db.execute(req)
            row = await cursor.fetchone()
            await cursor.close()
        return row
    except Exception as e:
        print(f'Database get error: {e}')
        print(f'Original request was "{req}"')
        return e

async def get_all(req):
    try:
        async with aiosqlite.connect("database.db") as db:
            cursor = await db.execute(req)
            rows = await cursor.fetchall()
            await cursor.close()
        return rows
    except Exception as e:
        print(f'Database get error: {e}')
        print(f'Original request was "{req}"')
        return e
        
async def commit(req):
    try:
        async with aiosqlite.connect("database.db") as db:
            await db.execute(req)
            await db.commit()
        return True
    except Exception as e:
        print(f'Database commit error: {e}')
        print(f'Original request was "{req}"')
        return False
    