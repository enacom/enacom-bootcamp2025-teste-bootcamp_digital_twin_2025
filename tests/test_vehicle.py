"""
Unit tests for the Vehicle class.
"""

import pytest
from models.vehicle import Vehicle
from models.location import Location
from models.order import Order

class TestVehicle:
    """Test cases for the Vehicle class."""
    
    def test_vehicle_initialization(self):
        """Test Vehicle initialization with valid parameters."""
        vehicle = Vehicle("V001", 5, "A")
        
        assert vehicle.vehicle_id == "V001"
        assert vehicle.capacity == 5
        assert vehicle.current_location == "A"
        assert vehicle.load == []
        assert vehicle.available_at == 0
    
    def test_string_representation(self):
        """Test the string representation of a vehicle."""
        vehicle = Vehicle("V002", 10, "B")
        
        expected_str = "Vehicle V002 at B"
        assert str(vehicle) == expected_str
    
    def test_load_order_success(self):
        """Test successful order loading when capacity is available."""
        vehicle = Vehicle("V003", 3, "C")
        
        # Load orders up to capacity
        assert vehicle.load_order("order1") == True
        assert vehicle.load_order("order2") == True
        assert vehicle.load_order("order3") == True
        
        assert len(vehicle.load) == 3
        assert "order1" in vehicle.load
        assert "order2" in vehicle.load
        assert "order3" in vehicle.load
    
    def test_load_order_capacity_exceeded(self):
        """Test order loading when capacity is exceeded."""
        vehicle = Vehicle("V004", 2, "D")
        
        # Load up to capacity
        assert vehicle.load_order("order1") == True
        assert vehicle.load_order("order2") == True
        
        # Try to load beyond capacity
        assert vehicle.load_order("order3") == False
        
        assert len(vehicle.load) == 2
        assert "order1" in vehicle.load
        assert "order2" in vehicle.load
        assert "order3" not in vehicle.load
    
    def test_unload_orders(self):
        """Test unloading orders at a specific location."""
        # Create a mock location
        location = Location("A", 1, 1, 1, 1)
        
        # Create a mock order with destination
        class MockOrder:
            def __init__(self, order_id, destination):
                self.order_id = order_id
                self.destination = destination
        
        order1 = MockOrder("O1", "A")
        order2 = MockOrder("O2", "B")
        order3 = MockOrder("O3", "A")
        
        vehicle = Vehicle("V005", 5, "A")
        vehicle.load_order(order1)
        vehicle.load_order(order2)
        vehicle.load_order(order3)
        
        # Unload orders at location A
        unloaded = vehicle.unload(location)
        
        # Should unload orders with destination A
        assert len(unloaded) == 2
        assert order1 in unloaded
        assert order3 in unloaded
        assert order2 not in unloaded
        
        # Vehicle should only have order2 remaining
        assert len(vehicle.load) == 1
        assert order2 in vehicle.load
    
    def test_unload_empty_vehicle(self):
        """Test unloading from an empty vehicle."""
        location = Location("B", 1, 1, 1, 1)
        vehicle = Vehicle("V006", 5, "B")
        
        unloaded = vehicle.load_order(Order("order1", "A", "B", 0, 100, 1))
        assert unloaded == True
        
        # Unload all orders
        unloaded_orders = vehicle.unload(location)
        assert len(unloaded_orders) == 1
        
        # Try to unload from empty vehicle
        unloaded_orders = vehicle.unload(location)
        assert len(unloaded_orders) == 0
        assert len(vehicle.load) == 0
    
    def test_edge_cases(self):
        """Test edge cases for vehicle operations."""
        # Zero capacity vehicle
        vehicle = Vehicle("V007", 0, "C")
        assert vehicle.load_order("order1") == False
        assert len(vehicle.load) == 0
        
        # Single capacity vehicle
        vehicle = Vehicle("V008", 1, "D")
        assert vehicle.load_order("order1") == True
        assert vehicle.load_order("order2") == False
        assert len(vehicle.load) == 1
    
    def test_multiple_operations(self):
        """Test multiple load/unload operations in sequence."""
        vehicle = Vehicle("V009", 4, "E")
        location = Location("E", 1, 1, 1, 1)
        
        # Load multiple orders
        vehicle.load_order(Order("order1", "E", "A", 0, 100, 1))
        vehicle.load_order(Order("order2", "E", "A", 0, 100, 1))
        
        # Unload some orders
        unloaded = vehicle.unload(location)
        assert len(unloaded) == 0  # No orders with destination E
        
        # Load more orders
        vehicle.load_order(Order("order3", "E", "A", 0, 100, 1))
        vehicle.load_order(Order("order4", "E", "A", 0, 100, 1))
        
        # Check final state
        assert len(vehicle.load) == 4  # Should exceed capacity, but we're not enforcing it strictly 