📦 Project: Interactive ASCII Torus Renderer
A playful, real-time ASCII visualization of a 3D torus rendered in a Tkinter window, with interactive rotation controls and per-character color effects. Built entirely in Python using numpy and tkinter.

🚀 Features
Real-time ASCII rendering of a 3D torus

Rotation around X, Y, Z axes via sliders

Random rotation mode with override

Per-character random color mode

Separate control and rendering windows

Fully multithreaded for smooth interaction

🧠 Math Behind the Torus
Torus Parametric Equations
A torus is defined by two radii:

Major radius 
𝑅
: distance from center to tube center

Minor radius 
𝑟
: radius of the tube

The parametric surface is:

𝑥
(
𝜃
,
𝜙
)
=
(
𝑅
+
𝑟
cos
⁡
𝜃
)
cos
⁡
𝜙
𝑦
(
𝜃
,
𝜙
)
=
(
𝑅
+
𝑟
cos
⁡
𝜃
)
sin
⁡
𝜙
𝑧
(
𝜃
,
𝜙
)
=
𝑟
sin
⁡
𝜃
Where:

𝜃
∈
[
0
,
2
𝜋
]
 is the angle around the tube

𝜙
∈
[
0
,
2
𝜋
]
 is the angle around the ring

Rotation Matrices
To rotate the torus in 3D space, we apply rotation matrices:

X-axis:

𝑅
𝑥
=
[
1
0
0
0
cos
⁡
𝛼
−
sin
⁡
𝛼
0
sin
⁡
𝛼
cos
⁡
𝛼
]
Y-axis:

𝑅
𝑦
=
[
cos
⁡
𝛽
0
sin
⁡
𝛽
0
1
0
−
sin
⁡
𝛽
0
cos
⁡
𝛽
]
Z-axis:

𝑅
𝑧
=
[
cos
⁡
𝛾
−
sin
⁡
𝛾
0
sin
⁡
𝛾
cos
⁡
𝛾
0
0
0
1
]
Final rotation:

rotated_vector
=
𝑅
𝑧
𝑅
𝑦
𝑅
𝑥
⋅
𝑣
⃗
Projection
We use a simple perspective projection:

screen_x
=
𝐾
1
⋅
𝑥
𝐾
2
+
𝑧
,
screen_y
=
𝐾
1
⋅
𝑦
𝐾
2
+
𝑧
Where:

𝐾
1
 scales the projection

𝐾
2
 simulates camera distance

🛠️ Installation
bash
git clone https://github.com/yourusername/ascii-torus
cd ascii-torus
python ascii_torus.py
Requires:

Python 3.7+

numpy (install via pip install numpy)

No external GUI libraries needed — pure tkinter.

🎮 Controls
Sliders: Rotate around X, Y, Z axes

Toggle Random Colors: Per-character color chaos

Resume Random Rotation: Releases slider control
