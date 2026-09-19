"""
PROTOTYPE - parameters for the two-panel chromostereopsis stimulus. Not part of the public API yet.
"""
import numpy as np

from ..image.utilities import _color


# ---------------------------------------------------------------------------------------------------
# Luminance helpers
#
# Same convention as pyllusion.analyze_luminance(): linearize sRGB, then weight the channels by the
# sRGB primaries. "Relative luminance" is therefore 0 (black) to 1 (white).
# ---------------------------------------------------------------------------------------------------
def _srgb_to_linear(rgb):
    rgb = np.asarray(rgb, dtype=float) / 255.0
    return np.where(rgb <= 0.04045, rgb / 12.92, np.power((rgb + 0.055) / 1.055, 2.4))


def _linear_to_srgb(linear):
    linear = np.clip(np.asarray(linear, dtype=float), 0, 1)
    srgb = np.where(linear <= 0.0031308, linear * 12.92, 1.055 * np.power(linear, 1 / 2.4) - 0.055)
    return tuple(int(round(c)) for c in np.clip(srgb * 255.0, 0, 255))


def _relative_luminance(rgb):
    """Relative luminance (0-1) of an RGB colour."""
    linear = _srgb_to_linear(rgb)
    return float(0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2])


def _scale_luminance(rgb, factor):
    """Scale a colour's luminance by `factor`, in linear light (so it is a real luminance scaling, not
    a scaling of the 8-bit code values). Hue is preserved; the result is clipped at white."""
    return _linear_to_srgb(_srgb_to_linear(rgb) * factor)


# ---------------------------------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------------------------------
def _disc_area(radius):
    """Area of a disc of radius `radius` clipped to the panel, in units where the panel has area 4
    (i.e. the panel runs from -1 to 1 on each axis, so `radius` is in units of half the panel side).

    Exact: for radius <= 1 the disc is inscribed; beyond that it is clipped by the four sides.
    """
    radius = float(radius)
    if radius <= 0:
        return 0.0
    if radius <= 1:
        return np.pi * radius ** 2
    if radius >= np.sqrt(2):  # disc covers the whole panel
        return 4.0
    # Subtract the four circular segments that stick out past the sides
    segment = radius ** 2 * np.arccos(1 / radius) - np.sqrt(radius ** 2 - 1)
    return np.pi * radius ** 2 - 4 * segment


def _size_panel_area_matched(size, gap):
    """Side of the panel at which the disc and the surround have equal area, given a disc of diameter
    `size` and an annulus of width `gap` (both in grid units).

    Matching the two areas means each panel holds equal amounts of the two colours, which is what makes
    the two panels of a stimulus equally luminous overall. Solving
    ``pi * r**2 == S**2 - pi * (r + gap)**2`` for the panel side S gives the closed form below. Exact
    only when difference=0.
    """
    radius = size / 2
    return float(np.sqrt(np.pi * (radius ** 2 + (radius + gap) ** 2)))


