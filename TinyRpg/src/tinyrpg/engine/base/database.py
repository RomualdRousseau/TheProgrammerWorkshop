import json
import os
from functools import cache


class Database:
    def __init__(self, source_path: str):
        self.tables: dict[str, dict | list] = {}
        self.load_tables(source_path)

    def load_tables(self, source_path: str):
        for file_name in (f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))):
            file_path = os.path.join(source_path, file_name)
            with open(file_path, "r") as fp:
                table_name = os.path.splitext(file_name)[0]
                table_data = json.load(fp)
                self.tables[table_name] = table_data

    def select_list(self, table_name: str) -> list:
        return self.tables[table_name]  # type: ignore

    def select_dict(self, table_name: str) -> dict:
        return self.tables[table_name]  # type: ignore


@cache
def get_database() -> Database:
    return Database("data/database")
