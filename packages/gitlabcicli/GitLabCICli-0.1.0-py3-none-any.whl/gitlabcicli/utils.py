"""Some useful functions."""


def right_replace(string: str, old: str, new: str, count: int = -1) -> str:
    """Like ``str.replace`` but go from right to left. Only makes sense for ``count`` > 0."""
    return string[::-1].replace(old[::-1], new[::-1], count)[::-1]
