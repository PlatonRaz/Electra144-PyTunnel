import math
from cables import cables

# Constants for Electra 143 Thermal Tunnel Rating

CONSTANTS = {
    # Temperatures (°C)
    'mean_air_inlet_temperature': 20.0,
    'remote_soil_temperature': 20.0,
    'conductor_temperature_limit': 85.0,

    # Tunnel dimensions (m)
    'tunnel_burial_depth_to_tunnel_center_line_1': 4.0,
    'diameter_j_8': 3.0,   # Tunnel diameter options
    'diameter_j_9': 6.0,
    'diameter_j_10': 9.0,
    'diameter_j_11': 12.0,
    'diameter_j_12': 15.0,

    'tunnel_overall_length': 1000.0,  # Tunnel length (m)

    # Physical properties
    'specific_heat_per_unit_volume_for_rock': 2.00e6,      # J/(m³·K)
    'thermal_resistivity_of_the_soil_1': 1.0,              # K·m/W
    'specific_heat_for_air_per_unit_volume': 1.18e3,       # J/(m³·K)
    'kinematic_viscosity_for_air': 1.57e-5,                # m²/s
    'thermal_conductivity_for_air': 0.0262,                # W/(m·K)
    'mean_air_velocity': 2.0,                              # m/s

    # Radiation constants
    'stefan_boltzman_constant': 0.567e-7,                  # W/(m²·K⁴)
    'ratio_of_cable_radiating_area_to_cable_surface_area': 0.90,
    'effective_cable_surface_emissivity': 0.9,

    # Other constants
    'weedy_constant': 0.1150,
    'num_cables': len(cables),
    'nodes_in_soil_region': 3
}

# Derived quantities based on tunnel diameter and air velocity
CONSTANTS['tunnel_cross_sect_area'] = math.pi * (CONSTANTS['diameter_j_8'] / 2) ** 2  # m²
CONSTANTS['volumetric_flow_rate_of_air'] = CONSTANTS['tunnel_cross_sect_area'] * CONSTANTS['mean_air_velocity']  # m³/s

# Prandtl number for air flow 
CONSTANTS['prondtl_number'] = (
    CONSTANTS['specific_heat_for_air_per_unit_volume'] * CONSTANTS['kinematic_viscosity_for_air']
) / CONSTANTS['thermal_conductivity_for_air']
