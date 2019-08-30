import asyncio

async def client_connected(reader, writer):
    msg = await reader.readline()
    print(msg)

async def main(host, port):
    srv = await asyncio.start_server(
        client_connected, host, port)
    # await srv.serve_forever()
    await srv.start_serving()
    srv.close()
    await srv.wait_closed()

asyncio.run(main('127.0.0.1', 8888))
