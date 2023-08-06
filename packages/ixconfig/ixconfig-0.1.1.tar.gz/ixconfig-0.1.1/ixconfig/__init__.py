from . import core
from .core import *

def main():
    import fire
    fire.Fire({'if': Ifc, 'iw': Iwc})
