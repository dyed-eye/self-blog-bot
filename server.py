import json
import aiofiles


async def get_data():
    async with aiofiles.open("server_data.json", "r") as f:
        data = await f.read()
    return json.loads(data)
        
async def set_value(key, value):
    try:
        data = await get_data()
        data[key] = value
        async with aiofiles.open("server_data.json", "w") as f:
            await f.write(json.dumps(data)) 
        return True
    except Exception as e:
        print(e)
        return False
        
