# -*- coding: utf-8 -*-
"""
Pyllusion module testing suite.
"""

import neuropsydia as n
import numpy as np
import pyllusion as il




n.start()
# =============================================================================
# Delboeuf
# =============================================================================
#n.instructions("Delboeuf")
#
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
#for i in range(10):
#    illusion_strength = round(np.random.uniform(-10, 10), 1)
#    real_difference = round(np.random.uniform(0, 0.5 ), 1)
#
#    n.newpage()
#    parameters = il.ponzo_compute(illusion_strength=illusion_strength, real_difference=real_difference)
#    il.ponzo_display(parameters)
#    n.write("Illusion" + str(illusion_strength), y=9)
#    n.write("Real" + str(real_difference), y=8)
#    n.refresh()
#    n.response()



# =============================================================================
# RodFrame
# =============================================================================
n.instructions("Rod and Frame")

for rod_angle in np.arange(-20, 21, 5):
    for illusion_strength in np.arange(-45, 46, 15):


        n.newpage()
        parameters = il.rodframe_compute(illusion_strength=illusion_strength, rod_angle=rod_angle)
        il.rodframe_display(parameters)
        n.write("Illusion: " + str(round(parameters["Illusion_Strength"], 2)), y=9)
        n.write("Difficulty: " + str(round(parameters["Difficulty"], 2)), y=8)
        n.refresh()
        n.response()



# =============================================================================
# Zollner
# =============================================================================
#n.instructions("Zollner")
#
#for i in range(20):
#    illusion_strength = round(np.random.uniform(-1.5, 1.5), 2)
#    real_angle = round(np.random.uniform(-10, 10), 2)
#
#    n.newpage()
#    parameters = il.zollner_compute(illusion_strength=illusion_strength, real_angle=real_angle)
#    il.zollner_display(parameters)
#    n.write("Illusion: " + str(illusion_strength), y=9)
#    n.write("Real: " + str(real_angle), y=8)
#    n.refresh()
#    n.response()
#
#
#n.close()


# =============================================================================
# Pareidolia
# =============================================================================
#img1 = il.create_image_blobs(figsize=(10, 10), n=2500, blobsize=1, blur_radius=5, background="black")
#img2 = il.create_image_blobs(figsize=(10, 10), n=150, blobsize=2.5, blur_radius=15, background="black")
#img3 = il.create_image_blobs(figsize=(10, 10), n=10, blobsize=5, blur_radius=15, background="black")
#
#img = il.merge_images(il.merge_images(img3, img2), img1)
#img.show()


