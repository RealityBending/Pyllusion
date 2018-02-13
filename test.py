# -*- coding: utf-8 -*-
"""
Pyllusion module testing suite.
"""

import neuropsydia as n
import numpy as np
import pandas as pd
import pyllusion as il
import PsiStaircase



n.start()
# =============================================================================
# Delboeuf
# =============================================================================
#n.instructions("Delboeuf")

#for difficulty in [0.1, 0.5, 0.8, -0.8, -0.5]:
#    for illusion in [0, 0.5, -0.5]:
#
#        n.newpage()
#        parameters = il.delboeuf_compute(difficulty=difficulty, illusion=illusion)
#        il.delboeuf_display(parameters)
#        n.write("Difficulty: " + str(round(parameters["Difficulty"], 2)), y=9)
#        n.write("Illusion: " + str(round(parameters["Illusion"], 2)), y=8)
#        n.write("Type: " + str(parameters["Illusion_Type"]), y=7)
#        n.refresh()
#        n.response()


#for i in range(10):
#    location_smaller = np.random.choice(["right", "left"])
#    distance = round(np.random.uniform(1, 5), 1)
#    inner_size_smaller = round(np.random.uniform(1, 2.5), 1)
#    real_difference = round(np.random.uniform(0, 1), 1)
#    illusion_strength = round(np.random.uniform(-1, 1), 1)
#
#    parameters = il.delboeuf_compute(distance=5,
#                                  distance_auto=True,
#                                  inner_size_smaller=inner_size_smaller,
#                                  location_smaller=location_smaller,
#                                  real_difference_ratio=real_difference,
#                                  illusion_strength=illusion_strength)
#    n.newpage()
#    n.write("Smaller: " + parameters["Real_Location_Smaller"], y=8)
#    n.write("Reality: " + str(round(parameters["Real_Difference_Inner_Ratio"], 1)), y=7)
#    n.write("Illusion: " + str(round(parameters["Illusion_Strength"], 1)), y=6)
#
#    il.delboeuf_display(parameters)
#
#    n.refresh()
#    resp, RT = n.response()



# =============================================================================
# Ponzo
# =============================================================================
#n.instructions("Ponzo")
#
#for difficulty in [25, -25]:
#    for illusion in [20, -20]:
#
#        n.newpage()
#        parameters = il.ponzo_compute(difficulty=difficulty, illusion=illusion)
#        il.ponzo_display(parameters)
#        n.write("Difficulty: " + str(round(parameters["Difficulty"], 2)), y=9)
#        n.write("Illusion: " + str(round(parameters["Illusion"], 2)), y=8)
#        n.write("Type: " + str(parameters["Illusion_Type"]), y=7)
#        n.refresh()
#        n.response()



# =============================================================================
# RodFrame
# =============================================================================
#n.instructions("Rod and Frame")
#
#for difficulty in [15, -15]:
#    for illusion in [30, -30]:
#
#        n.newpage()
#        parameters = il.rodframe_compute(difficulty=difficulty, illusion=illusion)
#        il.rodframe_display(parameters)
#        n.write("Difficulty: " + str(round(parameters["Difficulty"], 2)), y=9)
#        n.write("Illusion: " + str(round(parameters["Illusion"], 2)), y=8)
#        n.write("Type: " + str(parameters["Illusion_Type"]), y=7)
#        n.refresh()
#        n.response()



# =============================================================================
# Zollner
# =============================================================================
#for difficulty in [5, -5]:
#    for illusion in [20, -20]:
#
#        n.newpage()
#        parameters = il.zollner_compute(difficulty=difficulty, illusion=illusion)
#        il.zollner_display(parameters)
#        n.write("Difficulty: " + str(round(parameters["Difficulty"], 2)), y=9)
#        n.write("Illusion: " + str(round(parameters["Illusion"], 2)), y=8)
#        n.write("Type: " + str(parameters["Illusion_Type"]), y=7)
#        n.refresh()
#        n.response()

#

# =============================================================================
# TFM
# =============================================================================
#n.instructions("Transparency From Motion")
#for i in np.arange(0, 360, 60):
#    parameters = il.TFM(angle=i)
#    response = il.TFM_response(parameters)

# =============================================================================
# Pattern Detection in Motion
# =============================================================================
n_trials = 30

staircase = PsiStaircase.Psi(stimRange=np.arange(0, 75.5, 0.5), Pfunction='cGauss', nTrials=n_trials, threshold=None, thresholdPrior=('uniform', None), slope=None, slopePrior=('uniform', None), guessRate=None, guessPrior=('uniform', None), lapseRate=None, lapsePrior=('uniform', None), marginalize=True, thread=True)

n.instructions("Pattern Detection in Motion")

for trial in range(n_trials):
    signal = None
    angle = np.random.uniform(0, 360)
    while staircase.xCurrent == None:
        pass # hang in this loop until the psi calculation has finished
    signal = staircase.xCurrent

    parameters = il.PDM(signal=signal, angle=angle)
    response = il.PDM_response(parameters)
    if response == angle:
        correct = 1
    else:
        correct = 0
    print(correct)
    print(signal)
    print("---")

    staircase.addData(correct)

print("====")
print("Slope: %.02f +- %.02f" %(staircase.eSlope, staircase.stdSlope))
print("Treshold: %.02f +- %.02f" %(staircase.eThreshold, staircase.stdThreshold))

#
#staircase.eSlope
#staircase.stdSlope
#staircase.eThreshold
#staircase.stdThreshold


#pd.Series(staircase.threshold, staircase.pThreshold).plot()
#pd.Series(staircase.slope, staircase.pSlope).plot()



#staircase.plot()
# =============================================================================
# Pareidolia
# =============================================================================
#img1 = il.create_image_blobs(figsize=(10, 10), n=2500, blobsize=1, blur_radius=5, background="black")
#img2 = il.create_image_blobs(figsize=(10, 10), n=150, blobsize=2.5, blur_radius=15, background="black")
#img3 = il.create_image_blobs(figsize=(10, 10), n=10, blobsize=5, blur_radius=15, background="black")
#
#img = il.merge_images(il.merge_images(img3, img2), img1)
#img.show()


n.close()