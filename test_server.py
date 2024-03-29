import asyncio

async def client_connected(reader, writer):
    # Communicate with the client with
    # reader/writer streams.  For example:
    #await reader.readline()
    await asyncio.sleep(1)
    print(reader, writer)

async def main(host, port):
    srv = await asyncio.start_server(
        client_connected, host, port)
    await srv.serve_forever()

asyncio.run(main('127.0.0.1', 8888))
