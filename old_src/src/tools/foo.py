import asyncio
import uuid

def get_uuid_string():
    """Returns a unique UUID string"""
    myuuid = uuid.uuid4()
    return str(myuuid)


async def main():
    print(get_uuid_string())

if __name__ == "__main__":
    asyncio.run(main())