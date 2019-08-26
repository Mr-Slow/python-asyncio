import asyncio
import time


@asyncio.coroutine
def say_after(delay, what, task=0):
    yield from asyncio.sleep(delay)
    print(what)

@asyncio.coroutine
def main():
    task1 = asyncio.ensure_future(
        say_after(1, 'hello'))

    task2 = asyncio.ensure_future(
        say_after(2, 'world', task1))
    print(f"started at {time.strftime('%X')}")
    print(task1)
    yield from task1
    print(task2.get_stack(), 'aaabbb')
    yield from task2
    print(task1)
    print(f"finished at {time.strftime('%X')}")
    return 123

#a = asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
#print(a)
