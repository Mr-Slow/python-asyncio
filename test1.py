import asyncio
import time


async def say_after(delay, what):
    print('test1')
    await asyncio.sleep(delay)
    #raise Exception('test')
    print(what)
    return 123


async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(5, 'world'))

    print(f"started at {time.strftime('%X')}")
    print(task1)
    a = await task1
    #time.sleep(4)
    print(345)
    b = await task2
    print(f"finished at {time.strftime('%X')}")
    print(a,b)
    return 123

a = asyncio.run(main())
print(a)
