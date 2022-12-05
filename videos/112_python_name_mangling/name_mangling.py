def mangle_name(cls_name: str, identifier: str) -> str:
    if not identifier.startswith("__"):
        return identifier  # don't mangle a.normal_attr
    elif identifier.endswith("__"):
        return identifier  # don't mangle a.__len__
    elif "." in identifier:
        return identifier  # don't mangle import a.__x statement

    stripped_cls_name = cls_name.lstrip("_")
    if not stripped_cls_name:
        return identifier  # don't mangle inside class ______:

    return f"_{stripped_cls_name}{identifier}"


def main():
    assert mangle_name("NormalClass", "normal_attr") == "normal_attr"
    assert mangle_name("NormalClass", "__str__") == "__str__"
    assert mangle_name("NormalClass", "__") == "__"
    assert mangle_name("NormalClass", "dotted.name") == "dotted.name"
    assert mangle_name("NormalClass", "__dotted.name") == "__dotted.name"
    assert mangle_name("NormalClass", "_single") == "_single"
    assert mangle_name("NormalClass", "__double") == "_NormalClass__double"
    assert mangle_name("____UnderscoreClass", "__double") == "_UnderscoreClass__double"
    assert mangle_name("NormalClass", "______many") == "_NormalClass______many"
    assert mangle_name("NormalClass", "______many_") == "_NormalClass______many_"
    assert mangle_name("NormalClass", "______many__") == "______many__"
    assert mangle_name("____", "__double") == "__double"


if __name__ == '__main__':
    main()
