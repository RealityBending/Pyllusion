"""
Pyllusion submodule.
"""

from .delboeuf import delboeuf_parameters, delboeuf_image, delboeuf_psychopy
from .ebbinghaus import ebbinghaus_parameters, ebbinghaus_image, ebbinghaus_psychopy
from .ponzo import ponzo_parameters, ponzo_image, ponzo_psychopy
from .rodframe import rodframe_parameters, rodframe_image, rodframe_psychopy
from .mullerlyer import mullerlyer_parameters, mullerlyer_image, mullerlyer_psychopy
from .verticalhorizontal import verticalhorizontal_parameters, verticalhorizontal_image, verticalhorizontal_psychopy
from .zollner import zollner_parameters, zollner_image, zollner_psychopy
from .poggendorff import poggendorff_parameters, poggendorff_image, poggendorff_psychopy
from .contrast import contrast_parameters, contrast_image, contrast_psychopy
from .white import white_parameters, white_image
from .autostereogram import autostereogram
from .pareidolia import pareidolia

__all__ = [
    "delboeuf_parameters",
    "delboeuf_image",
    "delboeuf_psychopy",
    "ebbinghaus_parameters",
    "ebbinghaus_image",
    "ebbinghaus_psychopy",
    "ponzo_parameters",
    "ponzo_image",
    "ponzo_psychopy",
    "rodframe_parameters",
    "rodframe_image",
    "rodframe_psychopy",
    "mullerlyer_parameters",
    "mullerlyer_image",
    "mullerlyer_psychopy",
    "verticalhorizontal_parameters",
    "verticalhorizontal_image",
    "verticalhorizontal_psychopy",
    "zollner_parameters",
    "zollner_image",
    "zollner_psychopy",
    "poggendorff_parameters",
    "poggendorff_image",
    "poggendorff_psychopy",
    "contrast_parameters",
    "contrast_image",
    "contrast_psychopy",
    "white_parameters",
    "white_image",
    "autostereogram",
    "pareidolia",
]
