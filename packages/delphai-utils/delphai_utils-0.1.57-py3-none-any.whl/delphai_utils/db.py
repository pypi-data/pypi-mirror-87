from delphai_utils.config import get_config
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

db_connection_string = get_config('database.connection_string')
db_client = AsyncIOMotorClient(db_connection_string)
db = db_client.main
db_sync_client = MongoClient(db_connection_string)
db_sync = db_sync_client.main