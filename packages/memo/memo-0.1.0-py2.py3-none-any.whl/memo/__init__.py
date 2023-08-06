from ._error import NotInstalled
from ._grid import grid, random_grid
from ._base import memlist, memfile, memfunc
from ._common import capture_time

try:
    from memo._http import memweb
except ModuleNotFoundError:
    memweb = NotInstalled("memweb", "web")

try:
    from memo._wandb import memwandb
except ModuleNotFoundError:
    memwandb = NotInstalled("memwandb", "wandb")


__version__ = "0.1.0"
__all__ = [
    "grid",
    "random_grid",
    "memlist",
    "memfile",
    "memfunc",
    "memweb",
    "memwandb",
    "capture_time"
]
