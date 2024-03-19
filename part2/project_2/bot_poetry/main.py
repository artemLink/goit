from CommandHandler import handlers_dict
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from art import *


class HandlerFactory:
    @staticmethod
    def create_handler(command):
        handler_class = handlers_dict.get(command)
        if handler_class:
            return handler_class
        else:
            return None


if __name__ == "__main__":
    tprint("Personal    assistant")

    word_completer = WordCompleter(handlers_dict.keys())
    show_help_table = HandlerFactory.create_handler("help")
    show_help_table.handler()

    while True:
        command = prompt("Input command>>> ", completer=word_completer)
        command.lower()

        handler = HandlerFactory.create_handler(command)
        handler.handler() if handler else print("Invalid command")

        if command == "exit":
            break
