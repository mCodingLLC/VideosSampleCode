import ast


class Visitor(ast.NodeVisitor):

    def visit_For(self, node: ast.AST):
        print(node)
        self.generic_visit(node)


def main():
    with open('cool_module.py') as f:
        code = f.read()

    node = ast.parse(code)
    Visitor().visit(node)


if __name__ == '__main__':
    main()
