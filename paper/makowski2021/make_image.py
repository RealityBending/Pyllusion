import numpy as np
import PIL
import pyllusion

# PONZO FOR FIG 1 PPT
ponzo = pyllusion.Ponzo(illusion_strength=-15, difference=0.3, size_min=0.5)
img = ponzo.to_image()
img
img.save("ponzo_for_ppt.png")


# MOSAIC Illusions
img1 = pyllusion.Delboeuf(illusion_strength=3)
img1 = img1.to_image(width=1280, height=620)
img1_text = pyllusion.image_text(width=1280, height=90, text="Delboeuf", y=0, size=70)

img2 = pyllusion.Ebbinghaus(illusion_strength=2)
img2 = img2.to_image(width=1280, height=620)
img2_text = pyllusion.image_text(width=1280, height=90, text="Ebbinghaus", y=0, size=70)

img3 = pyllusion.MullerLyer(illusion_strength=-30)
img3 = img3.to_image(width=1280, height=620)
img3_text = pyllusion.image_text(width=1280, height=90, text="Müller-Lyer", y=0, size=70)

img4 = pyllusion.Ponzo(illusion_strength=20)
img4 = img4.to_image(width=1280, height=620)
img4_text = pyllusion.image_text(width=1280, height=90, text="Ponzo", y=0, size=70)

img5 = pyllusion.VerticalHorizontal(illusion_strength=-90)
img5 = img5.to_image(width=1280, height=620)
img5_text = pyllusion.image_text(width=1280, height=90, text="Vertical-Horizontal", y=0, size=70)

img6 = pyllusion.Zollner(illusion_strength=75)
img6 = img6.to_image(width=1280, height=620)
img6_text = pyllusion.image_text(width=1280, height=90, text="Zöllner", y=0, size=70)

img7 = pyllusion.RodFrame(illusion_strength=-11)
img7 = img7.to_image(width=1280, height=620)
img7_text = pyllusion.image_text(width=1280, height=90, text="Rod and Frame", y=0, size=70)

img8 = pyllusion.Poggendorff(illusion_strength=50)
img8 = img8.to_image(width=1280, height=620)
img8_text = pyllusion.image_text(width=1280, height=90, text="Poggendorff", y=0, size=70)

img9 = pyllusion.Contrast(illusion_strength=50)
img9 = img9.to_image(width=1280, height=620)
img9_text = pyllusion.image_text(width=1280, height=90, text="Contrast", y=0, size=70, color="black")

img10 = pyllusion.White(illusion_strength=100)
img10 = img10.to_image(width=1280, height=620)
img10_text = pyllusion.image_text(width=1280, height=90, text="White", y=0, size=70, color="black")

def get_concat_v(im1, im2, background=None):
    dst = PIL.Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

delb = get_concat_v(img1_text, img1)
ebb = get_concat_v(img2_text, img2)
mull = get_concat_v(img3_text, img3)
ponzo = get_concat_v(img4_text, img4)
vert = get_concat_v(img5_text, img5)
zollner = get_concat_v(img6_text, img6)
rod = get_concat_v(img7_text, img7)
pogg = get_concat_v(img8_text, img8)
contrast = get_concat_v(img9_text, img9)
white = get_concat_v(img10_text, img10)
final = pyllusion.image_mosaic([delb, ebb, mull, ponzo, vert, zollner, rod, pogg, contrast, white], ncols=2)
final.save("figure3.png")



# # MOSAIC Illusions
# img1 = pyllusion.delboeuf_image(width=1280, height=720, illusion_strength=3)
# img1 = pyllusion.image_text(image=img1, text="Delboeuf", y=0.9, size=80)
# img2 = pyllusion.ebbinghaus_image(width=1280, height=720, illusion_strength=2)
# img2 = pyllusion.image_text(image=img2, text="Ebbinghaus", y=0.9, size=80)
# img3 = pyllusion.mullerlyer_image(width=1280, height=720, illusion_strength=30)
# img3 = pyllusion.image_text(image=img3, text="Müller-Lyer", y=0.88, size=80)
# img4 = pyllusion.ponzo_image(width=1280, height=720, illusion_strength=20)
# img4 = pyllusion.image_text(image=img4, text="Ponzo", y=0.88, size=80)
# img5 = pyllusion.verticalhorizontal_image(width=1280, height=720, illusion_strength=90)
# img5 = pyllusion.image_text(image=img5, text="Vertical-Horizontal", y=0.9, size=80)
# img6 = pyllusion.zollner_image(width=1280, height=720, illusion_strength=75)
# img6 = pyllusion.image_text(image=img6, text="Zöllner", y=0.9, size=80)
# img7 = pyllusion.rodframe_image(width=1280, height=720, illusion_strength=11)
# img7 = pyllusion.image_text(image=img7, text="Rod and Frame", y=0.9, size=80)
# img8 = pyllusion.poggendorff_image(width=1280, height=720, illusion_strength=50)
# img8 = pyllusion.image_text(image=img8, text="Poggendorff", y=0.9, size=80)
# img9 = pyllusion.contrast_image(width=1280, height=720, illusion_strength=50)
# img9 = pyllusion.image_text(image=img9, text="Contrast", y=0.9, size=80, color="white")
# img10 = pyllusion.white_image(width=1280, height=720, illusion_strength=100)
# img10 = pyllusion.image_text(image=img10, text="White", y=0.9, size=80, color="white")

# final = pyllusion.image_mosaic([img1, img2, img3, img4, img5, img6, img7, img8, img9, img10], ncols=2)
# final
# final.save("figure3.png")

# MOSAIC DELBOEUF
imgs = []
for strength in [-2, -1, 0, 1, 2]:
    for diff in [-2, -1, 0, 1, 2]:
        stim = pyllusion.Delboeuf(illusion_strength=strength, difference=diff)
        stim = stim.to_image(height=800, width=800)

        PIL.ImageDraw.Draw(stim).text((20, 0),
                                    f"Strength = {strength}, Difference = {diff}",
                                    (0, 0, 0),
                                    font = PIL.ImageFont.truetype("arial.ttf", 50))

        imgs.append(stim)

new = pyllusion.image_mosaic(imgs)
final = new.copy()

# Vertical lines
for val in [-0.6, -0.2, 0.2, 0.6]:
    if(np.abs(val) == 0.2):
        color = (110,110,110)
    else:
        color = (220, 220, 220)
    final = pyllusion.image_line(image=final, x=val, length=2, color=color, size=2)
    final = pyllusion.image_line(image=final, y=val, length=2, color=color, rotate=90, size=2)

final
final.save("figure4.png")

