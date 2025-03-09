import cowsay
import shlex
import cmd

class CowCommandLine(cmd.Cmd):
    prompt = "twocows> "
    def do_cowsay(self, arg):
        """
                cowsay сообщение [название коровы [параметры]]
                Сказать сообщение коровой. Можно указать название коровы и параметры для её глаз и языка.
        """
        try:
            tokens = shlex.split(arg)
            if not tokens:
                print("Ошибка: сообщение не указано")
                return
            msg = tokens.pop(0)
            cow = tokens.pop(0) if tokens and tokens[0] in cowsay.list_cows() else "www"
            params = {k: v for param in tokens for k, v in [param.split("=")] if "=" in param}
            if cow not in cowsay.list_cows():
                print(f"Ошибка: корова '{cow}' не найдена")
                return

            result = cowsay.cowsay(message=msg, cow=cow, eyes=params.get("eyes", "oo"), tongue=params.get("tongue", "  "))
            print(result)
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")

    def do_cowthink(self, arg):
        """
                cowthink сообщение [название [параметр=значение ...]]
                корова думает над сообщением
        """
        try:
            tokens = shlex.split(arg)
            if not tokens:
                print("Ошибка: сообщение не указано")
                return

            msg = tokens.pop(0)
            cow = tokens.pop(0) if tokens and tokens[0] in cowsay.list_cows() else "www"
            params = {k: v for param in tokens for k, v in [param.split("=")] if "=" in param}

            if cow not in cowsay.list_cows():
                print(f"Ошибка: корова '{cow}' не найдена")
                return

            result = cowsay.cowthink(message=msg, cow=cow, eyes=params.get("eyes", "oo"),
                                     tongue=params.get("tongue", "  "))
            print(result)
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")

    def do_list_cows(self, arg):
        """
                list_cows
                Вывести список доступных коров.
        """
        print("Доступные коровы:", ", ".join(cowsay.list_cows()))

    def do_make_bubble(self, arg):
        """
               make_bubble сообщение [wrap_text=True]
               Создать текстовый пузырь для сообщения. Можно указать параметр wrap_text для оборачивания текста.
        """
        tokens = shlex.split(arg)
        if not tokens:
            print("Ошибка: сообщение не указано")
            return
        msg = tokens[0]
        wrap = tokens[1].lower() == 'true' if len(tokens) > 1 else True
        print(cowsay.make_bubble(msg, wrap_text=wrap))

    def do_help(self, arg):
        if arg:
            cmd.Cmd.do_help(self, arg)
        else:
            print("Доступные команды:")
            print("  cowsay — сказать сообщение коровой")
            print("  list_cows — вывести список доступных коров")
            print("  make_bubble — создать текстовый пузырь")
            print("  help — показать справку по командам")
            print("  exit — выйти из программы")
            print("  cowthink - корова думает над сообщением")

    def do_exit(self, arg):
        print("До свидания!")
        return True


print("Добро пожаловать в CowCommandLine! Введите 'help' для списка команд.")
CowCommandLine().cmdloop()