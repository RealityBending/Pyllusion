import pyllusion as ill

parameters = ill.ponzo_parameters(illusion_strength=20, 
                                  difficulty=0,
                                  size_min=0.5)
img = ill.ponzo_image(parameters)
img
img.save("ponzo_for_ppt.png")
