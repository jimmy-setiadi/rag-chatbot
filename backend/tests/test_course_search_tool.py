#!/usr/bin/env python3
"""Tests for CourseSearchTool execute method"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import Mock, patch
from config import config
from vector_store import VectorStore, SearchResults
from search_tools import CourseSearchTool

class TestCourseSearchTool(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.vector_store = Mock(spec=VectorStore)
        self.search_tool = CourseSearchTool(self.vector_store)
    
    def test_execute_basic_query(self):
        """Test basic query execution"""
        # Mock search results
        mock_results = SearchResults(
            documents=["Test content about MCP"],
            metadata=[{"course_title": "MCP Course", "lesson_number": 1}],
            distances=[0.5]
        )
        self.vector_store.search.return_value = mock_results
        self.vector_store.get_lesson_link.return_value = "http://example.com/lesson1"
        
        result = self.search_tool.execute("What is MCP?")
        
        # Verify search was called
        self.vector_store.search.assert_called_once_with(
            query="What is MCP?",
            course_name=None,
            lesson_number=None
        )
        
        # Verify result format
        self.assertIn("MCP Course", result)
        self.assertIn("Test content about MCP", result)
    
    def test_execute_with_course_filter(self):
        """Test query with course name filter"""
        mock_results = SearchResults(
            documents=["Course content"],
            metadata=[{"course_title": "Specific Course", "lesson_number": 2}],
            distances=[0.3]
        )
        self.vector_store.search.return_value = mock_results
        
        result = self.search_tool.execute("test query", course_name="Specific Course")
        
        self.vector_store.search.assert_called_once_with(
            query="test query",
            course_name="Specific Course",
            lesson_number=None
        )
    
    def test_execute_error_handling(self):
        """Test error handling in execute method"""
        # Mock error result
        error_results = SearchResults(
            documents=[],
            metadata=[],
            distances=[],
            error="Search failed"
        )
        self.vector_store.search.return_value = error_results
        
        result = self.search_tool.execute("test query")
        
        self.assertEqual(result, "Search failed")
    
    def test_execute_empty_results(self):
        """Test handling of empty search results"""
        empty_results = SearchResults(
            documents=[],
            metadata=[],
            distances=[]
        )
        self.vector_store.search.return_value = empty_results
        
        result = self.search_tool.execute("nonexistent query")
        
        self.assertIn("No relevant content found", result)

if __name__ == '__main__':
    unittest.main()