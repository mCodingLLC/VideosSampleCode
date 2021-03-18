from dataclasses import dataclass

def command_split(command):
    commands = command.split()
    if commands == ["make"]:
        print("default make")
    elif len(commands) == 2 and commands[0] == "make":
        cmd = commands[1]
        print(f"make command found: {cmd}")
    elif commands == ["restart"]:
        print("restarting")
    elif len(commands) >= 1 and commands[0] == "rm":
        files = commands[1:]
        print(f"deleting files: {files}")
    else:
        print("didn't match")

def match_errno(errno):
    if errno == 0:
        pass
    elif errno == 1:
        pass
    elif errno == 42:
        print("42!")
    else:
        print("wildcard")

def match_alternatives(command):
    commands = command.split()
    if commands == ["north"] or commands == ["go", "north"]:
        print("going north")
    elif len(commands) == 2 and commands[0] == "get":
        obj = commands[1]
        print(f"picking up: {obj}")
    elif len(commands) == 3 and commands[0:2] == ["pick", "up"]:
        obj = commands[2]
        print(f"picking up: {obj}")
    elif len(commands) == 3 and commands[0] == "pick" and commands[2] == "up":
        obj = commands[1]
        print(f"picking up: {obj}")

def match_capture_subpattern(command):
    commands = command.split()
    if len(commands) == 2 and commands[0] == "go" and commands[1] in {"north", "south", "east", "west"}:
        direction = commands[1]
        print(f"going {direction}")

def match_guard(command, exits):
    commands = command.split()
    if len(commands) == 2 and commands[0] == "go" and commands[1] in exits:
        direction = commands[1]
        print(f"going {direction}")
    elif len(commands) == 2 and commands[0] == "go":
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
    if isinstance(event, Click) and event.button == "left":
        x,y = event.position
        print(f"handling left click at {x, y}")
    elif isinstance(event, Click):
        x,y = event.position
        print(f"handling other click at {x, y}")
    elif isinstance(event, KeyPress) and event.key_name in ["Q","q"] \
            or isinstance(event, Quit):
        print("quitting")
    elif isinstance(event, KeyPress) and event.key_name == "up arrow":
        print("going up")
    elif isinstance(event, KeyPress):
        pass
    else:
        raise ValueError(f'unrecognized event: {event}')

def match_json_event(event):
    if event.get("transport") == "http":
        print("insecure event ignored")
    elif event.get("verb") == "GET" and event.get("page") == "articles" and "pageno" in event:
        n = event["pageno"]
        print(f"let me get that article for you on page {n}...")
    elif event.get("verb") == "POST" and event.get("page") == "signup":
        print("handling signup")

def main():
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
    match_by_class(Click(position=(0, 0), button="left"))
    match_by_class(Quit())
    try:
        match_by_class("BADVALUE")
    except ValueError:
        pass
    match_json_event({"verb": "GET", "page": "articles", "pageno": 5, "info": "extra"})

if __name__ == '__main__':
    main()
