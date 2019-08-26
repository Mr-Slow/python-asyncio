import asyncio


async def set_after(fut, delay, value):
    # Sleep for *delay* seconds.
    await asyncio.sleep(delay)
    print('hhh')

    # Set *value* as a result of *fut* Future.
    #fut.set_result(value)

async def main():
    loop = asyncio.get_running_loop()

    fut = loop.create_future()

    loop.create_task(
        set_after(fut, 1, '... world'))
    loop.create_task(
        set_after(fut, 1, '... world2'))

    print('hello ...')

    # Wait until *fut* has a result (1 second) and print it.
    print(await fut)

asyncio.run(main())
