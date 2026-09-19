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


Open questions for the Pyllusion API
------------------------------------
Every Pyllusion illusion exposes ``difference`` (the objective, physical difference) and
``illusion_strength`` (the contextual manipulation that biases perception of it). Chromostereopsis does
not map onto that cleanly, because the perceived attribute is *depth*, and a flat PNG has no objective
depth. Candidate resolutions, to discuss:

1. ``illusion_strength`` = the chromatic manipulation. Signed, so that positive = the red-forward
   configuration and negative = the reversing configuration (e.g. swapped hues, or a light background).
   Magnitude could be driven by hue separation, by saturation, or by the red-blue luminance ratio -
   these need to be teased apart rather than bundled, or the parameter is uninterpretable.
2. ``difference`` = an objective *pictorial* depth cue placed in opposition to the colour cue, so the
   observer's task ("which patch is in front?") has a ground truth. Options:

   - occlusion / overlap: which patch actually overlaps the other (clean, binary-ish, easy to draw);
   - relative size, or a size gradient;
   - blur, as a defocus cue.

   Occlusion looks like the best first candidate: it is unambiguous, continuously parameterisable via
   overlap amount, and it is the cue chromostereopsis has to fight against.
3. Alternatively ``difference`` = objective luminance difference between the two patches - but luminance
   is itself a driver of the illusion, so this confounds the two parameters. Probably a dead end, worth
   noting so we do not revisit it.

Further decisions:

- Should the class offer an ``equiluminant=True`` mode? We already have ``analyze_luminance()`` in
  ``pyllusion.utilities``, so matching sRGB relative luminance across the two colours is cheap. Real
  equiluminance is observer-specific, so this would be an approximation and must be documented as one.
- Which geometry: bars/gratings (closest to the literature), two patches side by side (closest to the
  rest of Pyllusion), or a figure/ground shape? Bars are what the effect sizes above were measured with.
- Parameters to expose for edges: sharp vs dithered transition, outline colour and thickness.
- ``get_parameters()`` should probably record background luminance and the two colours' luminances, since
  the stimulus is not reproducible across displays without them.
- The docstring for the eventual class must warn that (a) the effect is binocular and will not appear in
  screenshots or single-eye viewing, and (b) strength is display- and observer-dependent, so it is not a
  calibrated depth manipulation the way the size illusions are calibrated size manipulations.


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
