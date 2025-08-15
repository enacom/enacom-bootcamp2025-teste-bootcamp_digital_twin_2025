class Vehicle:
    """
    Represents a vehicle in the logistics fleet.
    
    A vehicle can transport orders between locations and has a limited capacity.
    Each vehicle tracks its current location, load, and availability status.
    
    Attributes:
        vehicle_id (str): Unique identifier for the vehicle
        capacity (int): Maximum number of orders the vehicle can carry
        current_location (str): Current location identifier
        load (list): List of orders currently loaded on the vehicle
        available_at (int): Time when the vehicle will be available for next task
    """
    
    def __init__(self, vehicle_id, capacity, start_location):
        """
        Initialize a new Vehicle instance.
        
        Args:
            vehicle_id (str): Unique identifier for the vehicle
            capacity (int): Maximum number of orders the vehicle can carry
            start_location (str): Initial location identifier
        """
        self.vehicle_id = vehicle_id
        self.capacity = capacity
        self.current_location = start_location
        self.load = []
        self.available_at = 0
    
    def __str__(self):
        """
        String representation of the vehicle.
        
        Returns:
            str: String describing the vehicle and its current location
        """
        return f"Vehicle {self.vehicle_id} at {self.current_location}"

    def unload(self, location):
        """
        Unload orders at a specific location.
        
        Simulates unloading orders that have the specified location as their destination.
        Orders are removed from the vehicle's load when unloaded.
        
        Args:
            location: Location object where unloading occurs
            
        Returns:
            list: List of orders that were unloaded
        """
        unloaded = []
        for order in self.load:
            if order.destination == location.location_id:
                unloaded.append(order)
                self.load.remove(order)
        return unloaded
    
    def load_order(self, order):
        """
        Load an order onto the vehicle.
        
        Attempts to load an order if the vehicle has available capacity.
        
        Args:
            order: Order object to be loaded
            
        Returns:
            bool: True if order was loaded successfully, False otherwise
        """
        if len(self.load) < self.capacity:
            self.load.append(order)
            return True
        return False
