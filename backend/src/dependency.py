# we need to make get_db function so we can use it as a dependency injection for our endpoints

# import session
# create the generator

from src.database import session


async def get_db():
    # Return the session without disconnecting since the connection is managed by lifespan
    yield session
