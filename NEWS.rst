News
=====

- Add `target_only` where applicable to not draw the "distractor" context.
- Zöllner: The `illusion_strength` has now an opposite effect (fix based on observed data). This behavior is the same as the original one, which got reversed in 1.1.0.
- RodFrame: The `illusion_strength` has now an opposite effect (fix based on observed data). `difference` also got inversed.
- Ebbinghaus: The `difference` has now to be specified in squared values, to maintain linear relationship with actual performance.
- Delboeuf: The `difference` has now to be specified in squared values, to maintain linear relationship with actual performance.
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