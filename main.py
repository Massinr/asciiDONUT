import numpy as np
import time
import threading
import tkinter as tk
import random

# Shared state
state = {
    'angle_x': 0.0,
    'angle_y': 0.0,
    'angle_z': 0.0,
    'use_sliders': False,
    'color_mode': False
}

# ANSI color codes for Tkinter Text widget tags
ansi_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white']

def random_spin_loop():
    while True:
        if not state['use_sliders']:
            state['angle_x'] += random.uniform(-0.05, 0.05)
            state['angle_y'] += random.uniform(-0.05, 0.05)
            state['angle_z'] += random.uniform(-0.05, 0.05)
        time.sleep(0.05)

def render_ascii_torus(text_widget):
    width, height = 40, 20
    chars = ".,-~:;=!*#$@"
    R1, R2 = 0.5, 1.0
    K2 = 3.0
    K1 = width * K2 * 3 / (8 * (R1 + R2))

    # Pre-create tags for colors
    for color in ansi_colors:
        text_widget.tag_config(color, foreground=color)

    while True:
        zbuffer = np.zeros((height, width))
        output = [[' ' for _ in range(width)] for _ in range(height)]
        color_map = [['white' for _ in range(width)] for _ in range(height)]

        ax = state['angle_x']
        ay = state['angle_y']
        az = state['angle_z']

        cx, sx = np.cos(ax), np.sin(ax)
        cy, sy = np.cos(ay), np.sin(ay)
        cz, sz = np.cos(az), np.sin(az)

        rot_x = np.array([[1, 0, 0],
                          [0, cx, -sx],
                          [0, sx, cx]])

        rot_y = np.array([[cy, 0, sy],
                          [0, 1, 0],
                          [-sy, 0, cy]])

        rot_z = np.array([[cz, -sz, 0],
                          [sz, cz, 0],
                          [0, 0, 1]])

        rotation = rot_z @ rot_y @ rot_x

        for theta in np.linspace(0, 2*np.pi, 60):
            costheta = np.cos(theta)
            sintheta = np.sin(theta)

            for phi in np.linspace(0, 2*np.pi, 60):
                cosphi = np.cos(phi)
                sinphi = np.sin(phi)

                x = (R2 + R1 * costheta) * cosphi
                y = (R2 + R1 * costheta) * sinphi
                z = R1 * sintheta

                vec = np.array([x, y, z])
                rotated = rotation @ vec

                x, y, z = rotated
                ooz = 1 / (K2 + z)
                xp = int(width / 2 + K1 * ooz * x)
                yp = int(height / 2 - K1 * ooz * y)

                L = cosphi * costheta * sy - cx * costheta * sinphi - sx * sintheta + cy * (cx * sintheta - costheta * sx * sinphi)
                luminance_index = int(max(0, L * 8))

                if 0 <= xp < width and 0 <= yp < height and ooz > zbuffer[yp][xp]:
                    zbuffer[yp][xp] = ooz
                    output[yp][xp] = chars[luminance_index]
                    color_map[yp][xp] = random.choice(ansi_colors) if state['color_mode'] else 'white'

        text_widget.delete("1.0", tk.END)
        for row_idx, row in enumerate(output):
            for col_idx, char in enumerate(row):
                color = color_map[row_idx][col_idx]
                text_widget.insert(tk.END, char, color)
            text_widget.insert(tk.END, '\n')
        time.sleep(0.03)

def launch_gui():
    donut_win = tk.Tk()
    donut_win.title("ASCII Donut")

    text = tk.Text(donut_win, width=40, height=20, font=("Courier", 10), bg="black")
    text.pack()

    control_win = tk.Toplevel()
    control_win.title("Rotation Controls")

    def update_angle(var, axis):
        state['use_sliders'] = True
        state[axis] = float(var)

    sliders = {
        'angle_x': tk.Scale(control_win, from_=0, to=6.28, resolution=0.01,
                            orient='horizontal', label='Rotate X',
                            command=lambda val: update_angle(val, 'angle_x')),
        'angle_y': tk.Scale(control_win, from_=0, to=6.28, resolution=0.01,
                            orient='horizontal', label='Rotate Y',
                            command=lambda val: update_angle(val, 'angle_y')),
        'angle_z': tk.Scale(control_win, from_=0, to=6.28, resolution=0.01,
                            orient='horizontal', label='Rotate Z',
                            command=lambda val: update_angle(val, 'angle_z'))
    }

    for slider in sliders.values():
        slider.pack(padx=10, pady=5)

    def toggle_color():
        state['color_mode'] = not state['color_mode']

    def resume_random():
        state['use_sliders'] = False

    tk.Button(control_win, text="Toggle Random Colors", command=toggle_color).pack(pady=5)
    tk.Button(control_win, text="Resume Random Rotation", command=resume_random).pack(pady=5)

    threading.Thread(target=render_ascii_torus, args=(text,), daemon=True).start()
    threading.Thread(target=random_spin_loop, daemon=True).start()
    donut_win.mainloop()

launch_gui()
