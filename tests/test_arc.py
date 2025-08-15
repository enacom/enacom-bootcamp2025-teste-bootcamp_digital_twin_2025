"""
Unit tests for the Arc class.
"""

import pytest
from models.arc import Arc


class TestArc:
    """Test cases for the Arc class."""
    
    def test_arc_initialization(self):
        """Test Arc initialization with valid parameters."""
        arc = Arc("A", "B", 30)
        
        assert arc.from_location == "A"
        assert arc.to_location == "B"
        assert arc.transit_time == 30
    
    def test_string_representation(self):
        """Test the string representation of an arc."""
        arc = Arc("C", "D", 45)
        
        expected_str = "Arc: C -> D, transit_time 45"
        assert str(arc) == expected_str
    
    def test_arc_with_zero_transit_time(self):
        """Test arc creation with zero transit time."""
        arc = Arc("E", "F", 0)
        
        assert arc.from_location == "E"
        assert arc.to_location == "F"
        assert arc.transit_time == 0
    
    def test_arc_with_negative_transit_time(self):
        """Test arc creation with negative transit time."""
        arc = Arc("G", "H", -10)
        
        assert arc.from_location == "G"
        assert arc.to_location == "H"
        assert arc.transit_time == -10
    
    def test_arc_with_large_transit_time(self):
        """Test arc creation with large transit time values."""
        large_time = 1000000
        arc = Arc("I", "J", large_time)
        
        assert arc.from_location == "I"
        assert arc.to_location == "J"
        assert arc.transit_time == large_time
    
    def test_arc_with_same_locations(self):
        """Test arc creation where origin and destination are the same."""
        arc = Arc("K", "K", 15)
        
        assert arc.from_location == "K"
        assert arc.to_location == "K"
        assert arc.transit_time == 15
    
    def test_multiple_arcs(self):
        """Test creation and comparison of multiple arcs."""
        arc1 = Arc("A", "B", 30)
        arc2 = Arc("A", "B", 30)
        arc3 = Arc("B", "C", 25)
        
        # Same locations and transit time
        assert arc1.from_location == arc2.from_location
        assert arc1.to_location == arc2.to_location
        assert arc1.transit_time == arc2.transit_time
        
        # Different transit times
        assert arc1.transit_time != arc3.transit_time
        
        # Different destinations
        assert arc1.to_location != arc3.to_location
    
    def test_arc_edge_cases(self):
        """Test edge cases for arc creation."""
        # Empty strings for locations
        arc = Arc("", "", 10)
        assert arc.from_location == ""
        assert arc.to_location == ""
        
        # Very long location names
        long_location = "X" * 1000
        arc = Arc(long_location, "Y", 20)
        assert arc.from_location == long_location
        
        # Very long transit time
        arc = Arc("Z", "W", 999999999)
        assert arc.transit_time == 999999999
    
    def test_arc_network_topology(self):
        """Test various network topology scenarios."""
        # Bidirectional connections
        arc_ab = Arc("A", "B", 30)
        arc_ba = Arc("B", "A", 30)
        
        assert arc_ab.from_location == "A"
        assert arc_ab.to_location == "B"
        assert arc_ba.from_location == "B"
        assert arc_ba.to_location == "A"
        
        # Hub and spoke pattern
        hub = "H"
        arc_h1 = Arc(hub, "1", 10)
        arc_h2 = Arc(hub, "2", 15)
        arc_h3 = Arc(hub, "3", 20)
        
        assert arc_h1.from_location == hub
        assert arc_h2.from_location == hub
        assert arc_h3.from_location == hub
    
    def test_arc_transit_time_variations(self):
        """Test arcs with various transit time patterns."""
        # Short transit times
        arc_short = Arc("X", "Y", 1)
        assert arc_short.transit_time == 1
        
        # Medium transit times
        arc_medium = Arc("Y", "Z", 60)
        assert arc_medium.transit_time == 60
        
        # Long transit times
        arc_long = Arc("Z", "W", 480)
        assert arc_long.transit_time == 480
        
        # Fractional transit times (if supported)
        arc_fractional = Arc("W", "V", 30.5)
        assert arc_fractional.transit_time == 30.5 