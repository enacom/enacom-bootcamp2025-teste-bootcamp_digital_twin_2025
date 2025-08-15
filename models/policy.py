import random

class Policy:
    """
    Base policy class for vehicle routing decisions.
    
    A policy defines how vehicles make decisions about loading, unloading,
    and routing in the logistics network. This is a base implementation
    that can be extended with more sophisticated optimization algorithms.
    
    Attributes:
        locations (dict): Dictionary of available locations
        fleet (list): List of available vehicles
    """
    
    def __init__(self, locations, fleet):
        """
        Initialize a new Policy instance.
        
        Args:
            locations (dict): Dictionary of available locations
            fleet (list): List of available vehicles
        """
        self.locations = locations
        self.fleet = fleet

    def choose_actions(self, vehicle, now):
        """
        Choose actions for a vehicle at a given time.
        
        This method determines what actions a vehicle should take,
        including unloading orders, loading new orders, and selecting
        the next location to visit.
        
        Args:
            vehicle: Vehicle object to make decisions for
            now (int): Current simulation time
            
        Returns:
            tuple: (unloads, loads, next_location) where:
                - unloads: list of orders to unload
                - loads: list of orders to load
                - next_location: next location to visit
        """
        unloads = []
        loads = []
        next_location = vehicle.current_location

        unloads = vehicle.unload(self.locations[vehicle.current_location])

        for order in self.locations[vehicle.current_location].load_queue:
            if vehicle.load_order(order):
                loads.append(order)

        next_location = self.get_next_location(vehicle.current_location)
        
        return unloads, loads, next_location

    def get_next_location(self, current_location):
        """
        Determine the next location for a vehicle to visit.
        
        This method implements the routing logic to decide which location
        a vehicle should visit next. Currently uses a simple random selection
        but can be enhanced with optimization algorithms.
        
        Args:
            current_location (str): Current location identifier
            
        Returns:
            str: Next location identifier to visit
        """
        return random.choice(list(self.locations.keys()))
