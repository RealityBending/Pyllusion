# Load packages
import pyllusion
from psychopy import visual, event

# Create parameters
parameters = pyllusion.delboeuf_parameters(illusion_strength=1, difference=2)

# Initiate Window
window = visual.Window(size=[1820, 980], winType='pygame', color='white', fullscr=False)

# Display illusion
pyllusion.delboeuf_psychopy(window=window, parameters=parameters)

# Refresh and close window
window.flip()
event.waitKeys()  # Press any key to close
window.close()
