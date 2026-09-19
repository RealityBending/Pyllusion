"""
Chromostereopsis - research notes (DRAFT, not implemented yet).

This module is currently a placeholder holding the literature summary that we will use to design the
``Chromostereopsis`` class. Nothing is exported yet: the open questions at the bottom need to be
settled before an API can be written.


Definition
----------
Chromostereopsis ("colour stereo-depth") is the illusion that, on a *flat* image, some colours appear
nearer than others. The canonical case is saturated red and blue on a black field: most observers see
red in front and blue behind (*positive* chromostereopsis). A minority see the reverse (*negative*
chromostereopsis) and roughly 10-20% see no depth at all.

It is a *binocular* illusion: covering one eye largely abolishes it. This is the single most important
constraint for us, because it means the effect cannot be guaranteed by the generated image alone - it
also depends on the observer's optics and on the display. Goethe (1810) first described blue as
"receding" and red/yellow as "advancing"; Einthoven (1885) gave the first optical account.


Mechanisms
----------
Two families of cues combine, and they can either add up or cancel out - which is why the illusion
reverses or vanishes under some conditions.

1. Optical / binocular (the "true" chromostereoptic cue)::

       chromatic aberration (LCA + TCA)  ->  red focuses behind the retina,
                                             blue focuses in front
       fovea sits ~5 deg temporal to the optical axis
       Stiles-Crawford effect + pupil position shifts the effective pupil centre
                                          |
                                          v
       red and blue images land on non-corresponding retinal points, with
       opposite sign in the two eyes  ->  binocular disparity  ->  perceived depth

2. Perceptual / monocular::

       luminance difference  ->  brighter = nearer (aerial perspective)
       colour contrast, borders, surround, other pictorial depth cues

On a typical display, red is emitted much brighter than blue, so part of the classic "red in front"
report is simply the brightness cue. Thompson, May & Stone (1993) showed that equating red and blue
luminance strongly reduces the depth effect in most observers - i.e. much of the everyday illusion is
a *compound* of a chromatic stereo cue and a plain brightness cue.

Accommodation may reinforce it: coloured text on black induces different focusing errors by hue (blue
~+0.6 D of lag vs red ~+0.2 D in a recent study), and observers then judge blue as farther. Corrective
lenses tend to *increase* the illusion.

The neural locus is unsettled. Chromatic disparity clearly reaches cortex (evoked-potential work), but
no specific mechanism has been isolated, and there is no model that quantitatively predicts depth
magnitude for an arbitrary colour pair.


Factors that modulate the effect
--------------------------------
This is the part that matters for a parametric implementation. Direction of effect, as reported:

Colour pairing
    Red/blue is the strongest and best studied pair. Warm hues (red, yellow) advance, cool hues (blue,
    green) recede. Red/green is weaker than red/blue - less chromatic separation to start with.
    Yellow-in-front-of-blue is a reliable variant (Kitaoka).
Luminance
    Dominant modulator. Larger red-minus-blue luminance difference -> stronger effect. Equiluminance
    (ideally set per observer by flicker photometry) minimises it.
Background
    Dark/black background maximises positive chromostereopsis. A white background can *invert* it, so
    blue appears nearer (Verhoeff 1928, confirmed later). Mid-grey washes it out.
Saturation
    Higher saturation -> stronger, though this is partly confounded with luminance contrast.
Spatial structure
    Sharp edges and dithered/pixelated red-blue transitions appear to enhance it relative to smooth
    fills or gradients. Thin contrasting outlines at the border can flip the perceived order.
Size and viewing distance
    Reported as stronger at longer viewing distances (>1 m) and for reasonably large, centrally viewed
    patches. Quantitative data is thin.
Ambient light / pupil size
    In bright light (small pupil) the perceived direction follows the predicted chromatic disparity; in
    dim light (large, eccentrically dilating pupil) direction becomes uncorrelated with it and often
    reverses (Simonet & Campbell 1990). Note this cuts against the intuition that "darker room = stronger".
Competing depth cues
    Shadows, perspective, occlusion, real stereo disparity all override the colour cue. Isolating the
    illusion means stripping other cues out.
Observer
    Large individual differences: refractive error, spectacle wear, lens yellowing with age, ocular
    dominance, stereoblindness.
Display
    Panel technology, subpixel layout, calibration and gamma all change the effective red/blue luminance
    ratio, so the same PNG is not the same stimulus on two screens.


Representative findings
-----------------------
+-------------------------------+------------------------------------+--------------------------------------+
| Study                         | Stimuli                            | Key result                           |
+===============================+====================================+======================================+
| Thompson, May & Stone (1993)  | Red/blue bars, varied luminance    | ~80-92% saw red nearer on black;     |
|                               | and background (N ~ 190-225)       | drops to ~40-64% when red is dimmed  |
|                               |                                    | or the background brightened         |
+-------------------------------+------------------------------------+--------------------------------------+
| Simonet & Campbell (1990)     | Red/blue slits, varied illuminance | Direction matches optical disparity  |
|                               |                                    | at high illuminance only             |
+-------------------------------+------------------------------------+--------------------------------------+
| Verhoeff (1928); replicated   | Red/blue on black vs white         | Order reverses with background;      |
| by later work                 |                                    | border contrast is critical          |
+-------------------------------+------------------------------------+--------------------------------------+
| Faubert (1994, 1995)          | Isoluminant colour on grey         | Depth still perceived; large         |
|                               |                                    | individual differences incl. reversal|
+-------------------------------+------------------------------------+--------------------------------------+
| Coloured-text accommodation   | Red/green/blue/yellow 8pt text on  | Blue: ~0.61 D lag, red: ~0.18 D;     |
| study (2026)                  | black, 50 cm (N = 30)              | ~77% judged blue farthest            |
+-------------------------------+------------------------------------+--------------------------------------+


Candidate design (two swapped panels)
-------------------------------------
Two square panels side by side, each a dithered coloured disc inside a dithered coloured surround,
separated by a bare black annulus. The two panels use the *same* two colours with the roles swapped:
one shows a red disc on a blue surround, the other a blue disc on a red surround. Prototyped in
``chromostereopsis_image.py``.

Why this layout is appealing: the two panels are geometrically identical and use the same two colours,
so they differ only in which colour is figure and which is ground. The chromostereoptic prediction is
that the red disc advances and the blue disc recedes, giving opposite depth percepts on the two sides
from a stimulus that is otherwise balanced.

This also gives a way out of the "no objective depth" problem, because it lets us move the judged
attribute from depth to **size**. Decided:

- ``difference`` = the objective size difference between the two discs (left radius relative to right),
  exactly as in Delboeuf and Ebbinghaus. The observer is asked which disc is larger.
- ``illusion_strength`` = deferred. Only its *sign* is wired up for now, setting which panel gets the
  ``color1`` disc; what the magnitude should scale is still open (see below).

The rationale is size constancy: a disc that appears nearer at the same retinal size should appear
*smaller*, so chromostereopsis should bias size judgements in a predictable direction. This is testable
with the machinery Pyllusion already has, and the anecdotal pixel-art reports that red "seems larger"
are at least consistent with a size effect existing. It is a hypothesis, though, not an established
finding - if chromostereopsis turns out not to bias size, the design collapses back to a pure depth
judgement with no ground truth.

Measured on the prototype
-------------------------
Two things the first renders turned up:

1. **The two panels are not luminance-matched by default.** With the default geometry the disc and the
   surround have different areas, and red is about three times more luminous than blue in sRGB. The
   panel with the red *surround* therefore comes out much brighter overall: mean relative luminance
   0.064 vs 0.043, a ~49% difference. Since brightness is itself a depth (and probably size) cue, this
   confounds exactly the comparison we want to make.

   Fix: choose the radius so that disc area equals surround area, which makes each panel contain equal
   amounts of red and blue and so equalises the two panels as wholes. With ``gap=0.08`` that radius is
   ``0.757``, and it brings the two panels to 0.053 vs 0.051 (residual is dither sampling noise).
   Note this only works at ``difference=0``; once the radii differ the areas cannot both be matched, so
   there will be a small residual luminance difference that scales with ``difference``. Worth
   quantifying and reporting in ``get_parameters()``.

2. **The dither pattern differed between panels.** Now shared by default (``dither_shared``), so colour
   assignment is the only difference between the two panels.


Exposed parameters
------------------
``chromostereopsis_parameters.py`` exposes the factors from the literature review as knobs, so their
effect on the illusion can be measured rather than guessed. Grouped by the factor they target:

=====================  ==========================================================================
Patterning             ``density``, ``density_inner``, ``dither_size``, ``dither_shared``
Luminance              ``luminance1``, ``luminance2``, ``equiluminant``
Contrast               ``background`` (raising it lowers both colours' contrast at once)
Colour pairing         ``color1``, ``color2``
Geometry               ``size``, ``size_panel``, ``gap``, ``distance``
Reproducibility        ``seed``
=====================  ==========================================================================

Two notes on measuring luminance and contrast with these:

- ``luminance1``/``luminance2`` scale in *linear light*, not in 8-bit code values, so ``0.5`` really is
  half the luminance (it maps red 255 -> 188, not -> 128). ``density`` is a second, independent
  luminance knob: it scales a region's mean luminance without touching its pixel colour, which makes it
  a useful way to dissociate "how bright the region is" from "how bright the colour is".
- **On a black background, Michelson contrast is 1 for every colour**, so ``Contrast_Color*`` carries no
  information there and a non-black ``background`` is needed to manipulate contrast at all. Useful
  landmark: mid-grey ``#808080`` has relative luminance 0.216, almost exactly that of pure red (0.213),
  so a mid-grey background is very nearly isoluminant with red while still being far from blue.

Geometry matched to Delboeuf
----------------------------
Sizes and distances use Pyllusion's grid units (sizes a proportion of the image height, positions -1 to
1 across the width), and the defaults are set to match Delboeuf so the two illusions can sit in the same
battery: ``size=0.25`` and ``distance=1`` give 75 px discs with centres 400 px apart on the default
800x600 canvas, identical to ``pyllusion.Delboeuf()``. The disc is the analogue of Delboeuf's inner
circle (the judged target) and the square panel of its outer circle (the context).

``size_panel`` is left at ``None`` by default, which sets it to the area-matched value - so the
brightness confound is off by default rather than something you have to remember to switch on. The gap
("the black outline") is ``gap``, in the same grid units. Raising it grows the area-matched panel with
it, since the surround has to grow to keep its area equal to the disc's.

Two consequences of matching Delboeuf worth keeping in mind:

- **The stimulus is small.** Delboeuf's geometry puts the whole panel at ~102 px on the default canvas.
  The literature reports chromostereopsis as stronger for larger stimuli and longer viewing distances,
  so the matched defaults may well sit at the weak end of the effect. Raising ``size`` (or rendering
  larger) is the easy fix, at the cost of no longer matching Delboeuf exactly - a trade-off to make
  deliberately rather than by accident.
- **The dither has little room.** ``dither_size`` is in pixels and does not scale with the image, so at
  ~102 px panels the default of 2 px gives ~50 cells across. Rendering larger without raising it changes
  the appearance; hold ``Dither_Cells_Across`` constant instead.

The parameters dict reports the derived quantities too - each colour's relative luminance, their ratio,
each colour's contrast against the background, the disc/surround areas, and the predicted mean luminance
of each panel. The panel luminances are computed analytically from areas and densities, and agree with
rendered stimuli to within dither sampling noise (0.0518/0.0795 predicted vs 0.0527/0.0798 measured at
the defaults), so the brightness confound can be read off a condition without rendering it.

Remaining open questions
------------------------
- **What does the magnitude of ``illusion_strength`` vary?** Deferred by agreement. Candidates:
  saturation of the colour pair, hue separation, or the red:blue luminance ratio. The luminance ratio is
  the best-supported choice, since it is the dominant modulator in the literature and is directly
  measurable - but it partly conflates the chromatic cue with the brightness cue, which is arguably the
  honest thing to do given that the everyday illusion is that compound. Note that whichever is chosen,
  it will overlap with the parameters already exposed above, so ``illusion_strength`` is likely to end
  up as a convenience wrapper over some of them rather than an independent knob.
- **Does chromostereopsis actually bias size?** The whole ``difference`` mapping rests on this. Needs
  checking against the literature, and it may simply need piloting.
- Geometry: the effect sizes in the table above were measured with bars, not discs. Should we also
  offer a bar/grating variant to stay comparable with the literature?
- No ``Chromostereopsis`` class yet: the natural time to add one (with ``to_image()`` and
  ``get_parameters()``) is once ``illusion_strength`` is settled.
- The eventual class docstring must warn that (a) the effect is binocular and will not appear in
  screenshots or single-eye viewing, and (b) strength is display- and observer-dependent, so this is not
  a calibrated depth manipulation the way the size illusions are calibrated size manipulations.


Sources to verify
-----------------
The summary above is compiled from a literature review that has not yet been checked against the
primary sources. Before any of this goes into user-facing documentation:

- The 2026 coloured-text accommodation study is attributed to two different first authors in the source
  material (Ramasubramanian et al. / Suganthan et al.) for the same numbers - find the actual citation.
- Thompson, May & Stone (1993) is quoted with both "92%" and "80-92%" for the red-nearer rate; check
  which condition each refers to.
- The background-reversal replication is cited as "Winn et al. (1998), Vision Research" - confirm.
- The claim that dithered edges enhance the effect comes from an artist's pixel-art write-up, not a
  controlled study. Treat as a hypothesis to test, not as a finding.
- Older references (Goethe 1810, Donders 1864, Bruecke 1868, Einthoven 1885, Verhoeff 1928,
  Sundet 1978, Simonet & Campbell 1990, Faubert 1994/1995, Kitaoka 2006/2016) are given without full
  bibliographic details.
"""
