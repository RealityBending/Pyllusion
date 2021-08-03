# Import packages
import pyllusion
import numpy as np
from psychopy import visual, event, gui, core
import wx

# Set up GUI
gui = gui.Dlg()
gui.addField("Subject ID:")
gui.addField("Experiment Title:")
gui.show()

# Initiate window
app = wx.App(False)
width = wx.GetDisplaySize()[0]
height = wx.GetDisplaySize()[1]
window = visual.Window(size=[width-100, height-100], fullscr=False,
                       screen=0, winType='pyglet', monitor='testMonitor',
                       allowGUI=False, color="white",
                       blendMode='avg', units='pix')

# Start instructions
instructions = visual.TextStim(win=window, wrapWidth=350, color="black")
instructions.text = """You will now see some visual illusions.\n
Press any key to begin."""
instructions.draw()
window.flip()
event.waitKeys()

# Create fixation cross
fix = visual.TextStim(win=window, name='fix', text='+',
                      font='Arial',
                      pos=(0, 0), height=100, wrapWidth=None, ori=0, 
                      color='black', colorSpace='rgb', opacity=1, 
                      languageStyle='LTR',
                      depth=-1.0)
jitter_duration = np.arange(0.5, 1.5, .15)

# Initiate parameters for illusion and draw 
differences = np.random.randint(low=-2, high=2, size=(5,))
strengths = np.random.randint(low=-2, high=2, size=(5,))
parameters_list = []

for diff, strg in zip(differences, strengths):
    ebbinghaus = pyllusion.Ebbinghaus(difference=diff, illusion_strength=strg)
    parameters = ebbinghaus.get_parameters()
    parameters_list.append(parameters)

for param in parameters_list:  # Loop illusions to display

    # Fixation Cross
    jitter = np.random.choice(jitter_duration)
    fix.draw()
    window.flip()
    core.wait(jitter)

    # Display illusion
    ebbinghaus.to_psychopy(window)
    window.flip()
    event.waitKeys()  # Press any key to move on
 
message_end = visual.TextStim(win=window, wrapWidth=350, color="black")
message_end.text = """You have now come to the end of the experiment.
Press any key to end.
"""
message_end.draw()
window.flip()
event.waitKeys()

window.close()


