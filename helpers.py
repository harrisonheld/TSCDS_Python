from os import path


def resource_path(relative_path):
    """Get absolute path to resource. This will work both in-development, and in a PyInstaller bundle."""
    return path.abspath(path.join(path.dirname(__file__), relative_path))
