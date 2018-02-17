"""
Transparency-from-motion illusion.
"""
from . import pyllusion_path

import pygame

import numpy as np
import pandas as pd
import neuropsydia as n
import datetime




def TFM(angle=0, n_points=1000, motion_slow=0, motion_size=75, box_size=8, point_size=0.05, point_speed=1, ITI=1000):
    """
    """

    angle_rad = np.radians(angle)
    y_movement = np.sin(np.radians(angle))*point_speed
    x_movement = np.cos(np.radians(angle))*point_speed


    # Generate points
    circle_r = n.Coordinates.to_pygame(distance_x=box_size/2)
    circle_x = n.Coordinates.to_pygame(x=0)
    circle_y = n.Coordinates.to_pygame(y=0)

    half1_x = []
    half1_y = []
    half2_x = []
    half2_y = []

    for point in range(int(n_points/2)):
        alpha = 2 * np.pi * np.random.random()
        r = circle_r * np.random.random()
        x = r * np.cos(alpha) + circle_x
        y = r * np.sin(alpha) + circle_y
        half1_x.append(x)
        half1_y.append(y)
    for point in range(int(n_points/2)):
        alpha = 2 * np.pi * np.random.random()
        r = circle_r * np.random.random()
        x = r * np.cos(alpha) + circle_x
        y = r * np.sin(alpha) + circle_y
        half2_x.append(x)
        half2_y.append(y)

    half1_x = np.array(half1_x)
    half1_y = np.array(half1_y)
    half2_x = np.array(half2_x)
    half2_y = np.array(half2_y)



    # Mask
    box_size = n.Coordinates.to_pygame(distance_y = box_size)
    x = n.screen_width/2-box_size/2
    y = (n.screen_height-box_size)/2

    # Preparation
    n.newpage("black", auto_refresh=False)
#    n.newpage("grey", auto_refresh=False)
    pygame.draw.circle(n.screen, n.color("grey"), (int(n.screen_width/2), int(n.screen_height/2)), int(abs(box_size)/2), 0)
    n.write("+", color="white", size=1.5)
    n.refresh()
    n.time.wait(ITI)

    # Movement
    time_start = datetime.datetime.now()
    for i in range(motion_size):
        n.newpage("black", auto_refresh=False)
#        n.newpage("grey", auto_refresh=False)
        pygame.draw.circle(n.screen, n.color("grey"), (int(n.screen_width/2), int(n.screen_height/2)), int(abs(box_size)/2), 0)

        for point in range(len(half1_x)):
            pygame.draw.circle(n.screen, n.color("black"), (int(half1_x[point]), int(half1_y[point])), 3, 0)
#            n.circle(x=half1_x[point], y=half1_y[point], size=point_size, fill_color="black")
        for point in range(len(half2_x)):
            pygame.draw.circle(n.screen, n.color("black"), (int(half2_x[point]), int(half2_y[point])), 3, 0)
#            n.circle(x=half2_x[point], y=half2_y[point], size=point_size, fill_color="black")

        half1_x += x_movement
        half1_y -= y_movement
        half2_x -= x_movement
        half2_y += y_movement
        # TODO: ensure that points stay in the mask area (and transport them from one side to another if needed)
        n.refresh()
        if motion_slow > 0:
            n.time.wait(motion_slow)

    # Save
    duration = datetime.datetime.now()-time_start
    parameters = {"Angle": angle,
                  "Angle_Radian": angle_rad,
                  "n_Points": n_points,
                  "Box_Size": box_size,
                  "Motion_Size": motion_size,
                  "Point_Size": point_size,
                  "Point_Speed": point_speed,
                  "Mask_Corrdinates": (int(n.screen_width/2), int(n.screen_height/2)),
                  "Mask_Size": int(abs(box_size)/2),
                  "ITI": ITI,
                  "Movement_Duration": duration}

    return(parameters)


def TFM_response(parameters):
    pygame.mouse.set_visible(True)

    n.newpage("grey")
    pygame.draw.circle(n.screen, n.color("black"), parameters["Mask_Corrdinates"], parameters["Mask_Size"], 0)

    n.image(pyllusion_path + "arrow_grey.png", x=-1.7, y=-6.2, size=2, rotate=parameters["Angle"]+180, scale_by="width")
    n.image(pyllusion_path + "arrow_grey.png", x=-2.3, y=-5.8, size=2, rotate=parameters["Angle"]+180, scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=-2, y=-6, size=3, rotate=parameters["Angle"], scale_by="width")


    n.image(pyllusion_path + "arrow_grey.png", x=1.7, y=-6.2, size=2, rotate=parameters["Angle"], scale_by="width")
    n.image(pyllusion_path + "arrow_grey.png", x=2.3, y=-5.8, size=2, rotate=parameters["Angle"], scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=2, y=-6, size=3, rotate=parameters["Angle"]+180, scale_by="width")


    n.line(left_x=0, left_y=-10, right_x=0, right_y=10, line_color="black", thickness=1)
    n.refresh()

    loop = True
    while loop == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            x, y = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()==(1,0,0):
                loop = False


    x, y = n.Coordinates.from_pygame(x=x, y=y)
    if x < 0:
        response_side = "LEFT"
        response = parameters["Angle"]
        n.rectangle(x=-5, width=10, height=20, fill_color="green")
    else:
        response_side = "RIGHT"
        response = parameters["Angle"]+180
        n.rectangle(x=5, width=10, height=20, fill_color="green")
    if response >= 360:
        response -= 360
    pygame.draw.circle(n.screen, n.color("black"), parameters["Mask_Corrdinates"], parameters["Mask_Size"], 0)
#    n.write(str(response), color="white")
    n.refresh()
    n.time.wait(50)
    pygame.mouse.set_visible(False)
    return(response, response_side)

