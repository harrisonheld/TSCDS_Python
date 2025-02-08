from os import path


def resource_path(relative_path):
    """Get absolute path to resource. This will work both in-development, and in a PyInstaller bundle."""
    return path.abspath(path.join(path.dirname(__file__), relative_path))


def distance_chess(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))
