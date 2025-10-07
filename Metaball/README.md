# 🧪 Metaball
This tutorial visualizes real-time metaballs animation in Python, leveraging raylib for rendering and Numba to accelerate performance-critical field calculations. Metaballs are organic-looking blobs that merge and separate in a visually fluid way, often used in computer graphics to simulate liquids, blobby shapes, or soft-body dynamics.

## 🚀 Features
- Fast metaball rendering using Numba JIT compilation
- Interactive, real-time animation with raylib
- Easy customization of blob count, speed, size, and more
- Vectorized math for optimal performance

## 🛠️ Requirements
- Tools
  - Python 3.11+
  - uv 0.1.0+
  - just 1.40.0+
- Dependencies
  - raylib
  - numpy
  - numba

Install the dependencies with:

```bash
just sync
```
or
```bash
uv sync
```

## 📄 How It Works
Metaballs are rendered by evaluating a field function over each pixel. The sum of the field values from all metaballs at a pixel is drawn by mapping this value to a color palette.

Each metaball m contributes:

```math
f_m(x, y) = r_m² / ((x - c_{m_x})² + (y - c_{m_y})²)
```
Where:
- r_m is the radius of the metaball m
- (c_m_x, c_m_y) is the center of the metaball m

Then a pixel value is:
```math
pixel(x, y) = \sum_{i=1}^n f_i(x, y)
```
Where:
- n is the number of metaballs

## 🧾 Usage
Run the script:
```bash
just run
```
or
```bash
uv run metaball
```
You can configure parameters inside \_\_init\_\_.py such as:
- METABALLS_COUNT
- METABALLS_PALETTE
- METABALL_RADIUS
- METABALL_SPEED

## 🧠 Customization Tips
- Experiment with different field equations for alternative effects.
- Add user interaction to control metaballs via mouse or keyboard.
- Export frames to generate video or GIF.

## 📁 File Structure
```
metaball/
├── justfile
├── pyproject.toml
├── README.md
├── src
│   └── metaball
│       ├── __init__.py
│       ├── __main__.py
│       ├── metaballs.py
│       ├── palettes.py
│       └── sketch.py
├── tests
│   └── metaball
└── uv.lock
```

## Contributing
Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

## 📜 License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](../LICENSE) file for details.