# ---------------------------------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------------------------------
def _chromostereopsis_parameters(
    difference=0,
    illusion_strength=0,
    size=0.25,
    size_panel=None,
    gap=0.02,
    distance=1,
    color1="red",
    color2="blue",
    luminance1=1.0,
    luminance2=1.0,
    equiluminant=False,
    background="black",
    density=0.5,
    density_inner=None,
    dither_size=2,
    dither_shared=True,
    seed=None,
):
    """Compute the parameters of the two-panel chromostereopsis stimulus.

    Sizes and distances use the same grid units as the rest of Pyllusion: sizes are a proportion of the
    image height (``size=2`` spans the full height) and positions run from -1 to 1 across the width.
    The defaults are chosen to match the Delboeuf illusion, so the two can be used side by side in the
    same battery: ``size=0.25`` and ``distance=1`` give 75 px discs with centres 400 px apart on the
    default 800x600 canvas, exactly like ``pyllusion.Delboeuf()``.

    Parameters
    ----------
    difference : float
        The objective size difference between the two discs: the diameter of the left disc relative to
        the right (e.g. ``difference=0.1`` makes the left disc 10% larger, ``-0.1`` 10% smaller).
        This is the attribute the observer is asked to judge.
    illusion_strength : float
        Provisional. Only its *sign* is used, and it sets which panel receives the disc drawn in
        ``color1`` (>= 0 puts it on the left). What the magnitude should scale is still open - see the
        notes in ``Chromostereopsis.py`` - so for now any positive value behaves like any other.

    Geometry
    --------
    size : float
        Diameter of the discs, in grid units. Matches Delboeuf's inner circle default of 0.25.
    size_panel : float
        Side of the square panels, in grid units. Left at ``None`` (the default) it is set to the value
        that makes disc area equal surround area, so each panel holds equal amounts of both colours and
        the two panels are equally luminous overall. Setting it by hand reintroduces that brightness
        difference, which is reported as ``Luminance_Panel_Ratio``. The automatic match is exact only at
        ``difference=0``; past that a residual remains, also reported there.
    gap : float
        Width of the bare background annulus between each disc and its surround ("the black outline"),
        in grid units. Set to 0 for the disc to abut the surround directly.
    distance : float
        Distance between the centres of the two panels, in grid units. Matches Delboeuf's default of 1.

    Colour and luminance
    --------------------
    color1, color2 : str or tuple
        The two colours, as a name or an RGB tuple. ``color1`` is the one whose disc position is set by
        the sign of ``illusion_strength``. Defaults to the classic red/blue pair; red/green and
        yellow/blue are the other pairings reported in the literature.
    luminance1, luminance2 : float
        Multipliers on each colour's luminance, applied in linear light so that ``0.5`` really is half
        the luminance. Values that would clip past white are clipped. Lowering the red is the standard
        way to weaken the illusion.
    equiluminant : bool
        If True, scale the brighter of the two colours down until both have the same relative
        luminance, after ``luminance1``/``luminance2`` are applied. Note this is an approximation:
        true equiluminance is observer-specific and would need flicker photometry.
    background : str or tuple
        Background, and colour of the gap annulus. Black maximises the effect; raising it toward white
        is the literature's background-brightness manipulation, which weakens and can reverse the
        illusion. Use a grey (e.g. ``"#808080"``) to lower the contrast of both colours at once - note
        that on pure black every colour has a Michelson contrast of 1, so a non-black background is
        needed for ``Contrast_Color*`` to carry any information.

    Dither
    ------
    density : float
        Proportion of dither cells that are coloured, 0-1, in the surround (and in the disc unless
        ``density_inner`` is set). 1 gives solid fills. This scales the mean luminance of a region
        without changing the colour of its pixels, so it is a second, independent luminance knob.
    density_inner : float
        Density for the disc only. Defaults to ``density``.
    dither_size : int
        Side of a dither cell in pixels. 1 gives per-pixel noise, larger values the chunky pixel-art
        look that is anecdotally reported to strengthen the effect. This is a pixel quantity, so it does
        not scale with the image: at the default 800x600 the panels are ~102 px, and the default of 2
        gives ~50 dither cells across a panel. Render bigger and you must raise it to keep the same
        look - ``Dither_Cells_Across`` in the returned dict is the scale-invariant number to hold
        constant.
    dither_shared : bool
        If True (default) both panels use the same dither pattern, so colour assignment is the only
        difference between them.
    seed : int
        Seed for the dither pattern.
    """
    if density_inner is None:
        density_inner = density

    # --- Colours -----------------------------------------------------------------------------------
    rgb1 = _scale_luminance(_color(color1), luminance1)
    rgb2 = _scale_luminance(_color(color2), luminance2)

    luminance_1 = _relative_luminance(rgb1)
    luminance_2 = _relative_luminance(rgb2)

    if equiluminant is True:
        target = min(luminance_1, luminance_2)
        if luminance_1 > target and luminance_1 > 0:
            rgb1 = _scale_luminance(rgb1, target / luminance_1)
        if luminance_2 > target and luminance_2 > 0:
            rgb2 = _scale_luminance(rgb2, target / luminance_2)
        luminance_1, luminance_2 = _relative_luminance(rgb1), _relative_luminance(rgb2)

    rgb_background = _color(background)
    luminance_background = _relative_luminance(rgb_background)

    # Michelson contrast of each colour against the background. Bounded [-1, 1] and well defined on a
    # black background, unlike Weber contrast which goes to infinity there.
    def _contrast(luminance):
        total = luminance + luminance_background
        return (luminance - luminance_background) / total if total > 0 else 0.0

    # --- Geometry (grid units) ---------------------------------------------------------------------
    area_matched = size_panel is None
    if area_matched is True:
        size_panel = _size_panel_area_matched(size, gap)

    size_left = size * (1 + difference / 2)
    size_right = size * (1 - difference / 2)

    position_left, position_right = -(distance / 2), (distance / 2)

    # Panel side in pixels at the default render height, only used to report Dither_Cells_Across
    size_panel_px = size_panel / 2 * 600

    # The area computations work in units of half the panel side, so convert
    radius_left = size_left / size_panel
    radius_right = size_right / size_panel
    gap_relative = 2 * gap / size_panel

    if max(radius_left, radius_right) + gap_relative > 1:
        raise ValueError(
            "Pyllusion error: the disc (size=%.3f) plus its gap (%.3f) does not fit inside the panel "
            "(size_panel=%.3f). Increase size_panel, or leave it as None to have it computed."
            % (max(size_left, size_right), gap, size_panel)
        )

    # --- Which panel gets which colour -------------------------------------------------------------
    if illusion_strength >= 0:
        inner_left, surround_left = rgb1, rgb2
        luminance_inner_left, luminance_surround_left = luminance_1, luminance_2
    else:
        inner_left, surround_left = rgb2, rgb1
        luminance_inner_left, luminance_surround_left = luminance_2, luminance_1
    inner_right, surround_right = surround_left, inner_left
    luminance_inner_right, luminance_surround_right = luminance_surround_left, luminance_inner_left

    # --- Predicted mean luminance of each panel ----------------------------------------------------
    # Analytic, so the brightness confound can be read off without rendering anything.
    def _panel_luminance(radius_panel, luminance_inner, luminance_surround):
        area_disc = _disc_area(radius_panel) / 4
        area_surround = 1 - _disc_area(radius_panel + gap_relative) / 4
        area_gap = 1 - area_disc - area_surround
        return (
            area_disc * (density_inner * luminance_inner + (1 - density_inner) * luminance_background)
            + area_surround * (density * luminance_surround + (1 - density) * luminance_background)
            + area_gap * luminance_background
        )

    panel_left = _panel_luminance(radius_left, luminance_inner_left, luminance_surround_left)
    panel_right = _panel_luminance(radius_right, luminance_inner_right, luminance_surround_right)

    return {
        # Objective difference (what the observer judges)
        "Difference": difference,
        "Size_Left": size_left,
        "Size_Right": size_right,
        # Illusion
        "Illusion": "Chromostereopsis",
        "Illusion_Strength": illusion_strength,
        # Deliberately not Congruent/Incongruent: that needs the direction of the size bias, which is
        # still a hypothesis (see the notes in Chromostereopsis.py).
        "Illusion_Type": "Undetermined",
        # Colours
        "Color_Inner_Left": inner_left,
        "Color_Surround_Left": surround_left,
        "Color_Inner_Right": inner_right,
        "Color_Surround_Right": surround_right,
        "Color_Background": rgb_background,
        "Equiluminant": equiluminant,
        # Luminance and contrast
        "Luminance_Color1": luminance_1,
        "Luminance_Color2": luminance_2,
        "Luminance_Background": luminance_background,
        "Luminance_Ratio": luminance_1 / luminance_2 if luminance_2 > 0 else np.inf,
        "Contrast_Color1": _contrast(luminance_1),
        "Contrast_Color2": _contrast(luminance_2),
        # Mean luminance of each panel, and the imbalance between them
        "Luminance_Panel_Left": panel_left,
        "Luminance_Panel_Right": panel_right,
        "Luminance_Panel_Ratio": panel_left / panel_right if panel_right > 0 else np.inf,
        # Geometry, in grid units
        "Size": size,
        "Size_Panel": size_panel,
        "Gap": gap,
        "Distance": distance,
        "Position_Left": position_left,
        "Position_Right": position_right,
        "Area_Matched": area_matched,
        "Area_Disc_Left": _disc_area(radius_left) / 4,
        "Area_Surround_Left": 1 - _disc_area(radius_left + gap_relative) / 4,
        # Geometry, in units of half the panel side (used for the area computations above)
        "Radius_Left": radius_left,
        "Radius_Right": radius_right,
        "Gap_Relative": gap_relative,
        # Dither
        "Density": density,
        "Density_Inner": density_inner,
        "Dither_Size": dither_size,
        "Dither_Cells_Across": size_panel_px / dither_size if dither_size else np.nan,
        "Dither_Shared": dither_shared,
        "Seed": seed,
    }
