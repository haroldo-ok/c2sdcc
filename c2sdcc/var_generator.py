from pycparser import c_ast
import collections

class VarGenerator(c_ast.NodeVisitor):
    """ Moves local variable declarations to the top of each function.
    """

    def __init__(self, **kwargs):
        self.decls = []

        return super().__init__(**kwargs)

    def generic_visit(self, node):
        res = super().generic_visit(node)

        for name in node.__slots__:
            attr = getattr(node, name, None)
            if self._is_declaration(attr):
                self.visit(attr)
                self.decls.append(attr)

                asgn = self._to_assignment(attr)
                setattr(node, name, asgn)

            if isinstance(attr, list):
                for idx, item in enumerate(attr):
                    if self._is_declaration(item):
                        self.visit(item)
                        self.decls.append(item)

                        asgn = self._to_assignment(item)
                        attr[idx] = asgn

        return res 

    def visit_Compound(self, n):
        return self.generic_visit(n)

    def visit_DeclList(self, n):
        return self.generic_visit(n)

    def visit_FuncDef(self, n):
        """
        decl = self.visit(n.decl)
        body = self.visit(n.body)
        if n.param_decls:
            for p in n.param_decls:
                self.visit(p)
        """
        self.generic_visit(n)

        for decl in self.decls:
            decl.init = None

        n.body.block_items = self.decls + [None] + n.body.block_items

        return n

    def _is_declaration(self, attr):
        return isinstance(attr, c_ast.Decl) and isinstance(attr.type, c_ast.TypeDecl)

    def _to_assignment(self, attr):
        return c_ast.Assignment('=', c_ast.ID(attr.name), attr.init) if attr.init else None

