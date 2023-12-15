import ast
import importlib.abc
import importlib.machinery
import logging
import sys
import types

import requests


def is_valid_python_source(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


class CloudFinder(importlib.abc.MetaPathFinder):
    def __init__(self, base_url):
        self.base_url = base_url

    def find_spec(self, fullname, path, target=None):
        spec = self._find_py_file_spec(fullname)
        if spec is not None:
            return spec

        spec = self._find_package_init_spec(fullname)
        if spec is not None:
            return spec

        return None

    def _find_py_file_spec(self, fullname):
        url = f"{self.base_url}/{fullname.replace('.', '/')}.py"
        source = self._get_remote_python_source(url)
        if source is None:
            return None
        loader = CloudLoader(fullname, source, url)
        return importlib.machinery.ModuleSpec(fullname, loader, origin=url)

    def _find_package_init_spec(self, fullname):
        url = f"{self.base_url}/{fullname.replace('.', '/')}/__init__.py"
        source = self._get_remote_python_source(url)
        if source is None:
            return None
        loader = CloudLoader(fullname, source, url)
        spec = importlib.machinery.ModuleSpec(
            fullname, loader, origin=url, is_package=True,
        )
        return spec

    def _get_remote_python_source(self, url):
        try:
            logging.info(f"Getting url: {url}")
            response = requests.get(url)
            response.raise_for_status()
        except requests.HTTPError:
            return None

        source = response.text

        if not is_valid_python_source(source):
            return None
        return source


class CloudLoader(importlib.abc.Loader):
    def __init__(self, fullname, source_code, url):
        self.fullname = fullname
        self.source_code = source_code
        self.url = url

    def create_module(self, spec):
        module = sys.modules.get(spec.name)
        if module is None:
            module = types.ModuleType(spec.name)
            sys.modules[spec.name] = module
        return module

    def exec_module(self, module):
        module.__file__ = self.url
        exec(self.source_code, module.__dict__)
        return module

    def get_source(self, name):
        return self.source_code


def add_repo(url: str):
    sys.meta_path.append(CloudFinder(url))


def add_gh_repo(username: str, repo: str, ref: str):
    add_repo(f"https://raw.githubusercontent.com/{username}/{repo}/{ref}")
