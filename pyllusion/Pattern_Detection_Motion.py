"""
Transparency-from-motion illusion.
"""
from . import pyllusion_path

import pygame

import numpy as np
import pandas as pd
import neuropsydia as n
import datetime




def PDM(signal=50, angle=0, n_points=1000, motion_slow=0, motion_size=75, box_size=8, point_size=0.05, point_speed=1, ITI=1000):
    """
    Pattern Detection in Motion
    """

    angle_rad = np.radians(angle)
    y_movement = np.sin(np.radians(angle))*point_speed
    x_movement = np.cos(np.radians(angle))*point_speed
    random_rad_angle = np.random.uniform(0, 360, int(n_points*(100-signal)/100))
    random_y_movement = np.sin(np.radians(random_rad_angle))*point_speed
    random_x_movement = np.cos(np.radians(random_rad_angle))*point_speed

    # Generate points
    circle_r = n.Coordinates.to_pygame(distance_x=box_size/2)
    circle_x = n.Coordinates.to_pygame(x=0)
    circle_y = n.Coordinates.to_pygame(y=0)

    signal_x = []
    signal_y = []
    random_x = []
    random_y = []

    for point in range(int(n_points*signal/100)):
        alpha = 2 * np.pi * np.random.random()
        r = circle_r * np.random.random()
        x = r * np.cos(alpha) + circle_x
        y = r * np.sin(alpha) + circle_y
        signal_x.append(x)
        signal_y.append(y)
    for point in range(int(n_points*(100-signal)/100)):
        alpha = 2 * np.pi * np.random.random()
        r = circle_r * np.random.random()
        x = r * np.cos(alpha) + circle_x
        y = r * np.sin(alpha) + circle_y
        random_x.append(x)
        random_y.append(y)

    signal_x = np.array(signal_x)
    signal_y = np.array(signal_y)
    random_x = np.array(random_x)
    random_y = np.array(random_y)



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

        for point in range(len(signal_x)):
            pygame.draw.circle(n.screen, n.color("black"), (int(signal_x[point]), int(signal_y[point])), 3, 0)
#            n.circle(x=half1_x[point], y=half1_y[point], size=point_size, fill_color="black")
        for point in range(len(random_x)):
            pygame.draw.circle(n.screen, n.color("black"), (int(random_x[point]), int(random_y[point])), 3, 0)
#            n.circle(x=half2_x[point], y=half2_y[point], size=point_size, fill_color="black")

        signal_x += x_movement
        signal_y -= y_movement
        random_x -= random_x_movement
        random_y += random_y_movement
        # TODO: ensure that points stay in the mask area (and transport them from one side to another if needed)
        n.refresh()
        if motion_slow > 0:
            n.time.wait(motion_slow)

    # Save
    duration = datetime.datetime.now()-time_start
    parameters = {"Angle": angle,
                  "Angle_Radian": angle_rad,
                  "Signal": signal,
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







def PDM_response(parameters):
    pygame.mouse.set_visible(True)

    n.newpage("grey")
    pygame.draw.circle(n.screen, n.color("black"), parameters["Mask_Corrdinates"], parameters["Mask_Size"], 0)


    angles = np.array([parameters["Angle"], parameters["Angle"]+90, parameters["Angle"]+180, parameters["Angle"]+270])
    angles[angles > 360] = angles[angles > 360] - 360
    angles = np.sort(angles)

    n.image(pyllusion_path + "arrow.png", x=1.5, y=-5, size=2, rotate=angles[0], scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=-1.5, y=-5, size=2, rotate=angles[1], scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=-1.5, y=-8, size=2, rotate=angles[2], scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=1.5, y=-8, size=2, rotate=angles[3], scale_by="width")

    n.line(left_x=-10, left_y=-6.5, right_x=10, right_y=-6.5, line_color="black", thickness=2)
    n.line(left_x=0, left_y=-10, right_x=0, right_y=10, line_color="black", thickness=2)
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
        if y < -6.5:
            response = angles[2]
            n.rectangle(x=-1.5, y=-8, width=3, height=3, fill_color="green", thickness=2)
        else:
            response = angles[1]
            n.rectangle(x=-1.5, y=-5, width=3, height=3, fill_color="green", thickness=2)
    else:
        if y < -6.5:
            response = angles[3]
            n.rectangle(x=1.5,  y=-8, width=3, height=3, fill_color="green", thickness=2)
        else:
            response = angles[0]
            n.rectangle(x=1.5, y=-5, width=3, height=3, fill_color="green", thickness=2)


    n.image(pyllusion_path + "arrow.png", x=1.5, y=-5, size=2, rotate=angles[0], scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=-1.5, y=-5, size=2, rotate=angles[1], scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=-1.5, y=-8, size=2, rotate=angles[2], scale_by="width")
    n.image(pyllusion_path + "arrow.png", x=1.5, y=-8, size=2, rotate=angles[3], scale_by="width")

    n.line(left_x=-10, left_y=-6.5, right_x=10, right_y=-6.5, line_color="black", thickness=2)
    n.line(left_x=0, left_y=-10, right_x=0, right_y=10, line_color="black", thickness=2)


    pygame.draw.circle(n.screen, n.color("black"), parameters["Mask_Corrdinates"], parameters["Mask_Size"], 0)
#    n.write(str(response), color="white")
    n.refresh()
    n.time.wait(50)
    pygame.mouse.set_visible(False)
    return(response)