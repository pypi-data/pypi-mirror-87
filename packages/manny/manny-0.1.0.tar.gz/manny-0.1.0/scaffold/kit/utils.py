import ast

import astor
import black


class Walker(ast.NodeTransformer):
    __imports = {}
    __sv = set()  # serializers and views

    def __init__(self, file, options=None):
        self.file = file
        with open(self.file, "r") as f:
            self.tree = ast.parse(f.read())
        self.options = options
        super().__init__()

    def visit_Attribute(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        if isinstance(node.value, ast.Name) and node.value.id == "models":
            self.__sv.add(node.attr)
        return node

    def visit_Assign(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        if self.options:
            # TODO: refactor
            if node.targets[0].id == self.options["variable"]:
                node.value.elts.extend(
                    [
                        ast.Constant(value=x, kind=None)
                        for x in self.options["variable_values"]
                        if x not in [app.value for app in node.value.elts]
                    ]
                )
        return node

    def visit_Import(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.__imports["free"] = [x.name for x in node.names]
        return node

    def visit_ImportFrom(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.__imports[node.module] = [x.name for x in node.names]
        return node

    def get_imports(self):
        self.visit(self.tree)
        return self.__imports

    def get_sv(self):
        self.visit(self.tree)
        return self.__sv

    def mutate(self):
        with open(self.file, "w") as f:
            content = astor.to_source(self.visit(self.tree))
            f.write(
                black.format_file_contents(content, fast=False, mode=black.FileMode())
            )
