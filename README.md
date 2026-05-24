# AeroFlow

Simple Drag Estimator is a lightweight Blender addon that approximates aerodynamic drag force directly inside the 3D viewport.
The addon was built as a simple physics and programming tool for quickly estimating drag force using object dimensions, airflow direction, velocity, and drag coefficient without requiring heavy simulation software.

## What It Solves

---

- quick drag force approximation.
- simple physics experimentation.
- lightweight calculations without expensive simulation workflows.

---

## Features

---

- Drag force estimation
- Adjustable airflow direction
- Velocity control
- Custom drag coefficient input
- Instant calculation results

---

## Installation

---

1. Open Blender
2. Go to:
   Edit → Preferences → Add-ons
3. Click:
   Install...
4. Select the `AeroFlow.py` file
5. Enable the addon

--

## How To Use

1. Select any object in the scene
2. Open the sidebar in the 3D Viewport (`N` key)
3. Open the `Drag` tab
4. Set:
   - airflow direction
   - velocity
   - drag coefficient
5. Click:
   `Calculate Drag`

The calculated drag value will be stored and displayed for the selected object.

## Requirements

---

- Blender 3.0+
  
---
