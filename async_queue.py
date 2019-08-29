import asyncio

async def worker1(queue):
    print('aaaa')
    a = await queue.get()
    print(a)

async def worker2(queue):
    await asyncio.sleep(2)
    print('put to queue:')
    await queue.put(3)

async def main():
    queue = asyncio.Queue()
    task1 = asyncio.create_task(worker1(queue))
    task2 = asyncio.create_task(worker2(queue))
    await task1
    await task2

asyncio.run(main())
