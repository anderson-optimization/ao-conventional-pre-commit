from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("ao-conventional-pre-commit")
except PackageNotFoundError:
    # package is not installed
    pass
