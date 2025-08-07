from constants import CONSTANTS
from cables import cables
import math
import pandas as pd


EPSILON = 1e-3
MAX_ITERATIONS = 5

"""
ANALYTICAL SOLUTIONS

`This solution is for steady state temperatures in a circular tunnel and includes radiation within the tunnel and heat loss from the tunnel to the soil surface.`
"""


def thermal_resistances():
    """Thermal resistances within the cable, defined for a single cable, are given by: """
    cable_data = cables[0]
    
    T1 = (cable_data['dielectric_thermal_resistivity'] / (2 * math.pi)) * math.log(1 + 2 * cable_data['dielectric_thickness'] / cable_data['conductor_outer_diameter'])
    T2 = (cable_data['oversheath_thermal_resistivity'] / (2 * math.pi)) * math.log(1 + 2 * cable_data['sheath_thickness'] / cable_data['sheath_outer_diameter'])
    
    _2_times_burial_depth = 2 * CONSTANTS['tunnel_burial_depth_to_tunnel_center_line_1']
    
    Te = (CONSTANTS['thermal_resistivity_of_the_soil_1'] / (2 * math.pi)) * math.log((_2_times_burial_depth / CONSTANTS['diameter_j_8']) + math.sqrt((_2_times_burial_depth / CONSTANTS['diameter_j_8'])**2 - 1))
    
    return T1, T2, Te

def tunnel_thermal_resistances(cable_surface_temp, tunnel_surface_temp, mean_air_velocity):
    """`The thermal resistances within the tunnel are given by: `"""
   
    cable_data = cables[0]
    
    Tst = 1 / (math.pi * cable_data['overall_diameter_of_cable'] * CONSTANTS['ratio_of_cable_radiating_area_to_cable_surface_area'] * CONSTANTS['effective_cable_surface_emissivity'] * CONSTANTS['stefan_boltzman_constant'] * ((cable_surface_temp + 273)**2 + (tunnel_surface_temp + 273)**2)) * 1 / ((cable_surface_temp + 273) + (tunnel_surface_temp + 273))
    
    Tas = 1 / (math.pi * CONSTANTS['thermal_conductivity_for_air'] * CONSTANTS['weedy_constant'] * ((mean_air_velocity * cable_data['overall_diameter_of_cable']) / CONSTANTS['kinematic_viscosity_for_air'])**0.65) 
    
    Tat = 1 / (math.pi * CONSTANTS['thermal_conductivity_for_air'] * 0.023 * ((mean_air_velocity * CONSTANTS['diameter_j_8']) / CONSTANTS['kinematic_viscosity_for_air'])**0.8 * CONSTANTS['prondtl_number']**0.4) 
    
    return Tst, Tas, Tat

def star_delta_transformation(Tst, Tas, Tat):
    """`For N equally-loaded cables, a star-delta transformation is then used to replace Tst, Tas and Tat by the following: `"""
    
    num_cables = CONSTANTS['num_cables']
    denominator = Tst / num_cables + Tas / num_cables + Tat
    
    Ts = (Tst * (Tas / num_cables**2)) / denominator
    Tt = (Tat * (Tst / num_cables)) / denominator
    Ta = (Tat * (Tas / num_cables)) / denominator
    
    return Ts, Tt, Ta

def heat_generation():
    """`The heat generation in a single cable is given by: `"""
   
    cable_data = cables[0]
    total_heat_generation = cable_data['conductor_loss'] * (1 + cable_data['sheath_loss_factor']) + cable_data['dielectric_loss_per_unit_length']
    return total_heat_generation

def air_temperature_at_tunnel_outlet(total_heat_generation, Te, Tt, Ta, tunnel_overall_length):
    """`The air temperature at tunnel outlet is given by: `"""
    num_cables = CONSTANTS['num_cables']
    
    if tunnel_overall_length == 0:
        return CONSTANTS['mean_air_inlet_temperature']
        
    exp_term = math.exp(-tunnel_overall_length / 
                        (CONSTANTS['specific_heat_for_air_per_unit_volume'] * CONSTANTS['volumetric_flow_rate_of_air'] * (Te + Tt + Ta)))
    
    temp_diff_term = (num_cables * total_heat_generation * (Te + Tt) + CONSTANTS['remote_soil_temperature'] - CONSTANTS['mean_air_inlet_temperature'])
    theta_a = temp_diff_term * (1 - exp_term) + CONSTANTS['mean_air_inlet_temperature']
    
    return theta_a

def heat_removed_by_air(total_heat_generation, Te, Tt, Ta, outlet_air_temp):
    """`The heat removed by the air is given by: `"""
    num_cables = CONSTANTS['num_cables']
    Wa = num_cables * total_heat_generation * ((Te + Tt) / (Te + Tt + Ta)) - (outlet_air_temp - CONSTANTS['remote_soil_temperature']) / (Te + Tt + Ta)
    return Wa

def star_point_temperature(outlet_air_temp, Ta, Wa):
    """ `The star point temperature is given by: `"""
    theta_e = outlet_air_temp + Ta * Wa
    return theta_e

