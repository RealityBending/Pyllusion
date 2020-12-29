# -*- coding: utf-8 -*-
# Import packages
import pyllusion as ill
import numpy as np
from psychopy import visual, event, gui
import os
import sys
import wx

# Set up GUI
gui = gui.Dlg()
gui.addField("Subject ID:")
gui.addField("Experiment Title:")

gui.show()

# subj_id = gui.data[0]
# rep_num = gui.data[1]

# data_path = subj_id + "_rep_" + rep_num + ".tsv"

# if os.path.exists(data_path):
#     sys.exit("Data path " + data_path + " already exists!")
# exp_data = []

# Initiate window
app = wx.App(False)
width = wx.GetDisplaySize()[0]
height = wx.GetDisplaySize()[1]

window = visual.Window(size=[width-100, height-100], fullscr=False,
                       screen=0, winType='pyglet', monitor='testMonitor',
                       allowGUI=False, color="white",
                       blendMode='avg', units='pix')

# # Set up mouse event
# mouse = event.Mouse(visible=True, win=window)

# Start instructions
instructions = visual.TextStim(win=window, wrapWidth=350, color="black")

instructions.text = """
You will now see some visual illusions.\n
Press any key to begin.
"""
instructions.draw()
window.flip()
event.waitKeys()

# Initiate parameters for illusion and draw 

difficulty = np.random.randint(low=1, high=6, size=(5,))
strength = np.random.randint(low=1, high=6, size=(5,))
parameters_list = []

for diff, strg in zip(difficulty, strength):
    parameters = ill.ebbinghaus_parameters(difficulty=diff, illusion_strength=strg)
    parameters_list.append(parameters)

for param in parameters_list:  # Loop illusions to display
    # print(param)
    ill.ebbinghaus_psychopy(window=window, parameters=param)
    window.flip()
    event.waitKeys()  # Press any key to move on
 
message_end = visual.TextStim(win=window, wrapWidth=350, color="black")

message_end.text = """
You have now come to the end of the experiment.
Press any key to end.
"""
message_end.draw()
window.flip()
event.waitKeys()

window.close()


