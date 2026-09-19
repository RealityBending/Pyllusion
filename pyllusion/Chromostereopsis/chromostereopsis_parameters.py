"""
PROTOTYPE - parameters for the two-panel chromostereopsis stimulus. Not part of the public API yet.
"""
import numpy as np
import scipy.optimize

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


def _radius_area_matched(gap):
    """Radius at which the disc and the surround have equal area, for a given gap width.

    Matching the two areas means each panel holds equal amounts of the two colours, which is what makes
    the two panels of a stimulus equally luminous overall. Exact only when difference=0.
    """
    return float(scipy.optimize.brentq(lambda r: _disc_area(r) - (4 - _disc_area(r + gap)), 0.01, 1.4))


# ---------------------------------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------------------------------
def _chromostereopsis_parameters(
    difference=0,
    illusion_strength=0,
    color1="red",
    color2="blue",
    luminance1=1.0,
    luminance2=1.0,
    equiluminant=False,
    background="black",
    radius=0.58,
    gap=0.08,
    area_matched=False,
    density=0.5,
    density_inner=None,
    dither_size=10,
    dither_shared=True,
    seed=None,
):
    """Compute the parameters of the two-panel chromostereopsis stimulus.

    Parameters
    ----------
    difference : float
        The objective size difference between the two discs: the radius of the left disc relative to
        the right (e.g. ``difference=0.1`` makes the left disc 10% larger, ``-0.1`` 10% smaller).
        This is the attribute the observer is asked to judge.
    illusion_strength : float
        Provisional. Only its *sign* is used, and it sets which panel receives the disc drawn in
        ``color1`` (>= 0 puts it on the left). What the magnitude should scale is still open - see the
        notes in ``Chromostereopsis.py`` - so for now any positive value behaves like any other.

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

    Geometry
    --------
    radius : float
        Radius of the discs, as a proportion of half the panel side. Ignored if ``area_matched``.
    gap : float
        Width of the bare annulus between disc and surround, in the same units.
    area_matched : bool
        If True, override ``radius`` with the value that makes disc area equal surround area, so the two
        panels contain equal amounts of both colours and are equally luminous overall. This removes the
        brightness confound between panels, but is exact only at ``difference=0``; the residual is
        reported as ``Luminance_Panel_Ratio``.

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
        look that is anecdotally reported to strengthen the effect.
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

    # --- Geometry ----------------------------------------------------------------------------------
    if area_matched is True:
        radius = _radius_area_matched(gap)

    radius_left = radius * (1 + difference / 2)
    radius_right = radius * (1 - difference / 2)

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
        area_surround = 1 - _disc_area(radius_panel + gap) / 4
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
        "Size_Left": radius_left,
        "Size_Right": radius_right,
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
        # Geometry
        "Radius": radius,
        "Gap": gap,
        "Area_Matched": area_matched,
        "Area_Disc_Left": _disc_area(radius_left) / 4,
        "Area_Surround_Left": 1 - _disc_area(radius_left + gap) / 4,
        # Dither
        "Density": density,
        "Density_Inner": density_inner,
        "Dither_Size": dither_size,
        "Dither_Shared": dither_shared,
        "Seed": seed,
    }
