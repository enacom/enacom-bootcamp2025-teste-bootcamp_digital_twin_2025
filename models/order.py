
class Order:
    """
    Represents a logistics order to be transported between locations.
    
    An order defines a transportation request with origin, destination,
    timing constraints, and cargo specifications.
    
    Attributes:
        order_id (str): Unique identifier for the order
        origin (str): Origin location identifier
        destination (str): Destination location identifier
        release_time (int): Time when the order becomes available for pickup
        due_time (int): Deadline for order delivery
        units (int): Number of units/cargo to be transported
        delivery_time (int): Actual time when the order was delivered
    """
    
    def __init__(self, order_id, origin, destination, release_time, due_time, units):
        """
        Initialize a new Order instance.
        
        Args:
            order_id (str): Unique identifier for the order
            origin (str): Origin location identifier
            destination (str): Destination location identifier
            release_time (int): Time when the order becomes available for pickup
            due_time (int): Deadline for order delivery
            units (int): Number of units/cargo to be transported
        """
        self.order_id = order_id
        self.origin = origin
        self.destination = destination
        self.release_time = release_time
        self.due_time = due_time
        self.units = units
        self.delivery_time = 0

    def __str__(self):
        """
        String representation of the order.
        
        Returns:
            str: String describing the order with origin, destination, and units
        """
        return f"Order {self.order_id}: {self.origin} -> {self.destination}, {self.units} units"
