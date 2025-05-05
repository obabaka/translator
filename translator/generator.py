from ast import NodeVisitor, AST
import ast


class Operators(NodeVisitor):
    def visit_BinOp(self, node) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.visit(node.op)
        return f"({left} {op} {right})"

    def visit_BoolOp(self, node) -> str:
        op = self.visit(node.op)
        values = []
        for expr in node.values:
            values.append(self.visit(expr))

        return op.join(values)

    def visit_Compare(self, node) -> str:
        left = self.visit(node.left)
        ops = [self.visit(op) for op in node.ops]
        comparators = [self.visit(comp) for comp in node.comparators]
        comparisons = " && ".join(
            f"{left} {ops[i]} {comparators[i]}" for i in range(len(ops))
        )
        return comparisons

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op = self.visit(node.op)
        return f"{op}{operand}"

    def visit_And(self, _) -> str:
        return "&&"

    def visit_Or(self, _) -> str:
        return "||"

    def visit_BitAnd(self, _) -> str:
        return "&"

    def visit_BitOr(self, _) -> str:
        return "|"

    def visit_BitXor(self, _) -> str:
        return "^"

    def visit_RShift(self, _) -> str:
        return ">>"

    def visit_LShift(self, _) -> str:
        return "<<"

    def visit_Invert(self, _) -> str:
        return "~"

    def visit_Not(self, _) -> str:
        return "!"

    def visit_UAdd(self, _) -> str:
        return "+"

    def visit_USub(self, _) -> str:
        return "-"

    def visit_Add(self, _) -> str:
        return "+"

    def visit_Sub(self, _) -> str:
        return "-"

    def visit_Mult(self, _) -> str:
        return "*"

    def visit_MatMult(self, _) -> str:
        raise RuntimeError("Operator '@' (MatMult) unsupported.")
        return None

    def visit_Pow(self, _) -> str:
        raise RuntimeError("Operator '**' (Pow) unsupported.")
        return None

    def visit_Div(self, _) -> str:
        return "/"

    def visit_FloorDiv(self, _) -> str:
        raise RuntimeError("Operator '//' (FloorDiv) unsupported.")
        return None

    def visit_Mod(self, _) -> str:
        return "%"

    def visit_Gt(self, _) -> str:
        return ">"

    def visit_GtE(self, _) -> str:
        return ">="

    def visit_Lt(self, _) -> str:
        return "<"

    def visit_LtE(self, _) -> str:
        return "<="

    def visit_Eq(self, _) -> str:
        return "=="

    def visit_NotEq(self, _) -> str:
        return "!="

    def visit_In(self, _) -> str:
        raise RuntimeError("Operator 'in' unsupported.")
        return None

    def visit_Is(self, _) -> str:
        raise RuntimeError("Operator 'is' unsupported.")
        return None

    def visit_IsNot(self, _) -> str:
        raise RuntimeError("Operator 'is not' unsupported.")
        return None

    def visit_NotIn(self, _) -> str:
        raise RuntimeError("Operator 'not in' unsupported.")
        return None


class FlowControlStmts(NodeVisitor):
    def visit_Pass(self, _) -> str:
        # TODO: Подумать, можно ли вернутиь пустой блок (значение)
        # raise RuntimeError("Keyword 'pass' unsupported.")
        # return None
        return ""

    def visit_Break(self, _) -> str:
        return f"{'\t'*self.tabindex}break;"

    def visit_Continue(self, _) -> str:
        return f"{'\t'*self.tabindex}continue;"

    def visit_Return(self, node) -> str:
        value = self.visit(node.value) if node.value else ""
        return f"{'\t'*self.tabindex}return {value};"

    def visit_Yield(self, _) -> str:
        raise RuntimeError("Keyword 'yield' unsupported.")
        return None

    def visit_YieldFrom(self, _) -> str:
        raise RuntimeError("Keyword 'yield from' unsupported.")
        return None

    def visit_Raise(self, _) -> str:
        # TODO: write me
        raise RuntimeError("Keyword 'raise' not realised yet.")
        return None

    def visit_Assert(self, _) -> str:
        # TODO: write me
        raise RuntimeError("Keyword 'assert' not realised yet.")
        return None


