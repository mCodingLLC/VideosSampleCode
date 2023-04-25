import os
import pathlib


def analyze_data(file: str):
    if not os.path.exists(file):
        # if not os.path.isfile(file):
        # if not os.path.isdir(file):

        print(f"Does not exist: {file}")
        return

    with open(file) as fp:
        ...


def analyze_data(file: str):
    try:
        with open(file) as fp:
            data = fp.read()
    except FileNotFoundError:
        print(f"Does not exist: {file}")


def analyze_data(file: str):
    try:
        data = pathlib.Path(file).read_text()
    except FileNotFoundError:
        print(f"Does not exist: {file}")
    except OSError:
        print(f"Failed to open: {file}")
    else:
        ...


def analyze_data(path: pathlib.Path):
    try:
        data = path.read_text()
    except FileNotFoundError:
        print(f"Does not exist: {path}")
    except OSError:
        print(f"Failed to open: {path}")
    else:
        ...


def initialize_app():
    config_dir = "."
    if is_user_config_dir_present(config_dir):
        ...  # load config files
    else:
        ...  # load defaults


def your_options():
    # file = "/path/to/some/file.txt"
    # path = pathlib.Path(file)
    path = pathlib.Path("path", "to", "some", "file.txt")
    if path.is_dir():
        print("Found")
    else:
        print("Not found")
