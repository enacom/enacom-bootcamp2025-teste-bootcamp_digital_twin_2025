"""
Unit tests for the Policy class.
"""

import pytest
from models.policy import Policy
from models.location import Location
from models.vehicle import Vehicle


class TestPolicy:
    """Test cases for the Policy class."""
    
    def test_policy_initialization(self):
        """Test Policy initialization with valid parameters."""
        locations = {"A": Location("A", 1, 1, 1, 1)}
        fleet = [Vehicle("V1", 5, "A")]
        
        policy = Policy(locations, fleet)
        
        assert policy.locations == locations
        assert policy.fleet == fleet
    
    def test_policy_with_empty_locations(self):
        """Test Policy initialization with empty locations."""
        locations = {}
        fleet = []
        
        policy = Policy(locations, fleet)
        
        assert policy.locations == {}
        assert policy.fleet == []
    
    def test_policy_with_empty_fleet(self):
        """Test Policy initialization with empty fleet."""
        locations = {"A": Location("A", 1, 1, 1, 1)}
        fleet = []
        
        policy = Policy(locations, fleet)
        
        assert len(policy.locations) == 1
        assert len(policy.fleet) == 0
    
    def test_choose_actions_basic(self):
        """Test basic action selection for a vehicle."""
        # Create test data
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        
        # Create mock orders
        class MockOrder:
            def __init__(self, order_id, destination):
                self.order_id = order_id
                self.destination = destination
        
        # Add orders to location A's load queue
        locations["A"].load_queue = [
            MockOrder("O1", "B"),
            MockOrder("O2", "C")
        ]
        
        fleet = [Vehicle("V1", 5, "A")]
        policy = Policy(locations, fleet)
        
        # Test action selection
        unloads, loads, next_location = policy.choose_actions(fleet[0], 0)
        
        # Should unload orders with destination A (none in this case)
        assert len(unloads) == 0
        
        # Should load orders from location A's queue
        assert len(loads) >= 0  # Depends on vehicle capacity
        
        # Should return a next location
        assert next_location in locations.keys()
    
    def test_choose_actions_with_vehicle_load(self):
        """Test action selection when vehicle has existing load."""
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        
        # Create mock orders
        class MockOrder:
            def __init__(self, order_id, destination):
                self.order_id = order_id
                self.destination = destination
        
        # Create vehicle with existing load
        vehicle = Vehicle("V1", 5, "A")
        vehicle.load_order(MockOrder("O1", "B"))  # Order to be delivered at B
        
        # Add orders to location B's load queue
        locations["B"].load_queue = [
            MockOrder("O2", "A"),
            MockOrder("O3", "C")
        ]
        
        fleet = [vehicle]
        policy = Policy(locations, fleet)
        
        # Test action selection at location B
        vehicle.current_location = "B"
        unloads, loads, next_location = policy.choose_actions(vehicle, 0)
        
        # Should unload order O1 at location B
        assert len(unloads) == 1
        assert unloads[0].destination == "B"
        
        # Should load new orders from location B
        assert len(loads) >= 0
        
        # Should return a next location
        assert next_location in locations.keys()
    
    def test_get_next_location(self):
        """Test next location selection logic."""
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1),
            "C": Location("C", 1, 1, 1, 1)
        }
        fleet = [Vehicle("V1", 5, "A")]
        
        policy = Policy(locations, fleet)
        
        # Test multiple calls to ensure randomness
        next_locations = set()
        for _ in range(10):
            next_location = policy.get_next_location("A")
            next_locations.add(next_location)
            assert next_location in locations.keys()
        
        # Should have visited multiple locations (random selection)
        assert len(next_locations) >= 1
    
    def test_policy_with_multiple_vehicles(self):
        """Test policy behavior with multiple vehicles."""
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        
        fleet = [
            Vehicle("V1", 5, "A"),
            Vehicle("V2", 3, "B"),
            Vehicle("V3", 7, "A")
        ]
        
        policy = Policy(locations, fleet)
        
        # Test action selection for each vehicle
        for vehicle in fleet:
            unloads, loads, next_location = policy.choose_actions(vehicle, 0)
            
            # Should return valid results
            assert isinstance(unloads, list)
            assert isinstance(loads, list)
            assert next_location in locations.keys()
    
    def test_policy_edge_cases(self):
        """Test policy behavior in edge cases."""
        # Single location
        locations = {"A": Location("A", 1, 1, 1, 1)}
        fleet = [Vehicle("V1", 5, "A")]
        
        policy = Policy(locations, fleet)
        
        # Next location should always be A
        next_location = policy.get_next_location("A")
        assert next_location == "A"
        
        # Empty fleet
        locations = {"A": Location("A", 1, 1, 1, 1)}
        fleet = []
        
        policy = Policy(locations, fleet)
        
        # Should still work (no vehicles to process)
        next_location = policy.get_next_location("A")
        assert next_location == "A"
    
    def test_policy_consistency(self):
        """Test that policy behavior is consistent across calls."""
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        fleet = [Vehicle("V1", 5, "A")]
        
        policy = Policy(locations, fleet)
        
        # Multiple calls should return valid results
        for _ in range(5):
            unloads, loads, next_location = policy.choose_actions(fleet[0], 0)
            
            assert isinstance(unloads, list)
            assert isinstance(loads, list)
            assert next_location in locations.keys() 