def conductor_temperature(conductor_loss, dielectric_loss, T1, total_heat_generation, T2, N, Ts, star_point_temp):
    """`The conductor temperature is given by: `"""
    theta_c = (conductor_loss + dielectric_loss / 2) * T1 + total_heat_generation * (T2 + N * Ts) + star_point_temp
    return theta_c

def cable_surface_temperature_at_tunnel_outlet(star_point_temp, Ts, N, total_heat_generation):
    """1The cable surface temperature at tunnel outlet is given by: `"""
    theta_s = star_point_temp + (Ts * N * total_heat_generation)
    return theta_s

def tunnel_wall_temperature_at_tunnel_outlet(star_point_temp, Tt, N, total_heat_generation, Wa):
    """`The tunnel walI temperature at tunnel outlet is given by: `"""
    theta_t = -Tt * ((N * total_heat_generation) - Wa) + star_point_temp
    return theta_t

def calculate_temperatures(param_value, param_type):
    """
        These equations are written in the order in which they are solved.
        However, the surface and wall temperatures θ_s and θ_t are required 
        in equation (A3.4) but are not calculated until equations (A3.15) and (A3.16). 

        The procedure adopted here is to use an overall iteration. 
        Initial values are specified for θ_s and θ_t (say θ_s(0), θ_t(0)), 
        and equations (A3.1) to (A3.16) are evaluated to obtain new values 
        of θ_s and θ_t. The procedure is repeated until convergence, 
        which occurs rapidly.

        Equation (A3.1) to (A3.16) provide the temperatures at tunnel exit, where they
        are highest. Values at other longitudinal locations are found by first iterating for θ_s and θ_t as specified above. 
        Then the required longitudinal distance issubstituted into eqn. (A3.1 1) 
        instead of the tunnel length, L, and the resulting air temperature substituted into equations (A3.12) onwards.
    """

    # Initial values
    T1, T2, Te = thermal_resistances()
    theta_s = CONSTANTS['mean_air_inlet_temperature']
    theta_t = CONSTANTS['mean_air_inlet_temperature']
    
    for _ in range(MAX_ITERATIONS):
        prev_theta_s = theta_s
        prev_theta_t = theta_t
        
       
        if param_type == 'velocity':
            mean_air_velocity = param_value
            tunnel_overall_length = CONSTANTS['tunnel_overall_length']
       
        elif param_type == 'length': 
            mean_air_velocity = CONSTANTS['mean_air_velocity']
            tunnel_overall_length = param_value

        Tst, Tas, Tat = tunnel_thermal_resistances(theta_s, theta_t, mean_air_velocity)
        Ts, Tt, Ta = star_delta_transformation(Tst, Tas, Tat)
        
        total_heat_generation = heat_generation()
        outlet_air_temp = air_temperature_at_tunnel_outlet(total_heat_generation, Te, Tt, Ta, tunnel_overall_length)
        heat_air_removed = heat_removed_by_air(total_heat_generation, Te, Tt, Ta, outlet_air_temp)
        star_point_temp = star_point_temperature(outlet_air_temp, Ta, heat_air_removed)
        
        conductor_temp = conductor_temperature(
            cables[0]['conductor_loss'], cables[0]['dielectric_loss_per_unit_length'], T1,
            total_heat_generation, T2, CONSTANTS['num_cables'], Ts, star_point_temp
        )
        
        cable_surface_temp = cable_surface_temperature_at_tunnel_outlet(star_point_temp, Ts, CONSTANTS['num_cables'], total_heat_generation)
        tunnel_wall_temp = tunnel_wall_temperature_at_tunnel_outlet(star_point_temp, Tt, CONSTANTS['num_cables'], total_heat_generation, heat_air_removed)
        
        if abs(cable_surface_temp - prev_theta_s) < EPSILON and abs(tunnel_wall_temp - prev_theta_t) < EPSILON:
            break
        
        theta_s = cable_surface_temp
        theta_t = tunnel_wall_temp
            
    return {
        'Outlet Air Temperature ': outlet_air_temp,
        'Tunnel Wall Temperature': tunnel_wall_temp,
        'Cable Surface Temperature': cable_surface_temp,
        'Conductor Temperature': conductor_temp
    }

#========================================================================================================================================================
def iterate_air_vel():
    """Iterates through a range of air velocities and returns a DataFrame of results."""    
    mean_air_velocity_start = CONSTANTS['mean_air_velocity']
    mean_air_velocity_end = 10
    step = 1
    
    results = []
    for mean_air_velocity in range(int(mean_air_velocity_start), int(mean_air_velocity_end) + 1, step):
        calc_results = calculate_temperatures(mean_air_velocity, 'velocity')
        results.append({**{'Mean Air Velocity (m/s)': mean_air_velocity}, **calc_results})
        
    return pd.DataFrame(results)

#========================================================================================================================================================

def iterate_tunnel_length(max_length):
    """Iterates through a range of tunnel lengths and returns a DataFrame of results."""    
    tunnel_length_start = 0
    step = 250
    
    results = []
    for tunnel_overall_length in range(int(tunnel_length_start), int(max_length) + 1, step):
        calc_results = calculate_temperatures(tunnel_overall_length, 'length')
        results.append({**{'Tunnel Length (m)': tunnel_overall_length}, **calc_results})

    return pd.DataFrame(results)