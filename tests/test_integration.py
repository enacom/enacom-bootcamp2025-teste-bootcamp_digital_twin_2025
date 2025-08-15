"""
Integration tests for the complete logistics routing system.
"""

import pytest
from models.location import Location
from models.vehicle import Vehicle
from models.order import Order
from models.arc import Arc
from models.policy import Policy
from simulator.simulator import Simulator


class TestSystemIntegration:
    """Integration tests for the complete system."""
    
    def test_complete_workflow_simple(self):
        """Test complete workflow with simple scenario."""
        # Create locations
        locations = {
            "A": Location("A", 2, 1, 1, 1),
            "B": Location("B", 1, 1, 2, 1)
        }
        
        # Create network connections
        arcs = [Arc("A", "B", 30)]
        
        # Create orders
        orders = [
            Order("O1", "A", "B", 0, 100, 1),
            Order("O2", "B", "A", 10, 150, 2)
        ]
        
        # Create fleet
        fleet = [Vehicle("V1", 5, "A")]
        
        # Create policy and simulator
        policy = Policy(locations, fleet)
        simulator = Simulator(locations, arcs, orders, fleet, horizon=100)
        
        # Run simulation
        results = simulator.run(policy)
        
        # Verify results structure
        assert isinstance(results, dict)
        assert 'served_on_time' in results
        assert 'served_late' in results
        assert 'total_late_minutes' in results
        
        # Verify result types
        assert isinstance(results['served_on_time'], int)
        assert isinstance(results['served_late'], int)
        assert isinstance(results['total_late_minutes'], int)
    
    def test_multi_location_network(self):
        """Test system with multiple locations and complex routing."""
        # Create a hub-and-spoke network
        locations = {
            "Hub": Location("Hub", 1, 1, 1, 1),
            "A": Location("A", 2, 1, 1, 1),
            "B": Location("B", 1, 2, 2, 1),
            "C": Location("C", 3, 1, 1, 2)
        }
        
        # Create network connections
        arcs = [
            Arc("Hub", "A", 20),
            Arc("Hub", "B", 25),
            Arc("Hub", "C", 30),
            Arc("A", "Hub", 20),
            Arc("B", "Hub", 25),
            Arc("C", "Hub", 30)
        ]
        
        # Create orders between different locations
        orders = [
            Order("O1", "Hub", "A", 0, 100, 1),
            Order("O2", "A", "Hub", 10, 150, 2),
            Order("O3", "Hub", "B", 20, 200, 1),
            Order("O4", "B", "Hub", 30, 250, 3),
            Order("O5", "Hub", "C", 40, 300, 2)
        ]
        
        # Create fleet with multiple vehicles
        fleet = [
            Vehicle("V1", 5, "Hub"),
            Vehicle("V2", 3, "Hub")
        ]
        
        # Run simulation
        policy = Policy(locations, fleet)
        simulator = Simulator(locations, arcs, orders, fleet, horizon=200)
        results = simulator.run(policy)
        
        # Verify system behavior
        assert isinstance(results, dict)
        assert len(results) == 3
        
        # All results should be non-negative
        for value in results.values():
            assert value >= 0
    
    def test_capacity_constraints(self):
        """Test system behavior under capacity constraints."""
        # Create locations
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        
        # Create network
        arcs = [Arc("A", "B", 30)]
        
        # Create more orders than vehicle capacity
        orders = [
            Order("O1", "A", "B", 0, 100, 1),
            Order("O2", "A", "B", 5, 150, 2),
            Order("O3", "A", "B", 10, 200, 3),
            Order("O4", "A", "B", 15, 250, 1),
            Order("O5", "A", "B", 20, 300, 2)
        ]
        
        # Create vehicle with limited capacity
        fleet = [Vehicle("V1", 3, "A")]  # Can only carry 3 orders
        
        # Run simulation
        policy = Policy(locations, fleet)
        simulator = Simulator(locations, arcs, orders, fleet, horizon=150)
        results = simulator.run(policy)
        
        # Verify results
        assert isinstance(results, dict)
        assert all(key in results for key in ['served_on_time', 'served_late', 'total_late_minutes'])
    
    def test_timing_constraints(self):
        """Test system behavior with strict timing constraints."""
        # Create locations
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        
        # Create network with long transit time
        arcs = [Arc("A", "B", 100)]  # Long transit time
        
        # Create orders with tight deadlines
        orders = [
            Order("O1", "A", "B", 0, 50, 1),   # Impossible to meet deadline
            Order("O2", "A", "B", 0, 200, 1),  # Possible to meet deadline
            Order("O3", "A", "B", 0, 300, 1)   # Easy to meet deadline
        ]
        
        # Create fleet
        fleet = [Vehicle("V1", 5, "A")]
        
        # Run simulation
        policy = Policy(locations, fleet)
        simulator = Simulator(locations, arcs, orders, fleet, horizon=400)
        results = simulator.run(policy)
        
        # Verify results
        assert isinstance(results, dict)
        assert results['served_late'] >= 0
        assert results['total_late_minutes'] >= 0
    
    def test_empty_system(self):
        """Test system behavior with no data."""
        # Empty system
        locations = {}
        arcs = []
        orders = []
        fleet = []
        
        # Run simulation
        policy = Policy(locations, fleet)
        simulator = Simulator(locations, arcs, orders, fleet, horizon=100)
        results = simulator.run(policy)
        
        # Should still return valid results
        assert isinstance(results, dict)
        assert results['served_on_time'] == 0
        assert results['served_late'] == 0
        assert results['total_late_minutes'] == 0
    
    def test_system_consistency(self):
        """Test that system produces consistent results across runs."""
        # Create simple system
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = []
        orders = []
        fleet = []
        
        policy = Policy(locations, fleet)
        simulator = Simulator(locations, arcs, orders, fleet, horizon=50)
        
        # Run multiple times
        results1 = simulator.run(policy)
        results2 = simulator.run(policy)
        results3 = simulator.run(policy)
        
        # Results should have same structure
        assert results1.keys() == results2.keys() == results3.keys()
        
        # All results should be valid
        for results in [results1, results2, results3]:
            assert isinstance(results, dict)
            assert all(key in results for key in ['served_on_time', 'served_late', 'total_late_minutes']) 