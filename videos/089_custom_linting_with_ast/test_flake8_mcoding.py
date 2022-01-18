import ast
import textwrap

from flake8_mcoding import MCodingASTPlugin


def get_errors(s: str) -> set[str]:
    tree = ast.parse(s)
    plugin = MCodingASTPlugin(tree)
    return {f'{line}:{col} {msg.partition(" ")[0]}' for line, col, msg, _ in plugin.run()}


def test_local_import_not_allowed():
    code = textwrap.dedent("""
    def f():
        print(123)
        import json
    """)
    actual = get_errors(code)
    expected = {'4:4 MCOD101'}
    assert actual == expected


def test_nested_local_import_not_allowed():
    code = textwrap.dedent("""
    def f():
        print(123)
        if True:
            import json
    """)
    actual = get_errors(code)
    expected = {'5:8 MCOD101'}
    assert actual == expected


def test_local_import_inside_local_function_not_allowed():
    code = textwrap.dedent("""
    def f():
        print(123)
        def local():
            import json
    """)
    actual = get_errors(code)
    expected = {'5:8 MCOD101'}
    assert actual == expected


def test_local_from_import_not_allowed():
    code = textwrap.dedent("""
    def f():
        print(123)
        from json import load
    """)
    actual = get_errors(code)
    expected = {'4:4 MCOD101'}
    assert actual == expected


def test_no_local_imports_multiple_errors_can_be_reported():
    code = textwrap.dedent("""
    def f():
        import json
        print(123)
        from json import load
        
    def g():
        import json
    """)
    actual = get_errors(code)
    expected = {'3:4 MCOD101', '5:4 MCOD101', '8:4 MCOD101'}
    assert actual == expected


def test_global_import_allowed():
    code = textwrap.dedent("""
    import json
    from json import load
    def f():
        print(123)
    """)
    actual = get_errors(code)
    expected = set()
    assert actual == expected
