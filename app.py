import api
from flask import Flask
import asyncio
from reset import remove_all_old_data

async def main():
    await remove_all_old_data()
    # API.run(port=5001)

if __name__ == "__main__":
    app = Flask(__name__)
    API = api.API(app)
    API.run(port=5001)
    asyncio.run(main())
