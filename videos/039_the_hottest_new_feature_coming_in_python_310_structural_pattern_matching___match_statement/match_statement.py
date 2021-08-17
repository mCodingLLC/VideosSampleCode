from dataclasses import dataclass

# NOTE: You need Python 3.10 to run this code.

def command_split(command):
    match command.split():
        case ["make"]:
            print("default make")
        case ["make", cmd]:
            print(f"make command found: {cmd}")
        case ["restart"]:
            print("restarting")
        case ["rm", *files]:
            print(f"deleting files: {files}")
        case _:
            print("didn't match")

def match_errno(errno):
    match errno:
        case 0:
            pass
        case 1:
            pass
        case 42:
            print("42!")
        case _:
            print("wildcard")

def match_alternatives(command):
    match command.split():
        case ["north"] | ["go", "north"]:
            print("going north")
        case ["get", obj] | ["pick", "up", obj] | ["pick", obj, "up"]:
            print(f"picking up: {obj}")

def match_capture_subpattern(command):
    match command.split():
        case ["go", ("north" | "south" | "east" | "west") as direction]:
            print(f"going {direction}")

def match_guard(command, exits):
    match command.split():
        case ["go", direction] if direction in exits:
            print(f"going {direction}")
        case ["go", _]:
            print(f"can't go that way")

@dataclass
class Click:
    position: tuple[int, int]
    button: str

@dataclass
class KeyPress:
    key_name: str

@dataclass
class Quit:
    pass

def match_by_class(event):
    match event:
        case Click(position=(x,y), button="left"):
            print(f"handling left click at {x,y}")
        case Click(position=(x,y)):
            print(f"handling other click at {x,y}")
        case KeyPress("Q"|"q") | Quit():
            print("quitting")
        case KeyPress(key_name="up arrow"):
            print("going up")
        case KeyPress():
            pass #ignore other keystrokes
        case other_event:
            raise ValueError(f'unrecognized event: {other_event}')

def match_json_event(event):
    match event:
        case {"transport": "http"}:
            print("insecure event ignored")
        case {"verb": "GET", "page": "articles", "pageno": n}:
            print(f"let me get that article for you on page {n}...")
        case {"verb": "POST", "page": "signup"}:
            print("handling signup")

def main():
    # x, y = 1, 2
    command_split("make")
    command_split("make clean")
    command_split("restart")
    command_split("rm a b c")
    command_split("doesnt match")
    match_errno(42)
    match_alternatives("go north")
    match_alternatives("pick up sword")
    match_capture_subpattern("go north")
    match_capture_subpattern("go east")
    match_guard("go north", exits=["east", "south"])
    match_guard("go north", exits=["north"])
    match_by_class(Click(position=(0,0), button="left"))
    match_by_class(Quit())
    try:
        match_by_class("BADVALUE")
    except ValueError:
        pass
    match_json_event({"verb": "GET", "page": "articles", "pageno": 5, "info": "extra"})
    pass

if __name__ == '__main__':
    main()
