import numpy as np


def movement_matrix(
    n_frames=10,
    n=50,
    angle=None,
    speed=None,
    keep_in_window=False,
    keep_in_circle=False,
    **kwargs
):
    """
    """
    if angle is None:
        angle = np.random.uniform(0, 360, size=n)
    elif isinstance(angle, (int, float)):
        angle = np.array([angle] * n)
    if speed is None:
        speed = np.random.uniform(0, 10, size=n)
    elif isinstance(speed, (int, float)):
        speed = np.array([speed] * n)
    y_movement = np.sin(np.radians(angle)) * speed / 200
    x_movement = np.cos(np.radians(angle)) * speed / 200

    # Mask sanitization
    if keep_in_window is True:
        keep_in_window = 1
    if keep_in_circle is True:
        keep_in_circle = 1

    # Initialize arrays
    x = np.zeros((n_frames, n))
    y = np.zeros((n_frames, n))

    # Starting locations
    if keep_in_circle is not False:
        a = np.random.uniform(0, 1, n) * 2 * np.pi
        r = keep_in_circle * np.sqrt(np.random.uniform(0, 1, n))
        x[0] = r * np.cos(a)
        y[0] = r * np.sin(a)
    else:
        x[0] = np.random.uniform(-1, 1, n)
        y[0] = np.random.uniform(-1, 1, n)

    for frame in range(1, n_frames):
        # Add movement
        x[frame] = x[frame - 1] + x_movement
        y[frame] = y[frame - 1] + y_movement

        # Deal with teleportation
        if keep_in_window is not False:
            idx = np.abs(x[frame]) > keep_in_window | np.abs(y[frame]) > keep_in_window
            x[frame][idx] = -1 * x[frame][idx]
            y[frame][idx] = -1 * y[frame][idx]

        if keep_in_circle is not False:
            idx = np.sqrt((x[frame] - 0) ** 2 + (y[frame] - 0) ** 2) > keep_in_circle
            x[frame][idx] = -1 * x[frame][idx]
            y[frame][idx] = -1 * y[frame][idx]

    return x, y

