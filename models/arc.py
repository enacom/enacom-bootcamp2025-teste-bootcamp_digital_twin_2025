class Arc:
    """
    Represents a connection between two locations in the logistics network.
    
    An arc defines the transit time required to travel from one location
    to another, forming the network topology for vehicle routing.
    
    Attributes:
        from_location (str): Origin location identifier
        to_location (str): Destination location identifier
        transit_time (int): Time required to travel between locations
    """
    
    def __init__(self, from_location, to_location, transit_time):
        """
        Initialize a new Arc instance.
        
        Args:
            from_location (str): Origin location identifier
            to_location (str): Destination location identifier
            transit_time (int): Time required to travel between locations
        """
        self.from_location = from_location
        self.to_location = to_location
        self.transit_time = transit_time

    def __str__(self):
        """
        String representation of the arc.
        
        Returns:
            str: String describing the arc with origin, destination, and transit time
        """
        return f"Arc: {self.from_location} -> {self.to_location}, transit_time {self.transit_time}"
