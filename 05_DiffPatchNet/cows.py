import asyncio
import cowsay
import shlex

clients = {}


async def handle_client(reader, writer):
    cow_name = None
    writer.write(b"Welcome to the cow chat! Register with 'login <cow_name>'\n")
    await writer.drain()

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            message = data.decode().strip()
            if not message:
                continue

            command, *args = shlex.split(message)

            if command == "login":
                if not args:
                    writer.write(b"Usage: login <cow_name>\n")
                elif args[0] in clients:
                    writer.write(b"This cow name is already taken.\n")
                elif args[0] not in cowsay.list_cows():
                    writer.write(b"Invalid cow name. Use 'cows' to see available names.\n")
                else:
                    cow_name = args[0]
                    clients[cow_name] = writer
                    writer.write(f"Welcome, {cow_name}!\n".encode())

            elif command == "who":
                writer.write(f"Registered cows: {', '.join(clients.keys())}\n".encode())

            elif command == "cows":
                available_cows = set(cowsay.list_cows()) - set(clients.keys())
                writer.write(f"Available cows: {', '.join(available_cows)}\n".encode())

            elif command == "say":
                if cow_name is None:
                    writer.write(b"You must login first.\n")
                elif len(args) < 2:
                    writer.write(b"Usage: say <cow_name> <message>\n")
                elif args[0] not in clients:
                    writer.write(b"Recipient not found.\n")
                else:
                    recipient = args[0]
                    msg = " ".join(args[1:])
                    formatted_msg = cowsay.cowsay(msg, cow=cow_name)
                    clients[recipient].write(f"{formatted_msg}\n".encode())
                    await clients[recipient].drain()

            elif command == "yield":
                if cow_name is None:
                    writer.write(b"You must login first.\n")
                elif not args:
                    writer.write(b"Usage: yield <message>\n")
                else:
                    msg = " ".join(args)
                    formatted_msg = cowsay.cowsay(msg, cow=cow_name)
                    for client_name, client_writer in clients.items():
                        if client_writer != writer:
                            client_writer.write(f"{formatted_msg}\n".encode())
                            await client_writer.drain()

            elif command == "quit":
                writer.write(b"Goodbye!\n")
                break

            else:
                writer.write(b"Unknown command.\n")

            await writer.drain()

    except asyncio.CancelledError:
        pass

    finally:
        if cow_name and cow_name in clients:
            del clients[cow_name]
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 12345)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
