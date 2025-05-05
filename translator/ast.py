from ast import AST

from ast import PyCF_ONLY_AST, PyCF_TYPE_COMMENTS


def parse(
    source,
    filename="<unknown>",
    mode="exec",
    *,
    type_comments=False,
    feature_version=None,
):
    flags = PyCF_ONLY_AST
    if type_comments:
        flags |= PyCF_TYPE_COMMENTS
    if feature_version is None:
        feature_version = -1
    elif isinstance(feature_version, tuple):
        major, minor = feature_version  # Should be a 2-tuple.
        if major != 3:
            raise ValueError(f"Unsupported major version: {major}")
        feature_version = minor
    # Else it should be an int giving the minor version for 3.x.
    return compile(source, filename, mode, flags, _feature_version=feature_version)


def generate_tree(text: str) -> AST:
    tree = parse(source=text, filename="<input_file>")
    return tree
