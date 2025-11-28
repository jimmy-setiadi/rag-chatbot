#!/usr/bin/env python3
"""Real system tests to identify actual failures"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from config import config
from rag_system import RAGSystem
from vector_store import VectorStore
from search_tools import CourseSearchTool, ToolManager

class TestRealSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up with real components"""
        try:
            self.vector_store = VectorStore(config.CHROMA_PATH, config.EMBEDDING_MODEL)
            self.search_tool = CourseSearchTool(self.vector_store)
            self.tool_manager = ToolManager()
            self.tool_manager.register_tool(self.search_tool)
        except Exception as e:
            self.skipTest(f"Could not initialize components: {e}")
    
    def test_vector_store_basic_functionality(self):
        """Test if vector store is working"""
        try:
            # Test basic search
            results = self.vector_store.search("test query", limit=1)
            print(f"Vector store search results: {results}")
            
            # Check if we have any courses
            course_count = self.vector_store.get_course_count()
            print(f"Course count: {course_count}")
            
            course_titles = self.vector_store.get_existing_course_titles()
            print(f"Course titles: {course_titles}")
            
            self.assertIsNotNone(results)
            
        except Exception as e:
            self.fail(f"Vector store test failed: {e}")
    
    def test_search_tool_execution(self):
        """Test CourseSearchTool execute method with real data"""
        try:
            # Test basic search
            result = self.search_tool.execute("What is MCP?")
            print(f"Search tool result: {result}")
            
            # Test if result is not an error
            self.assertNotIn("Search error", result)
            self.assertNotIn("query failed", result.lower())
            
        except Exception as e:
            self.fail(f"Search tool test failed: {e}")
    
    def test_tool_manager_functionality(self):
        """Test ToolManager with real tools"""
        try:
            # Get tool definitions
            tool_defs = self.tool_manager.get_tool_definitions()
            print(f"Tool definitions: {tool_defs}")
            
            self.assertGreater(len(tool_defs), 0)
            
            # Test tool execution
            result = self.tool_manager.execute_tool("search_course_content", query="test")
            print(f"Tool manager execution result: {result}")
            
            self.assertIsNotNone(result)
            
        except Exception as e:
            self.fail(f"Tool manager test failed: {e}")
    
    def test_rag_system_query(self):
        """Test full RAG system query with mock AI to isolate issues"""
        try:
            # Create RAG system but mock the AI part to isolate vector/tool issues
            from unittest.mock import Mock, patch
            
            with patch('rag_system.AIGenerator') as mock_ai_class:
                mock_ai = Mock()
                mock_ai.generate_response.return_value = "Mock AI response"
                mock_ai_class.return_value = mock_ai
                
                rag_system = RAGSystem(config)
                
                # Test query execution
                response, sources = rag_system.query("What is MCP?")
                print(f"RAG system response: {response}")
                print(f"RAG system sources: {sources}")
                
                # Verify AI was called with tools
                mock_ai.generate_response.assert_called_once()
                call_args = mock_ai.generate_response.call_args
                
                print(f"AI generator call args: {call_args}")
                
                # Check if tools were passed
                self.assertIn('tools', call_args[1])
                self.assertIn('tool_manager', call_args[1])
                
        except Exception as e:
            self.fail(f"RAG system test failed: {e}")

if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)