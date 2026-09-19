"""
PROTOTYPE - sketch of the two-panel chromostereopsis stimulus. Not part of the public API yet.

Layout (one panel)::

    +-----------------------------+
    |  dithered surround colour   |     <- e.g. blue pixels on black
    |      +---------------+      |
    |      |  black gap    |      |     <- unfilled annulus
    |      |   +-------+   |      |
    |      |   | inner |   |      |     <- e.g. red pixels on black
    |      |   +-------+   |      |
    |      +---------------+      |
    +-----------------------------+

The full stimulus is two such panels side by side with the two colours swapped, so one panel shows a
red disc on a blue surround and the other a blue disc on a red surround.
"""
import numpy as np
import PIL.Image


def _chromostereopsis_panel(
    size=400,
    color_inner=(255, 0, 0),
    color_surround=(0, 0, 255),
    background=(0, 0, 0),
    radius=0.58,
    gap=0.08,
    density=0.5,
    dither_size=1,
    rng=None,
):
    """Draw a single dithered panel: a coloured disc inside a coloured surround, separated by a gap of
    bare background.

    Parameters
    ----------
    size : int
        Side of the (square) panel, in pixels.
    color_inner, color_surround : tuple
        RGB of the dithered pixels of the disc and of the surround.
    background : tuple
        RGB of the undithered pixels (and of the gap annulus).
    radius : float
        Radius of the inner disc, as a proportion of half the panel side (1 = disc touches the edges).
    gap : float
        Width of the bare annulus between disc and surround, in the same units as ``radius``.
    density : float
        Proportion of cells that get coloured in the dithered regions (0-1). 1 gives solid fills.
    dither_size : int
        Side of a dither cell, in pixels. 1 gives per-pixel noise; larger values give the chunky
        pixel-art look that the (anecdotal) reports say strengthens the effect.
    rng : np.random.Generator
        Passed in so that the two panels of a stimulus can share a generator.
    """
    if rng is None:
        rng = np.random.default_rng()

    # Distance of every pixel from the centre, in units of half the panel side
    coords = (np.arange(size) - (size - 1) / 2) / ((size - 1) / 2)
    distance = np.sqrt(coords[:, None] ** 2 + coords[None, :] ** 2)

    # Which region each pixel belongs to
    is_inner = distance <= radius
    is_surround = distance > radius + gap

    # Dither: independently keep each cell with probability `density`, then blow the cells up to
    # `dither_size` pixels and crop back (the last cell may be partial)
    n_cells = int(np.ceil(size / dither_size))
    dither = rng.random((n_cells, n_cells)) < density
    dither = np.repeat(np.repeat(dither, dither_size, axis=0), dither_size, axis=1)[:size, :size]

    panel = np.zeros((size, size, 3), dtype=np.uint8)
    panel[:, :] = background
    panel[is_inner & dither] = color_inner
    panel[is_surround & dither] = color_surround

    return panel


def _chromostereopsis_image(
    difference=0,
    illusion_strength=0,
    width=800,
    height=400,
    color1=(255, 0, 0),
    color2=(0, 0, 255),
    background=(0, 0, 0),
    radius=0.58,
    gap=0.08,
    density=0.5,
    dither_size=1,
    margin=0.05,
    seed=None,
):
    """Draw the two-panel stimulus.

    Parameters
    ----------
    difference : float
        Objective size difference between the two discs: the radius of the left disc relative to the
        right (e.g. ``difference=0.1`` makes the left disc 10% larger). This is the attribute the
        observer would be asked to judge.
    illusion_strength : float
        Signed. The sign sets which panel receives the disc drawn in ``color1`` (positive = left
        panel), i.e. it flips the predicted direction of the depth/size bias. The magnitude currently
        does nothing - see the open question in ``Chromostereopsis.py``.
    width, height : int
        Size of the returned image. Each panel is a square of side ``height``.
    color1, color2 : tuple
        The two colours. ``color1`` defaults to red, ``color2`` to blue.
    background : tuple
        Background, and colour of the gap annulus. The literature effect is measured on black.
    radius, gap, density, dither_size
        Passed to :func:`_chromostereopsis_panel`.
    margin : float
        Space between and around the panels, as a proportion of the panel side.
    seed : int
        Seed for the dither pattern, for reproducible stimuli.
    """
    rng = np.random.default_rng(seed)

    panel_size = int(height * (1 - 2 * margin))

    # Objective size difference, applied symmetrically around `radius` (as in the size illusions)
    radius_left = radius * (1 + difference / 2)
    radius_right = radius * (1 - difference / 2)

    # The sign of illusion_strength swaps which colour is the disc
    if illusion_strength >= 0:
        inner_left, surround_left = color1, color2
    else:
        inner_left, surround_left = color2, color1
    inner_right, surround_right = surround_left, inner_left

    left = _chromostereopsis_panel(
        size=panel_size,
        color_inner=inner_left,
        color_surround=surround_left,
        background=background,
        radius=radius_left,
        gap=gap,
        density=density,
        dither_size=dither_size,
        rng=rng,
    )
    right = _chromostereopsis_panel(
        size=panel_size,
        color_inner=inner_right,
        color_surround=surround_right,
        background=background,
        radius=radius_right,
        gap=gap,
        density=density,
        dither_size=dither_size,
        rng=rng,
    )

    # Paste both panels onto the canvas
    image = PIL.Image.new("RGB", (width, height), color=tuple(background))
    y = (height - panel_size) // 2
    x_gap = int(panel_size * margin)
    total = 2 * panel_size + x_gap
    x = (width - total) // 2
    image.paste(PIL.Image.fromarray(left), (x, y))
    image.paste(PIL.Image.fromarray(right), (x + panel_size + x_gap, y))

    return image
