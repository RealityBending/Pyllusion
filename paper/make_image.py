import numpy as np
import PIL
import pyllusion as ill

# PONZO FOR FIG 1 PPT
parameters = ill.ponzo_parameters(illusion_strength=20,
                                  difficulty=0,
                                  size_min=0.5)
img = ill.ponzo_image(parameters)
img
img.save("ponzo_for_ppt.png")


# MOSAIC Illusions
img1 = ill.delboeuf_image(width=1280, height=720, illusion_strength=3)
img1 = ill.image_text(image=img1, text="Delboeuf", y=0.9, size=80)
img2 = ill.ebbinghaus_image(width=1280, height=720, illusion_strength=2)
img2 = ill.image_text(image=img2, text="Ebbinghaus", y=0.9, size=80)
img3 = ill.mullerlyer_image(width=1280, height=720, illusion_strength=30)
img3 = ill.image_text(image=img3, text="Müller-Lyer", y=0.88, size=80)
img4 = ill.ponzo_image(width=1280, height=720, illusion_strength=20)
img4 = ill.image_text(image=img4, text="Ponzo", y=0.88, size=80)
img5 = ill.verticalhorizontal_image(width=1280, height=720, illusion_strength=90)
img5 = ill.image_text(image=img5, text="Vertical-Horizontal", y=0.9, size=80)
img6 = ill.zollner_image(width=1280, height=720, illusion_strength=75)
img6 = ill.image_text(image=img6, text="Zöllner", y=0.9, size=80)
img7 = ill.rodframe_image(width=1280, height=720, illusion_strength=11)
img7 = ill.image_text(image=img7, text="Rod and Frame", y=0.9, size=80)
img8 = ill.poggendorff_image(width=1280, height=720, illusion_strength=50)
img8 = ill.image_text(image=img8, text="Poggendorff", y=0.9, size=80)
img9 = ill.contrast_image(width=1280, height=720, illusion_strength=50)
img9 = ill.image_text(image=img9, text="Contrast", y=0.9, size=80, color="white")
img10 = ill.white_image(width=1280, height=720, illusion_strength=100)
img10 = ill.image_text(image=img10, text="White", y=0.9, size=80, color="white")

final = ill.image_mosaic([img1, img2, img3, img4, img5, img6, img7, img8, img9, img10], ncols=2)
final
final.save("figure3.png")

# MOSAIC DELBOEUF
imgs = []
for strength in [-2, -1, 0, 1, 2]:
    for diff in [-2, -1, 0, 1, 2]:
        stim = ill.delboeuf_image(height=800, width=800, illusion_strength=strength, difference=diff)

        PIL.ImageDraw.Draw(stim).text((20, 0),
                                    f"Strength = {strength}, Difference = {diff}",
                                    (0, 0, 0),
                                    font = PIL.ImageFont.truetype("arial.ttf", 50))

        imgs.append(stim)

new = ill.image_mosaic(imgs)
final = new.copy()

# Vertical lines
for val in [-0.6, -0.2, 0.2, 0.6]:
    if(np.abs(val) == 0.2):
        color = (110,110,110)
    else:
        color = (220, 220, 220)
    final = ill.image_line(image=final, x=val, length=2, color=color, size=2)
    final = ill.image_line(image=final, y=val, length=2, color=color, rotate=90, size=2)

final
final.save("figure4.png")

