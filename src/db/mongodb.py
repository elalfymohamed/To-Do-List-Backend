from motor.motor_asyncio import AsyncIOMotorClient

from core.config import db_config


client = AsyncIOMotorClient(db_config.DB_URL)


async def get_db() -> AsyncIOMotorClient:
    """Get database client"""
    try:
        db = client[db_config.DB_NAME]
        # Ping MongoDB to confirm connection
        await db.command("ping")
        print("Connected to MongoDB")
        return db
    except Exception as e:
        print(e, "Failed to connect to MongoDB")
    