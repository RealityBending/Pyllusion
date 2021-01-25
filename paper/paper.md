---
title: "A Parametric Framework to Generate Visual Illusions using Python"
authors:
- affiliation: 1
  name: Dominique Makowski
  orcid: 0000-0001-5375-9967
- affiliation: 1
  name: Tam Pham
  orcid: 0000-0002-6392-6703
- affiliation: 1
  name: Zen J. Lau
  orcid: 0000-0003-4429-4082
- affiliation: 2, 3
  name: S.H. Annabel Chen
  orcid: 0000-0002-1540-5516

date: "04 Jan 2021"
output: pdf_document
bibliography: bibliography.bib
csl: apa.csl

tags:
- Pyllusion
- Visual Illusions
- Optical Illusions
- Schizophrenia
- Python
- PsychoPy
affiliations:
- index: 1
  name: School of Social Sciences, Nanyang Technological University, Singapore
- index: 2
  name: Centre for Research and Development in Learning, Nanyang Technological University, Singapore
- index: 3
  name: Lee Kong Chian School of Medicine, Nanyang Technological University, Singapore
---


[? - Perception](https://journals.sagepub.com/home/pec)
[2.45 - Journal of Experimental Psychology: Human Perception and Performance](https://www.apa.org/pubs/journals/xhp/)
[1.893 - Attention, Perception, & Psychophysics](https://www.springer.com/journal/13414)
[? - Art \& Perception](https://brill.com/view/journals/artp/artp-overview.xml)
[? - Journal of Vision](https://jov.arvojournals.org/)
[1.102 - Visual Cognition](https://www.tandfonline.com/toc/pvis20/current)
[2.61 - Vision Research](https://www.sciencedirect.com/journal/vision-research)
[3 - Visual Neuroscience](https://www.cambridge.org/core/journals/visual-neuroscience)

# Abstract

Visual illusions are fascinating phenomena that have been used and studied by artists and scientists for centuries, leading to important discoveries about the neurocognitive underpinnings of perception and consciousness. Surprisingly, despite their strong historical importance as psychological stimuli, there is no dedicated software, nor consistent approach, to generate illusions in a systemic fashion. Instead, scientists have to craft them by hand in an idiosyncratic fashion, or use pre-made images not tailored for the specific needs of their studies. This, in turns, hinders the reproducibility of illusion-based research and narrows its possibilities and applications. With the aim of addressing that gap, ***Pyllusion*** offers a framework to manipulate and generate illusions in a systematic way, compatible with different output formats such as image files (.png, .jpg, .tiff, etc.) or *PsychoPy* [@peirce2007psychopy] stimuli.


# Introduction


Visual illusions have been observed for hundreds of years [@LuckieshVisualIllusions1965], many of which were described in print by @Helmholtz in 1856 [@robinson1972psychology]. In general terms, a visual illusion can be thought of as the inaccurate perception of a visual stimulus or a given attribute, be it geometrical (size, shape, or angle), or another property such as colour [@muller1896lehre, @howe2005muller, @delboeuf1893nouvelle, @ebbinghaus1902grundzuge, @roberts2005roles, @adelson200024]. Often an illusory perception resists 'correction' in perception even after an observer has been made aware of the misperception. Novel examples of illusions are still observed and have even cropped up on social media platforms, a famous example being 'The Dress Illusion' (see **Fig. 1**) as discussed by Schlaffke et al. (2015). See @Ninio, @Luckiesh, and @Robinson for extensive collections of visual illusions.

- **FIX CITATIONS HERE**

![The internet-famous 'Dress illusion' image (on the left), which some people perceive as white and yellow *vs.* black and blue. It is thought to illustrate how perceptual priors (i.e., expectations regarding the lighting conditions) can bias our conscious representation of an object (see visual explanation - from Wikipedia - on the right).](figure1.png)

Entertainment value aside, illusions can serve a more practical utility. Visual illusions have helped scientists understand the architecture of the eye and its relationship with processes and structures involved further up stream in the brain, the dynamic interaction of these processes, and visual coding in the brain in general [@carbon2014understanding, @forte2005inter, @clifford2002perceptual]. Illusions such as the blind-spot or those associated with colour perception, orientation perception, and motion perception, have all been informative of neuronal activity/processes both at the level of the eye and the brain via the measurement of associated illusions  [@durgin1995filling, @webster1996human, @witkin1948studies, @mackay1957moving, @Holland1965, @curran2009hierarchy]. Indeed, visual illusions also have the potential as clinical tools, such as being markers of, or being used to investigate typical integration processes through the lens of, schizophrenia [@clifford2014tilt, @thakkar2020stronger, @palmer2018perceptual] and have been used to demonstrate vestibular and contextual influences on visual perception [@corbett2006observer, @chen2015contextual, @roberts2005roles]. Visual illusions, and perceptual illusions more generally, are a powerful tool in human perception and brain research, which in turn can inform artificial cognitive systems design considerations [@carbon2014understanding, @boyce2020optimality].


- **Add review on psychopathology**


Despite its relevance to psychology and neuroscience, the field of illusion research lacks a dedicated software to generate and report the stimuli, in order for them to be reproduced and re-used by other researchers and studies. This is particularly problematic in the context of the replicability and reproducibility issues recently outlined in psychological science [@topalidou2015long; @open2015estimating; @milkowski2018replicability; @maizey2019barriers]. Our software, **Pyllusion**, aims at addressing this gap by proposing and implementing a parametric framework for illusions generation.


# A Parametric Framework for Illusion Research


The core idea of the "parametric" approach proposed here and implemented in **Pyllusion** is to dissociate the parameters of an illusion from its rendered output. For instance, the Ponzo illusion (see **Fig. 2**) can be described in terms of properties of the "distractor" lines (which create the illusion), such as the angle (related to the illusion strength), the color, width, etc. and properties of the "target" lines (which are affected by the illusion), such as the size of the smallest line, the objective difference of the ratio of their length, or their color, width, etc. This set of parameters can then be rendered in different formats with further format-specific characteristics (in the case of images, the image size, ratio, resolution, compression, etc.).

![The "parametric framework" for illusions originally implemented in **Pyllusion** aims at dissociating the *parametric* representation of an illusion (on the left) from its *rendered* representation, in this case as an image (on the right).](figure2.png)

This essentially allows researchers to describe, manipulate, process and share their stimuli in a concise yet consistent way. For instance, researchers could report a *"linear modulation of the illusion strength between -15 and 15, resulting in a reduced reaction time of..."*, providing details about the remaining parameters, as well as the Python code used to fully reproduce their stimuli.

Moreover, this parametric approach is scalable and appears to work well with different kinds of illusions, as demonstrated in the software. Indeed, many visual illusions (especially the classical one) appears to have relatively similar parameters (such as a feature - like the angle or the size of some shapes - related to the strength of the illusion, or the color of the "target" objects), which in turn allows for a consistent programming interface (API).

Interestingly, in most of the visual illusions, the strength of the illusion can be dissociated from the actual "difference" (which is impacted by the illusion). For instance, in the Müller-Lyer illusion (see **FIG ???**), the difference between the two horizontal segments can be modulated orthogonally from the angle of the "distractors" arrows. Allowing researchers to easily manipulate these parameters opens the door for potentially interesting paradigms and experiments. In the following section, we will describe with concrete examples how we operationalized such a parametric approach in the **Pyllusion** software.



<!-- parametric representation -->
<!-- example, delboeuf parameters, show output of dictionary parameters. pass dict values into another function to generate either image or psychopy object -->


# Pyllusion


It is not the first time that Python, illusions and cognitive science are brought together. In his book, *"Programming visual illusions for everyone"*, @bertamini2017programming indeed describes how to use *PsychoPy* to generate famous illusions. That said, although being a fantastic tool and resource for researchers and anybody interested in illusions, it is rather presented as an fun introduction to programming and to Python, rather than a dedicated software for illusions *per se*.

**Pyllusion** is an open-source package to programmatically generate illusions written in Python 3 [@python3], which means that its users benefit from an large number of learning resources and a vibrant community. However, although being a programming-based tool, users not familiar with Python or other languages can easily use it as well, as it requires minimal programming skills (one can essentially copy the few necessary lines from the documentation and tweak the explicitly-named parameters). This makes it a very flexible tool; advanced users can incorporate **Pyllusion** in their scripts or experiments (for instance, to generate illusions "on the fly" based on the input of the user), whereas novice users can simply copy the minimal code to pre-generate and save the illusions as images.


The source code is available under the MIT license on GitHub (*https://github.com/RealityBending/Pyllusion/*). Its documentation (*https://realitybending.github.io/Pyllusion/*) is automatically built and rendered from the code and includes guides for installation, a description of the package's functions, with examples of use. Finally, the issue tracker on GitHub offers a convenient and public forum that allows users to report bugs, get help and gain insight into the development of the package. Additionally, the repository leverages a comprehensive test suite (using *pytest*) and continuous integration (using Travis-CI and GitHub actions) to ensure software stability and quality. The test coverage and build status can transparently be tracked via the GitHub repository. Thanks to its collaborative and open development, *Pyllusion* can continuously evolve, adapt, and integrate new functionalities to meet the needs of the community.

<!-- Installation -->
**Pyllusion** is available on PyPI, the main repository of software for Python and can thus be installed by running the command `pip install Pyllusion`. Once the software is installed, it must be loaded in Python scripts with `import pyllusion`.




## Step 1: Parameters



Currently, *Pyllusion* encompasses several different illusions, including the Delboeuf illusion, Ebbinghaus illusion, Müller-Lyer illusion, Ponzo illusion, Vertical–horizontal illusion, Zöllner illusion, Rod and Frame illusion and Poggendorff illusion.

Note the two main parameters, *illusion_strength*, and *difference*, have abstract names despite relative meaning depending on the illusion. For instance, in the Ponzo illusion, *illusion_strength* currently refers to the angle of the non-horizontal lines, whereas the same argument modulates the area of the outer circles in the Delboeuf illusion. This decision of unifying the "illusion strength" parameter under the same name was motivated by the aim of having a consistent naming scheme for the API. This means that users can experiment with new illusions by modulating the illusion strength, without the need of learning what is the actual physical parameter (e.g., "angle of the distractor lines") driving the illusion.


## Step 2: Rendering

<!-- pass parameters into an output generator (as images or psychopy objects, psychopy being the most common experimentation software in psychology) -->
<!-- two engines available in pyllusion as of now -->

*Pyllusion* encompasses a function-oriented philosophy based on the *psychopy* package. Each function is illusion-specific and hence, uniform function names (in the form `illusiontype_functiongoal()`) are used in the process of creating the illusion.
While the functions can be incorporated within a PsychoPy builder, it can also be used without a GUI - the following example demonstrates the latter in generating a Delboeuf illusion.
Parameters specifying the illusion difficulty and strength are generated using `*_parameters()` before executing the display via `*_psychopy()`.


### Images

```python
# Load package
import pyllusion as ill

# Create parameters
parameters = ill.delboeuf_parameters(difficulty=2, illusion_strength=1)

# Generate image from parameters
ill.delboeuf_image(parameters)
```

![Delboeuf Illusion generated by Pyllusion using `difficulty=2` and `illusion_strength=1` in `delboeuf_parameters()`](figures/example_delboeuf.PNG)


### PsychoPy

It is designed for specific integration within the *psychopy* [@peirce2007psychopy] package for PsychoPy experiment creation.


```python
# Load packages
import pyllusion as ill
from psychopy import visual, event

# Create parameters
parameters = ill.delboeuf_parameters(difficulty=2, illusion_strength=1)

# Initiate Window
window = visual.Window(size=[800, 600], fullscr=False,
                       screen=0, winType='pyglet', monitor='testMonitor',
                       allowGUI=False, color="white",
                       blendMode='avg', units='pix')

# Generate psychopy object from parameters
ill.delboeuf_psychopy(window=window, parameters=parameters)

# Refresh and close window
window.flip()
event.waitKeys()  # Press any key to close
window.close()
```


# Future Plans and Developments

Being an open-source software, **Pyllusion** will continue to grow and evolve based on the community's input. While the direction and state of the package in the long term can be hard to predict, several short term goals can be mentioned.
<!-- Add more illusions -->
While illusions are of number (there are even machine learning algorithms generating visual illusions [REF]), a subset of them is commonly used (for historical reasons mainly, as well as for their relative simplicity). This set of classical, well-described, illusions, such as the Delboeuf, the Ponzo [ETC], is the primary focus of ***Pyllusion***. That said, due to the open and collaborative nature of the software, new illusions can always be added depending on the needs of the community. 
Movements based (that could be saved as GIFs).

<!-- Add more illusions -->
Add support to more output engines eg., neuropsydia, opensesame

<!-- Experiments & validation -->
Validation to see how the illusion strength values affect the perception. Standardize the values.





# Acknowledgments

We would like to thank Prof. Mahamaya for her insights regarding illusions.

# References




