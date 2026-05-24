 """
Safe Formula Execution

Lightweight, restricted expression evaluation for the Grokulator.
Uses ast with a tight allowlist to remain defensive while still being useful.

Features for ease of use and troubleshooting:
- Clear, contextual error messages
- Optional debug mode (shows parsed tree + used names)
- Validation-only mode (check safety without executing)
- Variable usage reporting
- Integration hooks for provenance
"""

import ast
from typing import Any, Dict, Set, Tuple, Optional


ALLOWED_NODES = {
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
    ast.USub, ast.UAdd, ast.Name, ast.Load, ast.Call, ast.keyword
}

ALLOWED_NAMES = {
    "abs", "round", "min", "max", "sum", "len",
    "int", "float", "bool", "str"
}


class UnsafeExpressionError(Exception):
    """Raised when an expression contains unsafe operations or names."""
    pass


def _get_used_names(node: ast.AST) -> Set[str]:
    """Recursively collect all Name nodes in the AST."""
    names = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names.add(child.id)
    return names


def validate_expression(expression: str) -> Tuple[bool, Optional[str]]:
    """
    Check if an expression is safe to evaluate.
    Returns (is_safe, error_message).
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        return False, f"Syntax error: {e}"

    for node in ast.walk(tree):
        if type(node) not in ALLOWED_NODES:
            return False, f"Unsafe node type: {type(node).__name__}"
        if isinstance(node, ast.Name) and node.id not in ALLOWED_NAMES:
            # Allow variable names from context; only block dangerous builtins
            if node.id.startswith("_"):
                return False, f"Unsafe name (starts with underscore): {node.id}"
    return True, None


def execute_formula(
    expression: str,
    context: Optional[Dict[str, Any]] = None,
    debug: bool = False
) -> Dict[str, Any]:
    """
    Safely evaluate a formula expression with optional context variables.

    Returns a dict with:
    - success: bool
    - result: value or None
    - error: message if failed
    - used_variables: set of variable names referenced
    - debug_info: present if debug=True
    """
    context = context or {}
    result = {
        "success": False,
        "result": None,
        "error": None,
        "used_variables": set(),
    }

    is_safe, error_msg = validate_expression(expression)
    if not is_safe:
        result["error"] = error_msg
        return result

    try:
        tree = ast.parse(expression, mode="eval")
        used_names = _get_used_names(tree)
        result["used_variables"] = used_names

        # Build safe evaluation environment
        safe_globals = {"__builtins__": {}}
        safe_locals = {name: context[name] for name in used_names if name in context}

        # Add allowed names
        for name in ALLOWED_NAMES:
            if name in __builtins__:
                safe_globals[name] = __builtins__[name]

        evaluated = eval(compile(tree, "<string>", "eval"), safe_globals, safe_locals)
        result["success"] = True
        result["result"] = evaluated

        if debug:
            result["debug_info"] = {
                "parsed_tree": ast.dump(tree, indent=2),
                "used_names": list(used_names),
                "context_keys": list(context.keys())
            }

    except Exception as e:
        result["error"] = f"Execution error: {type(e).__name__}: {e}"

    return result