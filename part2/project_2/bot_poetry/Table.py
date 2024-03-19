from rich.table import Table
from abc import ABC, abstractmethod


class CreatingTable(ABC):
    @abstractmethod
    def get_table(self):
        pass


class BookTable(CreatingTable):
    def __init__(self, data):
        self.data = data

    def get_table(self):
        table = Table(show_header=True, header_style="bold cyan", style="blue")
        table.add_column("Name", style="bright_magenta")
        table.add_column("Phone", style="magenta")
        table.add_column("Birthday", style="cyan")

        for sh in self.data.values():
            table.add_row(
                f"{sh.name}",
                f"{', '.join(p.get_value for p in sh.phones)}",
                f"{sh.birthdays}",
            )
        return table


class HelpTable(CreatingTable):
    def __init__(self, data):
        self.data = data

    def get_table(self):
        table = Table(show_header=True, header_style="bold cyan", style="blue")
        table.add_column("Command", style="magenta")
        table.add_column("Description", style="cyan")

        for command, description in self.data.items():
            table.add_row(
                f"{command}",
                f"{description}",
            )
        return table