class ConditionalOperators(NodeVisitor):
    def visit_If(self, node) -> str:
        self._indent()
        test = self.visit(node.test)

        body = []
        for expr in node.body:
            body.append(self.visit(expr))

        if test == '__name__ == "__main__"':
            if node.orelse:
                raise RuntimeError(
                    "The entry point directive should not have branches."
                )

            self.entrypoint_flag = True
            entrypoint = f'\n\nint main() {{\n{"\n".join(body)}\n{'\t'*self.tabindex}return 0;\n}}'
            return entrypoint

        orelse = []
        for expr in node.orelse:
            orelse.append(self.visit(expr))

        if orelse:
            else_block = f'else {{\n{"\n".join(orelse)}\n{'\t'*(self.tabindex-1)}}}'

        else:
            else_block = ""

        result = f'{'\t'*(self.tabindex-1)}if ({test}) {{\n{"\n".join(body)}\n{'\t'*(self.tabindex-1)}}} {else_block}'
        self._dedent()
        return result

    def visit_IfExp(self, node) -> str:
        test = self.visit(node.test)
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        return f"({test}) ? {body} : {orelse};"


class FunctionsAndClasses(NodeVisitor):
    def visit_Lambda(self, node) -> str:
        arguments = self.visit(node.args)
        args = ", ".join(arguments)
        body = self.visit(node.body)
        return f"[](int {args}) {{ return {body}; }};"

    def visit_Call(self, node) -> str:
        if node.keywords:
            raise RuntimeError("Keyword arguments unsupported.")
            return None

        func = self.visit(node.func)
        arguments = []
        for arg in node.args:
            arguments.append(self.visit(arg))

        args = ", ".join(arguments)
        if func == "print":
            return f"cout << {args} << endl"

        else:
            return f"{func}({args})"

    def visit_FunctionDef(self, node):
        self._indent()
        if node.decorator_list:
            raise RuntimeError("Function decorators unsupported.")

        name = node.name
        args = self.visit(node.args)
        annotation = self.visit(node.returns) if node.returns else "None"
        vartype = self._convert_annotation(annotation)

        body = []
        for stmt in node.body:
            body.append(self.visit(stmt))

        func = f"\n{'\t'*(self.tabindex-1)}{vartype} {name}({', '.join(args)}) {{\n{'\n'.join(body)}\n{'\t'*(self.tabindex-1)}}}"
        self._dedent()
        return func

    def visit_AsyncFunctionDef(self, node):
        raise RuntimeError("Async functions unsupported.")
        return None

    def visit_ClassDef(self, node):
        self._indent()
        name = node.name
        bases = [self.visit(base) for base in node.bases] if node.bases else ""
        body = [self.visit(stmt) for stmt in node.body]

        if bases:
            bases = list(map(lambda x: "public " + x, bases))
            bases = f": {', '.join(bases)}"

        class_ = f"\n{'\t'*(self.tabindex-1)}class {name}{bases} {{\n{'\t'*(self.tabindex-1)}publick:\n{'\n'.join(body)}\n{'\t'*(self.tabindex-1)}}};\n"
        self._dedent()
        return class_


class Assigments(NodeVisitor):
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Tuple):
            raise RuntimeError("Group assigment unsupported.")
            return None

        target = self.visit(node.targets[0])
        value = self.visit(node.value)
        vartype = "auto"

        return f"{'\t'*self.tabindex}{vartype} {target} = {value};"

    def visit_AnnAssign(self, node):
        target = self.visit(node.target)
        value = self.visit(node.value) if node.value else ""
        annotation = self.visit(node.annotation)
        vartype = self._convert_annotation(annotation)

        if value:
            value = f" = {value}"

        return f"{'\t'*self.tabindex}{vartype} {target}{value};"

    # TODO: write me
    def visit_AugAssign(self, node): ...


class Collections(NodeVisitor):
    def visit_Set(self, node):
        # TODO: Write me
        raise RuntimeError("Collection 'set' not realised yet.")
        return None

    def visit_List(self, node):
        # TODO: Write me
        raise RuntimeError("Collection 'list' not realised yet.")
        return None

    def visit_Dict(self, node):
        # TODO: Write me
        raise RuntimeError("Collection 'dict' not realised yet.")
        return None

    def visit_Tuple(self, node):
        # TODO: Write me
        raise RuntimeError("Collection 'tuple' not realised yet.")
        return None


