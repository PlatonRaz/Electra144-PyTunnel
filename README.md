# Electra 144-PyTunnel

## Introduction

**Electra 144-PyTunnel** is a Python-based implementation of the steady-state thermal rating calculations for underground cable tunnels. The methodology is based on the **Electra No. 144** technical reference (CIGRÉ, 1992). This tool models heat transfer in a circular tunnel environment and performs numerical simulations using an iterative convergence approach.


- This tool performs a numerical steady-state simulation and visualisation to support engineering analysis of tunnel heat transfer performance.
- This is an independent computational implementation and is not affiliated with or endorsed by CIGRE or the authors of Electra 144.

## Features

- Iterative steady-state calculation of thermal tunnel performance against tunnel length or air velocity
- Graphical User Interface (GUI) for input control and result display
- Automated graphical output using a modified version of `pandastable`

## Libraries used

- pandas>=2.3.1  
- tkinter>=8.6  
- pandastable>=0.14.0


#### The `pandastable` library included in this project contains modified files (`plotting.py`, `core.py`) with improvements for plotted graphs, including:

- Automatic creation of plotted graphs  
- Higher resolution for the Y axis  
- Markers on every plotted point  
- Enabled grid display  

Additionally, a `pandastable.pyi` stub file has been created to prevent IDE warnings about missing type information.

**Note:** Because of these changes, the modified `pandastable` library is included within the project folder.

