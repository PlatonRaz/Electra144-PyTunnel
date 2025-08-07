# Electra 144-PyTunnel

**Electra 144-PyTunnel** is a Python-based implementation of steady-state thermal rating calculations for underground cable tunnels. The methodology is based on `Electra No. 144 (CIGRÉ, 1992)`. 

- This tool performs numerical simulations and visualisation to support engineering analysis of tunnel heat transfer performance.
- This is an independent computational implementation and is not affiliated with or endorsed by CIGRE or the authors of Electra 144.

# Features

- Iterative calculation of thermal tunnel performance based on tunnel length and air velocity
- Graphical User Interface (GUI) for input control and result display
- Automated tabular and graphical output using a modified version of `pandastable`
- Modular structure for constants, cable configuration, and numerical routines

## Libraries used

- pandas>=2.3.1  
- tkinter>=8.6  
- pandastable>=0.14.0


**IMPORTANT Modified pandastable library**

The `pandastable` library included in this project contains modified files (`plotting.py`, `core.py`) with improvements for plotted graphs, including:

- Automatic creation of plotted graphs  
- Higher resolution for the Y axis  
- Markers on every plotted point  
- Enabled grid display  

Additionally, a `pandastable.pyi` stub file has been created to prevent IDE warnings about missing type information.

**Note:** Because of these changes, the modified `pandastable` library is included within the project folder.

