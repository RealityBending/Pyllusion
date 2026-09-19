News
=====

1.5
---------

**Fixes**

- ``Delboeuf`` and ``Ebbinghaus``: fixed ``Size_Inner_Difference`` in ``get_parameters()``. An operator
  precedence slip (``np.pi * a**2 / np.pi * b**2``, which evaluates as ``(pi * a**2 / pi) * b**2``) made
  it return the product of the two squared radii instead of a difference of areas - it reported
  0.000244140625 for two circles of *identical* size. It is now the signed difference between the areas
  of the two inner circles, positive when the left circle is larger, as its docstring always described.
  Both illusions were affected, since ``Ebbinghaus`` reuses the same helper. **Any analysis that used
  this value will need re-running.**
- Corrected the name of that entry in the ``Delboeuf`` and ``Ebbinghaus`` docstrings, where it was
  listed as ``Sine_Inner_Difference``.

**Misc**

- Repaired the "Render README" workflow, which could not run: it installed reticulate from GitHub
  (rate limited without a token), never installed Pyllusion itself although ``README.Rmd`` imports it,
  and relied on a hard-coded local path to a Python distribution.

1.4
---------

**Compatibility**

- Fixed ``image_blob()``, ``image_blobs()`` and ``Pareidolia`` which were broken by the removal of
  ``np.int`` (NumPy >= 1.24) and of ``scipy.signal.gaussian`` (SciPy >= 1.13).
- Fixed ``image_text()`` (and ``Autostereogram``) which crashed with recent versions of Pillow when
  using the default ``size="auto"``.
- ``image_noise()`` no longer passes the ``mode`` argument to ``PIL.Image.fromarray()``
  (deprecated, removed in Pillow 13).
- ``images_to_gif()`` now passes the frame duration to ``imageio`` in milliseconds, as expected by
  recent versions (GIFs were previously played back at the wrong speed, and the deprecated ``fps``
  argument is no longer used).

**Fixes**

- ``Autostereogram(invert=True)`` used to fail with an ``AttributeError``.
- ``Autostereogram`` no longer raises an ``IndexError`` for small images / narrow pattern strips.
- ``Pareidolia.draw()`` no longer overwrites ``self.sd``, so calling it several times now gives
  consistent results.

**Misc**

- Requires Python >= 3.9, Pillow >= 10.1 and SciPy >= 1.13.
- Tests are now run against Python 3.10-3.13 and cover the illusions/functions above.

1.3
---------

- Added `image_scramble()` to shuffle / randomize pixels of an image.
- Ebbinghaus: The location of the distractor circles is now mirrored between the left and the right side, to prevent edge cases where the image is cut one side but not the other.
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