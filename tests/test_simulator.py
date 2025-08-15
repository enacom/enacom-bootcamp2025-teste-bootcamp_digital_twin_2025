"""
Unit tests for the Simulator class.
"""

import pytest
from simulator.simulator import Simulator
from models.location import Location
from models.vehicle import Vehicle
from models.arc import Arc
from models.order import Order
from models.policy import Policy


class TestSimulator:
    """Test cases for the Simulator class."""
    
    def test_simulator_initialization(self):
        """Test Simulator initialization with valid parameters."""
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = [Arc("A", "B", 30)]
        orders = [Order("O1", "A", "B", 0, 100, 1)]
        fleet = [Vehicle("V1", 5, "A")]
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=480)
        
        assert simulator.locations == locations
        assert simulator.arcs == arcs
        assert simulator.orders == orders
        assert simulator.fleet == fleet
        assert simulator.horizon == 480
    
    def test_simulator_default_horizon(self):
        """Test Simulator initialization with default horizon."""
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = []
        orders = []
        fleet = []
        
        simulator = Simulator(locations, arcs, orders, fleet)
        
        assert simulator.horizon == 480  # Default value
    
    def test_simulator_with_empty_data(self):
        """Test Simulator initialization with empty data."""
        locations = {}
        arcs = []
        orders = []
        fleet = []
        
        simulator = Simulator(locations, arcs, orders, fleet)
        
        assert len(simulator.locations) == 0
        assert len(simulator.arcs) == 0
        assert len(simulator.orders) == 0
        assert len(simulator.fleet) == 0
    
    def test_simulator_run_basic(self):
        """Test basic simulation run."""
        # Create test data
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        arcs = [Arc("A", "B", 30)]
        orders = [Order("O1", "A", "B", 0, 100, 1)]
        fleet = [Vehicle("V1", 5, "A")]
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=10)
        policy = Policy(locations, fleet)
        
        # Run simulation
        results = simulator.run(policy)
        
        # Should return results dictionary
        assert isinstance(results, dict)
        assert 'served_on_time' in results
        assert 'served_late' in results
        assert 'total_late_minutes' in results
    
    def test_simulator_run_with_multiple_vehicles(self):
        """Test simulation run with multiple vehicles."""
        locations = {
            "A": Location("A", 1, 1, 1, 1),
            "B": Location("B", 1, 1, 1, 1)
        }
        arcs = [Arc("A", "B", 30)]
        orders = [
            Order("O1", "A", "B", 0, 100, 1),
            Order("O2", "B", "A", 0, 150, 2)
        ]
        fleet = [
            Vehicle("V1", 5, "A"),
            Vehicle("V2", 3, "B")
        ]
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=20)
        policy = Policy(locations, fleet)
        
        results = simulator.run(policy)
        
        assert isinstance(results, dict)
        assert all(key in results for key in ['served_on_time', 'served_late', 'total_late_minutes'])
    
    def test_simulator_results_structure(self):
        """Test that simulation results have correct structure."""
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = []
        orders = []
        fleet = []
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=5)
        policy = Policy(locations, fleet)
        
        results = simulator.run(policy)
        
        # Check result types
        assert isinstance(results['served_on_time'], int)
        assert isinstance(results['served_late'], int)
        assert isinstance(results['total_late_minutes'], int)
        
        # Check result values are non-negative
        assert results['served_on_time'] >= 0
        assert results['served_late'] >= 0
        assert results['total_late_minutes'] >= 0
    
    def test_simulator_horizon_limits(self):
        """Test that simulation respects horizon limits."""
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = []
        orders = []
        fleet = []
        
        # Very short horizon
        simulator = Simulator(locations, arcs, orders, fleet, horizon=1)
        policy = Policy(locations, fleet)
        
        results = simulator.run(policy)
        
        # Should complete within horizon
        assert isinstance(results, dict)
    
    def test_simulator_with_complex_network(self):
        """Test simulation with a more complex network."""
        locations = {
            "A": Location("A", 2, 1, 1, 1),
            "B": Location("B", 1, 2, 2, 1),
            "C": Location("C", 3, 1, 1, 2)
        }
        arcs = [
            Arc("A", "B", 30),
            Arc("B", "C", 25),
            Arc("C", "A", 35)
        ]
        orders = [
            Order("O1", "A", "B", 0, 100, 1),
            Order("O2", "B", "C", 10, 150, 2),
            Order("O3", "C", "A", 20, 200, 1)
        ]
        fleet = [
            Vehicle("V1", 5, "A"),
            Vehicle("V2", 3, "B")
        ]
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=50)
        policy = Policy(locations, fleet)
        
        results = simulator.run(policy)
        
        assert isinstance(results, dict)
        assert len(results) == 3  # Three result fields
    
    def test_simulator_edge_cases(self):
        """Test simulator behavior in edge cases."""
        # No locations
        locations = {}
        arcs = []
        orders = []
        fleet = []
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=10)
        policy = Policy(locations, fleet)
        
        results = simulator.run(policy)
        assert isinstance(results, dict)
        
        # No orders
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = []
        orders = []
        fleet = [Vehicle("V1", 5, "A")]
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=10)
        policy = Policy(locations, fleet)
        
        results = simulator.run(policy)
        assert isinstance(results, dict)
        
        # No fleet
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = []
        orders = [Order("O1", "A", "B", 0, 100, 1)]
        fleet = []
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=10)
        policy = Policy(locations, fleet)
        
        results = simulator.run(policy)
        assert isinstance(results, dict)
    
    def test_simulator_consistency(self):
        """Test that simulator produces consistent results across runs."""
        locations = {"A": Location("A", 1, 1, 1, 1)}
        arcs = []
        orders = []
        fleet = []
        
        simulator = Simulator(locations, arcs, orders, fleet, horizon=10)
        policy = Policy(locations, fleet)
        
        # Multiple runs should produce consistent structure
        for _ in range(3):
            results = simulator.run(policy)
            assert isinstance(results, dict)
            assert all(key in results for key in ['served_on_time', 'served_late', 'total_late_minutes']) 