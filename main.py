"""
Main module for the logistics routing simulation system.

This module demonstrates the usage of the simulation framework by loading
sample data from JSON and running simulations with different routing policies.
"""

import json
from models.location import Location
from models.order import Order
from models.vehicle import Vehicle
from models.arc import Arc
from models.policy import Policy
from simulator.simulator import Simulator

def load_simulation_data(json_file_path):
    """
    Load simulation data from JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file containing simulation data
        
    Returns:
        tuple: (locations, arcs, orders, fleet)
    """
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Create Location instances
    locations = {}
    for loc_id, loc_data in data['locations'].items():
        locations[loc_id] = Location(
            location_id=loc_data['location_id'],
            base_load=loc_data['base_load'],
            gamma=loc_data['gamma'],
            base_unload=loc_data['base_unload'],
            delta=loc_data['delta']
        )
    
    # Create Arc instances
    arcs = []
    for arc_data in data['arcs']:
        arcs.append(Arc(
            from_location=arc_data['from_location'],
            to_location=arc_data['to_location'],
            transit_time=arc_data['transit_time']
        ))
    
    # Create Order instances
    orders = []
    for order_data in data['orders']:
        orders.append(Order(
            order_id=order_data['order_id'],
            origin=order_data['origin'],
            destination=order_data['destination'],
            release_time=order_data['release_time'],
            due_time=order_data['due_time'],
            units=order_data['units']
        ))
    
    # Create Vehicle instances
    fleet = []
    for vehicle_data in data['fleet']:
        fleet.append(Vehicle(
            vehicle_id=vehicle_data['vehicle_id'],
            capacity=vehicle_data['capacity'],
            start_location=vehicle_data['start_location']
        ))
    
    return locations, arcs, orders, fleet

def main():
    """
    Main function that demonstrates the simulation system.
    
    Loads logistics data from JSON file including locations, orders, vehicles,
    and network connections, then runs a simulation to demonstrate
    the system's capabilities.
    """
    # Load simulation data from JSON
    json_file_path = "simulation_inputs.json"
    try:
        locations, arcs, orders, fleet = load_simulation_data(json_file_path)
        print(f"Dados carregados com sucesso do arquivo: {json_file_path}")
    except FileNotFoundError:
        print(f"Erro: Arquivo {json_file_path} não encontrado!")
        return
    except json.JSONDecodeError:
        print(f"Erro: Arquivo {json_file_path} não é um JSON válido!")
        return
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return
    
    policy = Policy(locations, fleet)
    
    simulator = Simulator(locations, arcs, orders, fleet)
    
    results = simulator.run(policy)
    
    print("Resultados da Simulação:")
    print(results)


if __name__ == "__main__":
    main()
