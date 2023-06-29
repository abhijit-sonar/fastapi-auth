from motor.motor_asyncio import AsyncIOMotorClient
import os


MONGODB_URL = os.environ.get("MONGODB_URL")
if MONGODB_URL is None:
    raise ValueError("The environment variable MONGODB_URL must be set")


client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URL)


def get_collection():
    return client.users.users
