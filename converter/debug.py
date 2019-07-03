def print_structure(root):
    """Prints the structure of the xml tags for a given root element
    """
    structure = get_structure(root)
    _print_structure_part(structure, 0)


def _print_structure_part(structure, level):
    """recursive call to print the parts of the xml tree
    """
    for key, val in structure.items():
        print('\t' * level + key)
        _print_structure_part(val, level + 1)


def get_structure(root):
    """Recursively build the xml structure of the given root element
    """
    structure = {}
    for child in root:
        if child.tag not in structure:
            structure[child.tag] = get_structure(child)
    return structure
