import asyncio
import time

async def say_after2(delay, what, task=0):
    await say_after(delay, what, task)


async def say_after(delay, what, task=0):
    if task:
        print(task.get_stack(), 'aaa2')
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(
        say_after2(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world', task1))
    print(task1.get_stack(), 'aaa')
    print(f"started at {time.strftime('%X')}")
    print(task1)
    await task1
    print(task2.get_stack(), 'aaabbb')
    await task2
    print(f"finished at {time.strftime('%X')}")
    print(task2.get_stack(), 'aaa')
    return 123

a = asyncio.run(main())
print(a)

print(123)
