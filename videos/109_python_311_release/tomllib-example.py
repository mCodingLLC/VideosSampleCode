import tomllib


def tomllib_example():
    with open("pyproject.toml") as fp:
        proj_data = tomllib.load(fp)

    print(proj_data["build-system"]["requires"])
    

def main():
    tomllib_example()


if __name__ == "__main__":
    main()
