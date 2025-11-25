#!/usr/bin/env python3
"""Tests for AIGenerator tool calling functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import Mock, patch, MagicMock
from ai_generator import AIGenerator
from search_tools import ToolManager, CourseSearchTool

class TestAIGeneratorToolCalling(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_key"
        self.model = "claude-3-sonnet-20240229"
        
        # Mock the anthropic client
        self.mock_client = Mock()
        self.ai_generator = AIGenerator(self.api_key, self.model)
        self.ai_generator.client = self.mock_client
        
        # Set up tool manager
        self.tool_manager = Mock(spec=ToolManager)
        self.search_tool = Mock(spec=CourseSearchTool)
    
    def test_generate_response_without_tools(self):
        """Test response generation without tools"""
        # Mock Claude response
        mock_response = Mock()
        mock_response.stop_reason = "end_turn"
        mock_response.content = [Mock(text="Test response")]
        self.mock_client.messages.create.return_value = mock_response
        
        result = self.ai_generator.generate_response("What is Python?")
        
        self.assertEqual(result, "Test response")
        self.mock_client.messages.create.assert_called_once()
    
    def test_generate_response_with_tool_use(self):
        """Test response generation that triggers tool use"""
        # Mock initial response with tool use
        mock_tool_block = Mock()
        mock_tool_block.type = "tool_use"
        mock_tool_block.name = "search_course_content"
        mock_tool_block.id = "tool_123"
        mock_tool_block.input = {"query": "What is MCP?"}
        
        mock_initial_response = Mock()
        mock_initial_response.stop_reason = "tool_use"
        mock_initial_response.content = [mock_tool_block]
        
        # Mock final response after tool execution
        mock_final_response = Mock()
        mock_final_response.content = [Mock(text="Final answer based on search")]
        
        self.mock_client.messages.create.side_effect = [
            mock_initial_response,
            mock_final_response
        ]
        
        # Mock tool manager
        self.tool_manager.execute_tool.return_value = "Search results about MCP"
        
        tools = [{"name": "search_course_content", "description": "Search tool"}]
        
        result = self.ai_generator.generate_response(
            "What is MCP?",
            tools=tools,
            tool_manager=self.tool_manager
        )
        
        # Verify tool was executed
        self.tool_manager.execute_tool.assert_called_once_with(
            "search_course_content",
            query="What is MCP?"
        )
        
        # Verify final response
        self.assertEqual(result, "Final answer based on search")
        
        # Verify two API calls were made
        self.assertEqual(self.mock_client.messages.create.call_count, 2)
    
    def test_tool_execution_error_handling(self):
        """Test handling of tool execution errors"""
        mock_tool_block = Mock()
        mock_tool_block.type = "tool_use"
        mock_tool_block.name = "nonexistent_tool"
        mock_tool_block.id = "tool_456"
        mock_tool_block.input = {"query": "test"}
        
        mock_initial_response = Mock()
        mock_initial_response.stop_reason = "tool_use"
        mock_initial_response.content = [mock_tool_block]
        
        mock_final_response = Mock()
        mock_final_response.content = [Mock(text="Error response")]
        
        self.mock_client.messages.create.side_effect = [
            mock_initial_response,
            mock_final_response
        ]
        
        # Mock tool manager returning error
        self.tool_manager.execute_tool.return_value = "Tool 'nonexistent_tool' not found"
        
        tools = [{"name": "search_course_content", "description": "Search tool"}]
        
        result = self.ai_generator.generate_response(
            "test query",
            tools=tools,
            tool_manager=self.tool_manager
        )
        
        self.assertEqual(result, "Error response")

if __name__ == '__main__':
    unittest.main()