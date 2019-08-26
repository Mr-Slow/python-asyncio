import asyncio
import time
import threading
ss = 100


def thread_test(lp, name):
    v = asyncio.run_coroutine_threadsafe(thread_1(name), lp)


async def thread_1(name):
    task1 = asyncio.create_task(
        say_after(1, name))
    await task1
    return 123


async def say_after(delay, what):
    global ss
    await asyncio.sleep(delay)
    ss += 1
    print(ss, what, '---')


async def main():
    loop = asyncio.get_running_loop()
    task1 = asyncio.create_task(
        say_after(1, 'main'))
    for i in range(5):
        b = threading.Thread(target=thread_test, args=(loop, 'thread_%s' % i))
        b.start()
    await task1
    return 123


a = asyncio.run(main())
print(ss, 'final')
