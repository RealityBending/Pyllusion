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

from .chromostereopsis_parameters import _chromostereopsis_parameters


def _chromostereopsis_panel(
    size=400,
    color_inner=(255, 0, 0),
    color_surround=(0, 0, 255),
    background=(0, 0, 0),
    radius=0.58,
    gap=0.08,
    density=0.5,
    density_inner=None,
    dither_size=10,
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
        Radius of the disc and width of the bare annulus, as a proportion of half the panel side.
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

    # Distance of every pixel from the centre, in units of half the panel side
    coords = (np.arange(size) - (size - 1) / 2) / ((size - 1) / 2)
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


def _chromostereopsis_dither(size, dither_size=10, rng=None):
    """Uniform [0, 1) draw per dither cell, upsampled to `size` x `size` pixels."""
    if rng is None:
        rng = np.random.default_rng()
    n_cells = int(np.ceil(size / dither_size))
    cells = rng.random((n_cells, n_cells))
    return np.repeat(np.repeat(cells, dither_size, axis=0), dither_size, axis=1)[:size, :size]


def _chromostereopsis_image(parameters=None, width=800, height=400, margin=0.05, **kwargs):
    """Draw the two-panel stimulus.

    Parameters
    ----------
    parameters : dict
        Output of :func:`_chromostereopsis_parameters`. Built from ``**kwargs`` if not given.
    width, height : int
        Size of the returned image. Each panel is a square, sized to fit the height.
    margin : float
        Space between and around the panels, as a proportion of the panel side.
    **kwargs
        Passed to :func:`_chromostereopsis_parameters`.
    """
    if parameters is None:
        parameters = _chromostereopsis_parameters(**kwargs)

    rng = np.random.default_rng(parameters["Seed"])
    panel_size = int(height * (1 - 2 * margin))

    # One shared dither pattern, or one per panel
    dither = None
    if parameters["Dither_Shared"] is True:
        dither = _chromostereopsis_dither(
            panel_size, dither_size=parameters["Dither_Size"], rng=rng
        )

    panels = []
    for side, radius in [("Left", parameters["Size_Left"]), ("Right", parameters["Size_Right"])]:
        panels.append(
            _chromostereopsis_panel(
                size=panel_size,
                color_inner=parameters["Color_Inner_" + side],
                color_surround=parameters["Color_Surround_" + side],
                background=parameters["Color_Background"],
                radius=radius,
                gap=parameters["Gap"],
                density=parameters["Density"],
                density_inner=parameters["Density_Inner"],
                dither_size=parameters["Dither_Size"],
                dither=dither,
                rng=rng,
            )
        )

    # Paste both panels onto the canvas
    image = PIL.Image.new("RGB", (width, height), color=tuple(parameters["Color_Background"]))
    y = (height - panel_size) // 2
    x_gap = int(panel_size * margin)
    x = (width - (2 * panel_size + x_gap)) // 2
    image.paste(PIL.Image.fromarray(panels[0]), (x, y))
    image.paste(PIL.Image.fromarray(panels[1]), (x + panel_size + x_gap, y))

    return image
