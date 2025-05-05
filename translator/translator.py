from .ast import generate_tree
from ast import dump
from .generator import CodeGenerator


class Translator:
    """
    The main handler class, managing the flow
    of program execution.
    """

    @classmethod
    def translate(cls, text: str, debug: bool = False) -> None:
        """__summary__"""

        error = None
        code = None
        try:
            tree = generate_tree(text)
            if debug:
                print(dump(tree, indent=4))
            generator = CodeGenerator(tree)
            code = generator.generate()

        except Exception as e:
            error = e

        return code, error
