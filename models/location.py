
class Location:
    """
    Represents a location in the logistics network.
    
    A location can be a warehouse, distribution center, or any point where
    loading/unloading operations can occur. Each location has specific
    time parameters for loading and unloading operations.
    
    Attributes:
        location_id (str): Unique identifier for the location
        base_load (int): Base time required for loading operations
        gamma (int): Time multiplier for loading based on units
        base_unload (int): Base time required for unloading operations
        delta (int): Time multiplier for unloading based on units
        load_queue (list): Queue of orders waiting to be loaded
        unload_queue (list): Queue of orders waiting to be unloaded
    """
    
    def __init__(self, location_id, base_load, gamma, base_unload, delta):
        """
        Initialize a new Location instance.
        
        Args:
            location_id (str): Unique identifier for the location
            base_load (int): Base time required for loading operations
            gamma (int): Time multiplier for loading based on units
            base_unload (int): Base time required for unloading operations
            delta (int): Time multiplier for unloading based on units
        """
        self.location_id = location_id
        self.base_load = base_load
        self.gamma = gamma
        self.base_unload = base_unload
        self.delta = delta
        self.load_queue = []  # Fila de carga (LOAD)
        self.unload_queue = []  # Fila de descarga (UNLOAD)

    def load_time(self, units):
        """
        Calculate the total time required to load a specific number of units.
        
        Args:
            units (int): Number of units to be loaded
            
        Returns:
            int: Total loading time (base_load + gamma * units)
        """
        return self.base_load + self.gamma * units

    def unload_time(self, units):
        """
        Calculate the total time required to unload a specific number of units.
        
        Args:
            units (int): Number of units to be unloaded
            
        Returns:
            int: Total unloading time (base_unload + delta * units)
        """
        return self.base_unload + self.delta * units
