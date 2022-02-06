import ast
import textwrap

import libcst as cst
from libcst.metadata import PositionProvider
from libcst.tool import dump


def f():
    pass


def g():
    pass


def default():
    pass


_switch_dict = {
    0: f,
    1: g,
    2: g,
    3: f,
    4: g,
}


def switch_dict_example(x):
    do_next = _switch_dict.get(x, default)
    do_next()


def match_int_example(x):
    match x:
        case 0:
            pass
        case 1 | 2:
            pass
        case 3:
            pass
        case _:
            pass


def match_int_elif_example(x):
    if x == 0:
        pass
    elif x in (1, 2):
        pass
    elif x == 3:
        pass
    else:
        pass


class Visitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def visit_Tuple(self, node: cst.Tuple):
        pos = self.get_metadata(PositionProvider, node)

        if pos.start.line != pos.end.line:
            return

        match node:
            case cst.Tuple(
                elements=[
                    *_,
                    _,
                    cst.Element(
                        value=cst.Comparison(
                            comparisons=[
                                cst.ComparisonTarget(
                                    operator=cst.Equal(),
                                    comparator=cst.Tuple() as tup
                                ),
                            ],
                            lpar=[],
                            rpar=[],
                        ),
                    ),
                ],
            ):
                pos = self.get_metadata(PositionProvider, tup)
                print(f"matched {pos.start.line, pos.start.column}")

        # if isinstance(node, cst.Tuple):
        #     elements = node.elements
        #     if len(elements) >= 2:
        #         last_element = elements[-1]
        #         cmp = last_element.value
        #         if isinstance(cmp, cst.Comparison) and (not cmp.lpar) and (not cmp.rpar):
        #             comparisons = cmp.comparisons
        #             if len(comparisons) == 1:
        #                 target = comparisons[0]
        #                 if isinstance(target.operator, cst.Equal) and isinstance(tup := target.comparator, cst.Tuple):
        #                     pos = self.get_metadata(PositionProvider, tup)
        #                     print(f"matched {pos.start.line, pos.start.column}")


example_code = textwrap.dedent("""
    a = 'hello'  # some comment
    b="subscribe"

    def cool(n):
        for i in range(1, n): # hello
            print(i * "*")
        for i in range(n, 0, -1):
            print(i * "*")

        print((True, True, True == (True, True, True)))


    True, True, (True == (True, True, True))
    """)


def dump_ast_example():
    code = example_code

    print("ORIGINAL CODE")
    print(code)

    node = ast.parse(code)
    # print("ABSTRACT SYNTAX TREE")
    # print(ast.dump(node, indent=4))

    print("RECONSTRUCTED CODE")
    print(ast.unparse(node))


def dump_cst_example():
    code = example_code

    print("ORIGINAL CODE")
    print(code)

    node = cst.parse_module(code)
    # print("CONCRETE SYNTAX TREE")
    # print(dump(node, show_syntax=True, indent=" " * 4, show_whitespace=True, show_defaults=True))

    print("RECONSTRUCTED CODE")
    print(node.code)
    assert code == node.code  # perfect reconstruction


def ambiguous_tuple_equality_example():
    codes = ["True, True, True == (True, True, True)",
             "True, True, (True == (True, True, True))",
             "(True, True, True) == (True, True, True)", ]

    for code in codes:
        print(code)
        node = cst.parse_module(code)
        node_with_metadata = cst.MetadataWrapper(node)
        # print(dump(node.body[0].body[0].value, show_syntax=True, indent=" " * 4, show_whitespace=True, show_defaults=True))
        node_with_metadata.visit(Visitor())


def main():
    # dump_ast_example()
    # dump_cst_example()
    ambiguous_tuple_equality_example()


if __name__ == '__main__':
    main()
