import asyncio

async def client_connected(reader, writer):
    await reader.readline()

async def main(host, port):
    srv = await asyncio.start_server(
        client_connected, host, port)
    # await srv.serve_forever()
    await srv.start_serving()

asyncio.run(main('127.0.0.1', 0))