class Imports(NodeVisitor):
    def visit_Import(self, node) -> None:
        for name in node.names:
            module = f"#include <{self.visit(name)}.h>"
            self.include_directives[module] = ...

        return None

    def visit_ImportFrom(self, node) -> str:
        # TODO: Try to convert From Import to regular Import
        raise RuntimeError("From import unsupported.")
        return None


class Loops(NodeVisitor):
    def visit_While(self, node):
        # TODO: orelse
        self._indent()
        test = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        loop = f"\nwhile ({test}) {{\n{'\n'.join(body)}\n{'\t'*(self.tabindex-1)}}}\n"
        self._dedent()
        return loop

    def visit_For(self, node):
        # TODO: orelse
        self._indent()
        target = self.visit(node.target)
        iter_ = self.visit(node.iter)
        body = [self.visit(stmt) for stmt in node.body]
        loop = f"\nfor (auto {target} : {iter_}) {{\n{'\n'.join(body)}\n{'\t'*(self.tabindex-1)}}}\n"
        self._dedent()
        return loop


class CodeGenerator(
    Operators,
    FlowControlStmts,
    ConditionalOperators,
    Assigments,
    Collections,
    Imports,
    FunctionsAndClasses,
    Loops,
):
    def __init__(self, tree: AST) -> None:
        self.tabindex = 0
        self.include_directives = {
            "#include <iostream>": ...,
            "#include <string>": ...,
        }
        self.namespace_directives = {
            "using namespace std;": ...,
        }
        self.statements = []
        self.entrypoint_flag: bool = False
        self.tree = tree

    def _convert_annotation(self, annotation: str) -> None:
        typemap = {
            "str": "string",
            "int": "int",
            "bool": "bool",
            "float": "float",
            "None": "void",
            None: "void",
            "nill": "void",
        }
        vartype = typemap.get(annotation)
        if vartype is None:
            raise RuntimeError(f"Annotation '{vartype}' unsupported.")
            return None

        return vartype

    def _indent(self):
        self.tabindex += 1

    def _dedent(self):
        self.tabindex -= 1

    def generate(self) -> str:
        self.visit(self.tree)

        if not self.entrypoint_flag:
            raise RuntimeError(
                "The directive `if __name__ == '__main__':` is mandatory."
            )

        code = "{include}{statements}{entrypoint}"
        code = code.format(
            include="\n".join(self.include_directives.keys()) + "\n\n",
            statements="\n".join(self.namespace_directives.keys()) + "\n\n",
            entrypoint="\n".join(self.statements) + "\n\n",
        )

        return code

    def visit_Module(self, node) -> str:
        """Рекурсивный проход по каждому выражению в file (tabindex 0)"""
        for stmt in node.body:
            statement = self.visit(stmt)
            if statement is not None:
                self.statements.append(statement)

    def visit_Name(self, node) -> str:
        return node.id

    def visit_Constant(self, node) -> str:
        if isinstance(node.value, str):
            return f'"{node.value}"'

        elif isinstance(node.value, float):
            return f"{node.value}f"

        elif node.value is None:
            return "nill"

        return str(node.value)

    def visit_arguments(self, node) -> str:
        if node.args:
            arguments = []
            for arg in node.args:
                arguments.append(self.visit(arg))

            return arguments

        else:
            return []

        # TODO: implement arguments when define a function, etc.
        raise RuntimeError("Other arguments variants not realised yet.")
        return None

    def visit_arg(self, node):
        name = node.arg
        annotation = self.visit(node.annotation) if node.annotation else "int"
        vartype = self._convert_annotation(annotation)

        return f"{vartype} {name}"

    def visit_Expr(self, node):
        return f"{'\t'*self.tabindex}{self.visit(node.value)};"

    def visit_Subscript(self, node):
        if node.slice == ast.Slice:
            raise RuntimeError("Framed slice not realised yet.")
            return None

        value = self.visit(node.value)
        slice_ = self.visit(node.slice)

        return f"{value}[{slice_}]"

    def visit_alias(self, node) -> str:
        module = node.name.split(".")[-1]
        return module

    def visit_Attribute(self, node) -> str:
        value = self.visit(node.value)
        attr = node.attr

        return f"{value}.{attr}"
