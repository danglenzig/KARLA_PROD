import asyncio

async def main():
    with open('junk/junk.txt', 'r') as f:
        bar_str:str = f.read().strip()
    print(bar_str)

if __name__ == "__main__":
    asyncio.run(main())