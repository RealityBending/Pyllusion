# Load packages
import pyllusion
from psychopy import visual, event

# Create parameters
delboeuf = pyllusion.Delboeuf(illusion_strength=1, difference=2)

# Initiate Window
window = visual.Window(size=[1920, 1080], winType='pygame',
                       color='white', fullscr=False)

# Display illusion
delboeuf.to_psychopy(window)

# Refresh and close window
window.flip()
event.waitKeys()  # Press any key to close
window.close()