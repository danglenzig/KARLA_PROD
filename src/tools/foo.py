import asyncio

async def main():
    with open('junk/junk.txt', 'w') as f:
        f.write("BAR")

if __name__ == "__main__":
    asyncio.run(main())