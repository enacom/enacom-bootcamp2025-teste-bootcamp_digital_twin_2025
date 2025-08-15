"""
Unit tests for the Order class.
"""

import pytest
from models.order import Order


class TestOrder:
    """Test cases for the Order class."""
    
    def test_order_initialization(self):
        """Test Order initialization with valid parameters."""
        order = Order("O001", "A", "B", 0, 100, 5)
        
        assert order.order_id == "O001"
        assert order.origin == "A"
        assert order.destination == "B"
        assert order.release_time == 0
        assert order.due_time == 100
        assert order.units == 5
        assert order.delivery_time == 0
    
    def test_string_representation(self):
        """Test the string representation of an order."""
        order = Order("O002", "C", "D", 10, 200, 3)
        
        expected_str = "Order O002: C -> D, 3 units"
        assert str(order) == "Order O002: C -> D, 3 units"
    
    def test_order_with_zero_values(self):
        """Test order creation with zero values for time and units."""
        order = Order("O003", "E", "F", 0, 0, 0)
        
        assert order.release_time == 0
        assert order.due_time == 0
        assert order.units == 0
        assert order.delivery_time == 0
    
    def test_order_with_negative_times(self):
        """Test order creation with negative time values."""
        order = Order("O004", "G", "H", -10, -5, 2)
        
        assert order.release_time == -10
        assert order.due_time == -5
        assert order.units == 2
    
    def test_order_with_large_values(self):
        """Test order creation with large values."""
        large_release = 1000000
        large_due = 2000000
        large_units = 50000
        
        order = Order("O005", "I", "J", large_release, large_due, large_units)
        
        assert order.release_time == large_release
        assert order.due_time == large_due
        assert order.units == large_units
    
    def test_order_attributes_modification(self):
        """Test that order attributes can be modified after creation."""
        order = Order("O006", "K", "L", 50, 150, 4)
        
        # Initially None
        assert order.delivery_time == 0
        
        # Set delivery time
        order.delivery_time = 120
        assert order.delivery_time == 120
        
        # Modify other attributes
        order.units = 6
        assert order.units == 6
    
    def test_multiple_orders(self):
        """Test creation and comparison of multiple orders."""
        order1 = Order("O007", "M", "N", 0, 100, 1)
        order2 = Order("O008", "M", "N", 0, 100, 1)
        order3 = Order("O009", "P", "Q", 20, 120, 2)
        
        # Different orders should have different IDs
        assert order1.order_id != order2.order_id
        assert order1.order_id != order3.order_id
        
        # Same origin and destination
        assert order1.origin == order2.origin
        assert order1.destination == order2.destination
        
        # Different units
        assert order1.units != order3.units
    
    def test_order_edge_cases(self):
        """Test edge cases for order creation."""
        # Empty strings for locations
        order = Order("O010", "", "", 0, 100, 1)
        assert order.origin == ""
        assert order.destination == ""
        
        # Very long order ID
        long_id = "A" * 1000
        order = Order(long_id, "X", "Y", 0, 100, 1)
        assert order.order_id == long_id
        
        # Zero units
        order = Order("O011", "Z", "W", 0, 100, 0)
        assert order.units == 0
    
    def test_order_timing_constraints(self):
        """Test various timing constraint scenarios."""
        # Order available immediately
        order1 = Order("O012", "A", "B", 0, 100, 1)
        assert order1.release_time == 0
        
        # Order with delay
        order2 = Order("O013", "C", "D", 30, 150, 2)
        assert order2.release_time == 30
        
        # Order with tight deadline
        order3 = Order("O014", "E", "F", 0, 10, 1)
        assert order3.due_time == 10
        
        # Order with long deadline
        order4 = Order("O015", "G", "H", 0, 1000, 1)
        assert order4.due_time == 1000 