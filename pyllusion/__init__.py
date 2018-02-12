"""
The Pyllusion module.
"""
__version__ = "0.0.3"




# Import first submodule
from .Delboeuf import *


# Get path of stimuli images
import inspect
pyllusion_path = inspect.getfile(delboeuf_compute)  # Get path of a random function
pyllusion_path = pyllusion_path.split("Delboeuf.py")[0] 
pyllusion_path = pyllusion_path + "stimuli\\"

# Import rest of submodules
from .Pareidolia import *
from .Ponzo import *
from .RodFrame import *
from .Zollner import *
from .TFM import *