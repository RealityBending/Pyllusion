"""
PROTOTYPE - sketch of the two-panel chromostereopsis stimulus. Not part of the public API yet.

Layout (one panel)::

    +-----------------------------+
    |  dithered surround colour   |     <- e.g. blue on black
    |      +---------------+      |
    |      |  bare gap     |      |     <- undithered background
    |      |   +-------+   |      |
    |      |   | disc  |   |      |     <- e.g. red on black
    |      |   +-------+   |      |
    |      +---------------+      |
    +-----------------------------+

The full stimulus is two such panels side by side with the two colours swapped, so one panel shows a
red disc on a blue surround and the other a blue disc on a red surround.
"""
import numpy as np
import PIL.Image

from ..image.rescale import rescale
from .chromostereopsis_parameters import _chromostereopsis_parameters


def _chromostereopsis_panel(
    size=400,
    color_inner=(255, 0, 0),
    color_surround=(0, 0, 255),
    background=(0, 0, 0),
    radius=37.5,
    gap=6,
    density=0.5,
    density_inner=None,
    dither_size=2,
    dither=None,
    rng=None,
):
    """Draw a single dithered panel: a coloured disc inside a coloured surround, separated by a gap of
    bare background.

    Parameters
    ----------
    size : int
        Side of the (square) panel, in pixels.
    color_inner, color_surround, background : tuple
        RGB of the disc's pixels, of the surround's pixels, and of everything else.
    radius, gap : float
        Radius of the disc and width of the bare annulus, in pixels (fractional is fine). Kept in
        pixels rather than panel-relative units so that the disc lands on exactly the diameter the grid
        geometry asks for, instead of being discretised twice.
    density, density_inner : float
        Proportion of dither cells that get coloured, in the surround and in the disc.
    dither_size : int
        Side of a dither cell, in pixels.
    dither : np.ndarray
        A precomputed boolean dither mask, so that the two panels of a stimulus can share one. Built
        from `rng` if not given.
    rng : np.random.Generator
        Used to build the dither mask when `dither` is not supplied.
    """
    if density_inner is None:
        density_inner = density
    if rng is None:
        rng = np.random.default_rng()

    # Distance of every pixel from the centre of the panel, in pixels. The centre is put *on* a pixel
    # (rather than at (size - 1) / 2, which falls between pixels for an even panel) so that the disc
    # comes out at the same diameter whatever the panel's parity - otherwise an even panel loses a pixel.
    coords = np.arange(size) - size // 2
    distance = np.sqrt(coords[:, None] ** 2 + coords[None, :] ** 2)

    is_inner = distance <= radius
    is_surround = distance > radius + gap

    # Dither: a uniform draw per cell, blown up to `dither_size` pixels and cropped back. Thresholding
    # a shared draw (rather than a shared boolean mask) lets the two regions use different densities
    # while still being the same underlying pattern.
    if dither is None:
        dither = _chromostereopsis_dither(size, dither_size=dither_size, rng=rng)

    panel = np.zeros((size, size, 3), dtype=np.uint8)
    panel[:, :] = background
    panel[is_inner & (dither < density_inner)] = color_inner
    panel[is_surround & (dither < density)] = color_surround

    return panel


def _chromostereopsis_dither(size, dither_size=2, rng=None):
    """Uniform [0, 1) draw per dither cell, upsampled to `size` x `size` pixels."""
    if rng is None:
        rng = np.random.default_rng()
    n_cells = int(np.ceil(size / dither_size))
    cells = rng.random((n_cells, n_cells))
    return np.repeat(np.repeat(cells, dither_size, axis=0), dither_size, axis=1)[:size, :size]


def _chromostereopsis_image(parameters=None, width=800, height=600, **kwargs):
    """Draw the two-panel stimulus.

    Parameters
    ----------
    parameters : dict
        Output of :func:`_chromostereopsis_parameters`. Built from ``**kwargs`` if not given.
    width, height : int
        Size of the returned image. Defaults match the other illusions. The panels are sized and placed
        from the grid-unit geometry in ``parameters``, as in the rest of Pyllusion: sizes scale with the
        height, positions run from -1 to 1 across the width.
    **kwargs
        Passed to :func:`_chromostereopsis_parameters`.
    """
    if parameters is None:
        # width/height are forwarded because the automatic `size_panel` needs the aspect ratio
        parameters = _chromostereopsis_parameters(width=width, height=height, **kwargs)

    rng = np.random.default_rng(parameters["Seed"])

    # Grid units -> pixels, the same way _coord_circle() does it: sizes against the height, positions
    # against the width.
    panel_size = int(rescale(parameters["Size_Panel"], to=[0, height], scale=[0, 2]))

    # One shared dither pattern, or one per panel
    dither = None
    if parameters["Dither_Shared"] is True:
        dither = _chromostereopsis_dither(
            panel_size, dither_size=parameters["Dither_Size"], rng=rng
        )

    image = PIL.Image.new("RGB", (width, height), color=tuple(parameters["Color_Background"]))

    for side in ["Left", "Right"]:
        panel = _chromostereopsis_panel(
            size=panel_size,
            color_inner=parameters["Color_Inner_" + side],
            color_surround=parameters["Color_Surround_" + side],
            background=parameters["Color_Background"],
            radius=rescale(parameters["Size_" + side], to=[0, height], scale=[0, 2]) / 2,
            gap=rescale(parameters["Gap"], to=[0, height], scale=[0, 2]),
            density=parameters["Density"],
            density_inner=parameters["Density_Inner"],
            dither_size=parameters["Dither_Size"],
            dither=dither,
            rng=rng,
        )
        # Paste centred on the panel's grid position
        x = int(rescale(parameters["Position_" + side], to=[0, width], scale=[-1, 1]))
        image.paste(PIL.Image.fromarray(panel), (x - panel_size // 2, (height - panel_size) // 2))

    return image
