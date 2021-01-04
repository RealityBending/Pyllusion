"""
The Pyllusion module.
"""
__version__ = "0.0.6"


# Import rest of submodules
from .illusion import *

# Import first submodule
from .image import *
from .movement import *


# Get path of stimuli images
# import inspect
# pyllusion_path = inspect.getfile(autostereogram)  # Get path of a random function
# pyllusion_path = pyllusion_path.split("autostereogram.py")[0]
# pyllusion_path = pyllusion_path + "stimuli\\"
