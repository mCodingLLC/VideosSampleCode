import argparse
import ast
from collections.abc import Iterator
from typing import NamedTuple

from flake8.options.manager import OptionManager


class Flake8ASTErrorInfo(NamedTuple):
    line_number: int
    offset: int
    msg: str
    cls: type  # unused currently, but required


class LocalImportsNotAllowed:
    msg = "MCOD101 local imports are not allowed"

    @classmethod
    def check(cls, node: ast.FunctionDef, errors: list[Flake8ASTErrorInfo]) -> None:
        for child in ast.walk(node):
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                err = Flake8ASTErrorInfo(child.lineno, child.col_offset, cls.msg, cls)
                errors.append(err)


class MCodingASTVisitor(ast.NodeVisitor):

    def __init__(self):
        self.errors: list[Flake8ASTErrorInfo] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        LocalImportsNotAllowed.check(node, self.errors)
        self.generic_visit(node)  # continue visiting child nodes


class MCodingASTPlugin:
    name = 'flake8_mcoding_ast'
    version = '0.0.0'

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Iterator[Flake8ASTErrorInfo]:
        visitor = MCodingASTVisitor()
        visitor.visit(self._tree)
        yield from visitor.errors

    @staticmethod
    def add_options(option_manager: OptionManager):
        option_manager.add_option(
            '--some-fancy-var',  # converted to some_fancy_var in options
            type=int,
            metavar='n',  # shows up in help text
            default=0,
            parse_from_config=True,
            help='Fancy var description. (Default: %(default)s)'
        )

    @staticmethod
    def parse_options(options: argparse.Namespace):
        if options.some_fancy_var > 0:
            ...
