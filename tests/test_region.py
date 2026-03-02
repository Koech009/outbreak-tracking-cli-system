# tests/test_region.py

import unittest
import sys
import os
from typing import Dict, List

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.region import Region
from models.case import Case
from utils.helpers import (
    validate_email, 
    validate_name, 
    validate_age, 
    validate_status,
    validate_region_name,
    get_current_timestamp,
    format_date,
    generate_id
)


class TestRegionClass(unittest.TestCase):
    """Test cases for Region model."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.region_id = generate_id("REG")
        self.region_name = "Test Region"
        self.location = "North District"
        
        # Create a region instance
        self.region = Region(
            region_id=self.region_id,
            name=self.region_name,
            location=self.location
        )
        
        # Create mock cases for testing
        self.case1 = Case(
            case_id="CASE_001",
            patient_name="John Doe",
            age=35,
            location=self.location,
            status="suspected",
            reported_by="user_123"
        )
        
        self.case2 = Case(
            case_id="CASE_002",
            patient_name="Jane Smith",
            age=28,
            location=self.location,
            status="confirmed",
            reported_by="user_456"
        )
    
    def test_region_initialization(self):
        """Test that a region is initialized correctly."""
        self.assertEqual(self.region.id, self.region_id)
        self.assertEqual(self.region.name, self.region_name)
        self.assertEqual(self.region.location, self.location)
        self.assertEqual(len(self.region.cases), 0)
    
    def test_add_case(self):
        """Test adding a case to a region."""
        # Add first case
        result = self.region.add_case(self.case1)
        self.assertTrue(result)
        self.assertEqual(len(self.region.cases), 1)
        self.assertIn(self.case1, self.region.cases)
        
        # Add second case
        self.region.add_case(self.case2)
        self.assertEqual(len(self.region.cases), 2)
    
    def test_add_duplicate_case(self):
        """Test that adding the same case twice doesn't duplicate."""
        self.region.add_case(self.case1)
        self.region.add_case(self.case1)  # Add again
        self.assertEqual(len(self.region.cases), 1)  # Should still be 1
    
    def test_remove_case(self):
        """Test removing a case from a region."""
        self.region.add_case(self.case1)
        self.region.add_case(self.case2)
        self.assertEqual(len(self.region.cases), 2)
        
        # Remove first case
        result = self.region.remove_case(self.case1.id)
        self.assertTrue(result)
        self.assertEqual(len(self.region.cases), 1)
        self.assertNotIn(self.case1, self.region.cases)
        self.assertIn(self.case2, self.region.cases)
    
    def test_remove_nonexistent_case(self):
        """Test removing a case that doesn't exist."""
        result = self.region.remove_case("NONEXISTENT")
        self.assertFalse(result)
        self.assertEqual(len(self.region.cases), 0)
    
    def test_get_case_by_id(self):
        """Test retrieving a case by ID."""
        self.region.add_case(self.case1)
        self.region.add_case(self.case2)
        
        found_case = self.region.get_case_by_id(self.case1.id)
        self.assertEqual(found_case, self.case1)
        
        not_found = self.region.get_case_by_id("FAKE_ID")
        self.assertIsNone(not_found)
    
    def test_get_cases_by_status(self):
        """Test filtering cases by status."""
        self.region.add_case(self.case1)  # suspected
        self.region.add_case(self.case2)  # confirmed
        
        suspected = self.region.get_cases_by_status("suspected")
        self.assertEqual(len(suspected), 1)
        self.assertEqual(suspected[0], self.case1)
        
        confirmed = self.region.get_cases_by_status("confirmed")
        self.assertEqual(len(confirmed), 1)
        self.assertEqual(confirmed[0], self.case2)
        
        recovered = self.region.get_cases_by_status("recovered")
        self.assertEqual(len(recovered), 0)
    
    def test_get_case_count(self):
        """Test getting total case count."""
        self.assertEqual(self.region.get_case_count(), 0)
        
        self.region.add_case(self.case1)
        self.assertEqual(self.region.get_case_count(), 1)
        
        self.region.add_case(self.case2)
        self.assertEqual(self.region.get_case_count(), 2)
    
    def test_get_case_count_by_status(self):
        """Test getting case counts grouped by status."""
        self.region.add_case(self.case1)  # suspected
        self.region.add_case(self.case2)  # confirmed
        
        # Add another confirmed case
        case3 = Case(
            case_id="CASE_003",
            patient_name="Bob Johnson",
            age=45,
            location=self.location,
            status="confirmed",
            reported_by="user_123"
        )
        self.region.add_case(case3)
        
        counts = self.region.get_case_count_by_status()
        self.assertEqual(counts["suspected"], 1)
        self.assertEqual(counts["confirmed"], 2)
        self.assertEqual(counts["recovered"], 0)
        self.assertEqual(counts["deceased"], 0)
    
    def test_to_dict(self):
        """Test conversion to dictionary for JSON serialization."""
        self.region.add_case(self.case1)
        
        data = self.region.to_dict()
        
        self.assertEqual(data["id"], self.region_id)
        self.assertEqual(data["name"], self.region_name)
        self.assertEqual(data["location"], self.location)
        self.assertIsInstance(data["cases"], list)
        self.assertEqual(len(data["cases"]), 1)
        
        # Check that case IDs are stored, not full objects
        self.assertEqual(data["cases"][0], self.case1.id)
    
    def test_str_representation(self):
        """Test string representation of region."""
        self.region.add_case(self.case1)
        
        str_repr = str(self.region)
        self.assertIn(self.region_name, str_repr)
        self.assertIn("1 cases", str_repr)


class TestHelpersWithRegion(unittest.TestCase):
    """Test helper functions in context of region operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.valid_region_name = "North Region"
        self.invalid_region_name = "A"  # Too short
    
    def test_validate_region_name_valid(self):
        """Test validation of valid region names."""
        self.assertTrue(validate_region_name("Main District"))
        self.assertTrue(validate_region_name("North East Region"))
        self.assertTrue(validate_region_name("County of London"))
    
    def test_validate_region_name_invalid(self):
        """Test validation of invalid region names."""
        self.assertFalse(validate_region_name(""))  # Empty
        self.assertFalse(validate_region_name("A"))  # Too short
        self.assertFalse(validate_region_name(None))  # None
        self.assertFalse(validate_region_name(123))  # Not string
    
    def test_generate_id_with_prefix(self):
        """Test ID generation with prefix."""
        region_id = generate_id("REG")
        self.assertTrue(region_id.startswith("REG_"))
        
        case_id = generate_id("CASE")
        self.assertTrue(case_id.startswith("CASE_"))
    
    def test_generate_id_without_prefix(self):
        """Test ID generation without prefix."""
        id_str = generate_id()
        self.assertNotIn("_", id_str[:5])  # First part should be timestamp
        self.assertIn("_", id_str)  # Should have at least one underscore
    
    def test_get_current_timestamp_format(self):
        """Test timestamp format."""
        timestamp = get_current_timestamp()
        # Should match YYYY-MM-DD HH:MM:SS format
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        self.assertRegex(timestamp, pattern)


if __name__ == "__main__":
    unittest.main()