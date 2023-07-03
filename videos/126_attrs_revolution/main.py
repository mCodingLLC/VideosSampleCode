from __future__ import annotations

import inspect
from typing import Any

from attrs import validators, setters
from attrs import define, frozen, field, Factory


@define
class User:
    id: int = field(validator=validators.instance_of(int))
    name: str = field(converter=str)
    email: str = field(repr=False)

    @email.default
    def _email_default(self):
        return f"{self.name}@example.com"


def slots_is_the_default():
    user = User(0, "James", "james@example.com")
    user.nmae = "JAMES"


def show_sources():
    print(inspect.getsource(User.__init__))
    print(inspect.getsource(User.__eq__))
    print(inspect.getsource(User.__repr__))


def main():
    slots_is_the_default()
    show_sources()


if __name__ == '__main__':
    main()
