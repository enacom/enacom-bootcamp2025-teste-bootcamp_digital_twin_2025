class Simulator:
    """
    Main simulation engine for the logistics routing system.
    
    The simulator manages the execution of vehicle routing policies,
    tracks simulation time, and collects performance metrics.
    
    Attributes:
        locations (dict): Dictionary of available locations
        arcs (list): List of network arcs/connections
        orders (list): List of orders to be processed
        fleet (list): List of available vehicles
        horizon (int): Simulation time horizon
    """
    
    def __init__(self, locations, arcs, orders, fleet, horizon=480):
        """
        Initialize a new Simulator instance.
        
        Args:
            locations (dict): Dictionary of available locations
            arcs (list): List of network arcs/connections
            orders (list): List of orders to be processed
            fleet (list): List of available vehicles
            horizon (int, optional): Simulation time horizon. Defaults to 480.
        """
        self.locations = locations
        self.arcs = arcs
        self.orders = orders
        self.fleet = fleet
        self.horizon = horizon

    def run(self, policy):
        """
        Execute the simulation with a given policy.
        
        Runs the simulation for the specified time horizon, applying
        the routing policy to make decisions for each vehicle at each
        time step.
        
        Args:
            policy: Policy object that defines routing decisions
            
        Returns:
            dict: Simulation results and performance metrics
        """
        current_time = 0
        while current_time < self.horizon:
            for vehicle in self.fleet:
                unloads, loads, next_location = policy.choose_actions(vehicle, current_time)
                
                vehicle.current_location = next_location
                vehicle.available_at = current_time + 30

            current_time += 1
        return self.get_results()

    def get_results(self):
        """
        Collect and return simulation results.
        
        Calculates key performance indicators (KPIs) including
        on-time deliveries, late deliveries, and total delay time.
        
        Returns:
            dict: Dictionary containing simulation KPIs:
                - served_on_time: Number of orders delivered on time
                - served_late: Number of orders delivered late
                - total_late_minutes: Total delay time for late orders
        """
        served_on_time = 0
        served_late = 0
        total_late_minutes = 0
        for order in self.orders:
            if order.delivery_time <= order.due_time:
                served_on_time += 1
            else:
                served_late += 1
                total_late_minutes += (order.delivery_time - order.due_time)

        return {
            'served_on_time': served_on_time,
            'served_late': served_late,
            'total_late_minutes': total_late_minutes
        }
