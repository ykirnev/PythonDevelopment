import asyncio
import cmd
import readline
import shlex


class CowChatClient(cmd.Cmd):
    prompt = "cowchat> "

    def __init__(self, host='127.0.0.1', port=12345):
        super().__init__()
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.cow_names = []
        self.connected = False

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.connected = True
        asyncio.create_task(self.listen_server())

    async def listen_server(self):
        while self.connected:
            line = await self.reader.readline()
            if not line:
                break
            print(f"\n{line.decode().strip()}\n{self.prompt}{readline.get_line_buffer()}", end="", flush=True)

    def send(self, command):
        if self.writer is None:
            print("Not connected to the server.")
            return
        self.writer.write(f"{command}\n".encode())
        asyncio.create_task(self.writer.drain())

    def do_login(self, arg):
        "Login with a cow name: login <cow_name>"
        self.send(f"login {arg}")

    def complete_login(self, text, line, begidx, endidx):
        self.send("cows")
        return [name for name in self.cow_names if name.startswith(text)]

    def do_who(self, arg):
        "List registered cows: who"
        self.send("who")

    def do_cows(self, arg):
        "List available cow names: cows"
        self.send("cows")

    def do_say(self, arg):
        "Send a message to another cow: say <cow_name> <message>"
        self.send(f"say {arg}")

    def complete_say(self, text, line, begidx, endidx):
        self.send("who")
        return [name for name in self.cow_names if name.startswith(text)]

    def do_yield(self, arg):
        "Send a message to all cows: yield <message>"
        self.send(f"yield {arg}")

    def do_quit(self, arg):
        "Exit the chat: quit"
        self.send("quit")
        self.connected = False
        return True


async def main():
    client = CowChatClient()
    await client.connect()
    client.cmdloop()


asyncio.run(main())
