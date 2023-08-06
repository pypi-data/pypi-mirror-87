pytest_plugins = ['pytester']

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

pytest_plugins = "pytester"

REPOSITORY_ROOT = pathlib.Path(__file__).parent
