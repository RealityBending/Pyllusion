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


# MOSAIC
imgs = []
for strength in [-2, -1, 0, 1, 2]:
    for diff in [-2, -1, 0, 1, 2]:
        stim = ill.delboeuf_image(height=800, width=800, illusion_strength=strength, difference=diff)

        PIL.ImageDraw.Draw(stim).text((20, 0),
                                    f"Strength = {strength}, Difference = {diff}",
                                    (0, 0, 0),
                                    font = PIL.ImageFont.truetype("arial.ttf", 40))

        imgs.append(stim)

nrows, ncols = int(np.sqrt(len(imgs))), int(np.sqrt(len(imgs)))
new = PIL.Image.new('RGB', (imgs[0].width * nrows, imgs[0].height * ncols))
i = 0
for row in range(nrows):
    for col in range(ncols):
        new.paste(imgs[i], (imgs[i].width * row, imgs[i].height * col))
        i += 1

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
