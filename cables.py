"""
INPUT DATA FOR TEST PROBLEM

`The following data are used to represent three cables, spaced vetically within a ventilated cable tunnel. The spacing between the cables is three times their diameter.`
"""

cables = [
    {
        'conductor_cross_sect_area': 2313,  # mm²
        'conductor_outer_diameter': 0.0575,  # m
        'dielectric_outer_diameter': 0.1060,  # m
        'sheath_outer_diameter': 0.1140,  # m
        'overall_diameter_of_cable': 0.1220,  # m
        'specific_heat_per_unit_volume_for_conductor': 3.45e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_dielectric': 2.00e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_sheath': 1.45e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_oversheath': 2.40e6,  # J/(m³·K)
        'dielectric_thermal_resistivity': 5.0,  # K·m/W
        'oversheath_thermal_resistivity': 3.5,  # K·m/W
        'conductor_ac_resistance': 12.52e-6,  # ohm/m
        'dielectric_loss_per_unit_length': 13.35,  # W/m
        'sheath_loss_factor': 0.04503,
        'current': 2000,  # A
        'thermal_resistance_conductor': 12.52e-6,  # ohm/m
        'tan_delta': 0.001,
        'sheath_thickness' : 0.0038,
        'outer_sheath_thickness' : 0.004  # m

    },
      {
        'conductor_cross_sect_area': 2313,  # mm²
        'conductor_outer_diameter': 0.0575,  # m
        'dielectric_outer_diameter': 0.1060,  # m
        'sheath_outer_diameter': 0.1140,  # m
        'overall_diameter_of_cable': 0.1220,  # m
        'specific_heat_per_unit_volume_for_conductor': 3.45e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_dielectric': 2.00e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_sheath': 1.45e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_oversheath': 2.40e6,  # J/(m³·K)
        'dielectric_thermal_resistivity': 5.0,  # K·m/W
        'oversheath_thermal_resistivity': 3.5,  # K·m/W
        'conductor_ac_resistance': 12.52e-6,  # ohm/m
        'dielectric_loss_per_unit_length': 13.35,  # W/m
        'sheath_loss_factor': 0.04503,
        'current': 2000,  # A
        'thermal_resistance_conductor': 12.52e-6,  # ohm/m
        'tan_delta': 0.001,
        'sheath_thickness' : 0.0038,
        'outer_sheath_thickness' : 0.004  # m

    },
     
     {
       'conductor_cross_sect_area': 2313,  # mm²
        'conductor_outer_diameter': 0.0575,  # m
        'dielectric_outer_diameter': 0.1060,  # m
        'sheath_outer_diameter': 0.1140,  # m
        'overall_diameter_of_cable': 0.1220,  # m
        'specific_heat_per_unit_volume_for_conductor': 3.45e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_dielectric': 2.00e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_sheath': 1.45e6,  # J/(m³·K)
        'specific_heat_per_unit_volume_for_oversheath': 2.40e6,  # J/(m³·K)
        'dielectric_thermal_resistivity': 5.0,  # K·m/W
        'oversheath_thermal_resistivity': 3.5,  # K·m/W
        'conductor_ac_resistance': 12.52e-6,  # ohm/m
        'dielectric_loss_per_unit_length': 13.35,  # W/m
        'sheath_loss_factor': 0.04503,
        'current': 2000,  # A
        'thermal_resistance_conductor': 12.52e-6,  # ohm/m
        'tan_delta': 0.001,
        'sheath_thickness' : 0.0038,
        'outer_sheath_thickness' : 0.004  # m

    }
    
]

for cable in cables:
    cable['dielectric_thickness'] = (cable['dielectric_outer_diameter'] - cable['conductor_outer_diameter']) / 2  # m
    cable['conductor_loss'] = cable['current']**2 * cable['thermal_resistance_conductor']  # W/m


    
    

   