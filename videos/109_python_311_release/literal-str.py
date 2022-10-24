from re import X
from typing import LiteralString


def execute_query(conn, query: LiteralString, *params):
    ...


def literal_examples(lit: LiteralString):
    x = "this is literal"
    y = "this is also" + x + lit
    z = "\n".join([x, y])  # still literal
    t = f"{x} {y} {z} still literal!"


def bad_code(conn, user_proved_string: str):
    execute_query(conn, f"SELECT * FROM users where id = ?", user_proved_string)
