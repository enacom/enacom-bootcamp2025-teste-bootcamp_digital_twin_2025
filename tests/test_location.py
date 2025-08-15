"""
Unit tests for the Location class.
"""

import pytest
from models.location import Location


class TestLocation:
    """Test cases for the Location class."""
    
    def test_location_initialization(self):
        """Test Location initialization with valid parameters."""
        location = Location("A", 3, 1, 2, 1)
        
        assert location.location_id == "A"
        assert location.base_load == 3
        assert location.gamma == 1
        assert location.base_unload == 2
        assert location.delta == 1
        assert location.load_queue == []
        assert location.unload_queue == []
    
    def test_load_time_calculation(self):
        """Test load time calculation with different unit amounts."""
        location = Location("B", 5, 2, 3, 1)
        
        # Base load time
        assert location.load_time(0) == 5
        
        # Load time with units
        assert location.load_time(1) == 7  # 5 + 2*1
        assert location.load_time(3) == 11  # 5 + 2*3
        assert location.load_time(10) == 25  # 5 + 2*10
    
    def test_unload_time_calculation(self):
        """Test unload time calculation with different unit amounts."""
        location = Location("C", 2, 1, 4, 3)
        
        # Base unload time
        assert location.unload_time(0) == 4
        
        # Unload time with units
        assert location.unload_time(1) == 7  # 4 + 3*1
        assert location.unload_time(2) == 10  # 4 + 3*2
        assert location.unload_time(5) == 19  # 4 + 3*5
    
    def test_queue_operations(self):
        """Test that load and unload queues can be modified."""
        location = Location("D", 1, 1, 1, 1)
        
        # Initially empty
        assert len(location.load_queue) == 0
        assert len(location.unload_queue) == 0
        
        # Add items to queues
        location.load_queue.append("order1")
        location.unload_queue.append("order2")
        
        assert len(location.load_queue) == 1
        assert len(location.unload_queue) == 1
        assert location.load_queue[0] == "order1"
        assert location.unload_queue[0] == "order2"
    
    def test_edge_cases(self):
        """Test edge cases for time calculations."""
        location = Location("E", 0, 0, 0, 0)
        
        # Zero parameters
        assert location.load_time(5) == 0
        assert location.unload_time(5) == 0
        
        # Negative units (should work but may not be realistic)
        location2 = Location("F", 10, 2, 5, 1)
        assert location2.load_time(-2) == 6  # 10 + 2*(-2)
        assert location2.unload_time(-1) == 4  # 5 + 1*(-1)
    
    def test_large_numbers(self):
        """Test with large numbers to ensure no overflow issues."""
        location = Location("G", 1000, 100, 2000, 200)
        
        large_units = 10000
        expected_load = 1000 + 100 * large_units
        expected_unload = 2000 + 200 * large_units
        
        assert location.load_time(large_units) == expected_load
        assert location.unload_time(large_units) == expected_unload 