News
=====

- Delboeuf: added `distractor_fill` argument to modulate the color of the outer circles.
- Delboeuf: `illusion_strength=0` now generates the outline circle of the *same size* as the target circles (instead of being slightly bigger). This was done to fix an unintented effect of the prior behavior (see illusion game validation study and https://github.com/RealityBending/Pyllusion/issues/17).
- Add `target_only` where applicable to not draw the "distractor" context.
- Zöllner: The `illusion_strength` has now an opposite effect (fix based on observed data). This behavior is the same as the original one, which got reversed in 1.1.0.
- RodFrame: The `difference` effect got inversed.
- Zollner: target red lines are now in front of the distractor lines.

1.1.0
---------

**Breaking**

- We realised that in several illusions, the effect of illusion strength was coded in the opposite way: positive values were congruent with the real difference. We reversed the direction of the illusion strength for:
  - Zöllner
  - Poggendorff (fixed the logic)
  - White
  - Contrast

If you want to get back to previous behavior, swap negative values for positive.

1.0.0
-------------------

- Initial release