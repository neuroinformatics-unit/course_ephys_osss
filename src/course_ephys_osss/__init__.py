"""Course materials for the OSSS Extracellular Ephys 2026 Course."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("course_ephys_osss")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = ["__version__"]