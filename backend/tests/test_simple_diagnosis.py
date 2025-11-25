#!/usr/bin/env python3
"""Simple diagnostic tests without external dependencies"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from search_tools import CourseSearchTool, ToolManager, CourseOutlineTool
        print("✓ search_tools imported successfully")
        
        from vector_store import VectorStore, SearchResults
        print("✓ vector_store imported successfully")
        
        from ai_generator import AIGenerator
        print("✓ ai_generator imported successfully")
        
        from rag_system import RAGSystem
        print("✓ rag_system imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_search_tool_definition():
    """Test CourseSearchTool tool definition"""
    try:
        from search_tools import CourseSearchTool
        from unittest.mock import Mock
        
        mock_vector_store = Mock()
        search_tool = CourseSearchTool(mock_vector_store)
        
        tool_def = search_tool.get_tool_definition()
        print(f"Search tool definition: {tool_def}")
        
        # Check required fields
        assert "name" in tool_def
        assert "description" in tool_def
        assert "input_schema" in tool_def
        
        print("✓ CourseSearchTool definition is valid")
        return True
        
    except Exception as e:
        print(f"✗ CourseSearchTool definition test failed: {e}")
        return False

def test_outline_tool_definition():
    """Test CourseOutlineTool tool definition"""
    try:
        from search_tools import CourseOutlineTool
        from unittest.mock import Mock
        
        mock_vector_store = Mock()
        outline_tool = CourseOutlineTool(mock_vector_store)
        
        tool_def = outline_tool.get_tool_definition()
        print(f"Outline tool definition: {tool_def}")
        
        # Check required fields
        assert "name" in tool_def
        assert "description" in tool_def
        assert "input_schema" in tool_def
        
        print("✓ CourseOutlineTool definition is valid")
        return True
        
    except Exception as e:
        print(f"✗ CourseOutlineTool definition test failed: {e}")
        return False

def test_tool_manager():
    """Test ToolManager functionality"""
    try:
        from search_tools import ToolManager, CourseSearchTool, CourseOutlineTool
        from unittest.mock import Mock
        
        mock_vector_store = Mock()
        tool_manager = ToolManager()
        
        # Register tools
        search_tool = CourseSearchTool(mock_vector_store)
        outline_tool = CourseOutlineTool(mock_vector_store)
        
        tool_manager.register_tool(search_tool)
        tool_manager.register_tool(outline_tool)
        
        # Test tool definitions
        tool_defs = tool_manager.get_tool_definitions()
        print(f"Registered tools: {len(tool_defs)}")
        
        for tool_def in tool_defs:
            print(f"  - {tool_def['name']}: {tool_def['description']}")
        
        assert len(tool_defs) == 2
        tool_names = [t['name'] for t in tool_defs]
        assert "search_course_content" in tool_names
        assert "get_course_outline" in tool_names
        
        print("✓ ToolManager working correctly")
        return True
        
    except Exception as e:
        print(f"✗ ToolManager test failed: {e}")
        return False

def test_search_results_class():
    """Test SearchResults class functionality"""
    try:
        from vector_store import SearchResults
        
        # Test normal results
        results = SearchResults(
            documents=["doc1", "doc2"],
            metadata=[{"course": "test1"}, {"course": "test2"}],
            distances=[0.1, 0.2]
        )
        
        assert not results.is_empty()
        assert results.error is None
        
        # Test empty results
        empty_results = SearchResults.empty("No results found")
        assert empty_results.is_empty()
        assert empty_results.error == "No results found"
        
        print("✓ SearchResults class working correctly")
        return True
        
    except Exception as e:
        print(f"✗ SearchResults test failed: {e}")
        return False

def test_mock_search_tool_execution():
    """Test CourseSearchTool execution with mocked vector store"""
    try:
        from search_tools import CourseSearchTool
        from vector_store import SearchResults
        from unittest.mock import Mock
        
        # Create mock vector store
        mock_vector_store = Mock()
        
        # Mock successful search
        mock_results = SearchResults(
            documents=["Test content about MCP"],
            metadata=[{"course_title": "MCP Course", "lesson_number": 1}],
            distances=[0.5]
        )
        mock_vector_store.search.return_value = mock_results
        mock_vector_store.get_lesson_link.return_value = "http://example.com/lesson1"
        
        # Test search tool
        search_tool = CourseSearchTool(mock_vector_store)
        result = search_tool.execute("What is MCP?")
        
        print(f"Search tool result: {result}")
        
        # Verify search was called
        mock_vector_store.search.assert_called_once_with(
            query="What is MCP?",
            course_name=None,
            lesson_number=None
        )
        
        # Check result format
        assert "MCP Course" in result
        assert "Test content about MCP" in result
        
        print("✓ CourseSearchTool execution working correctly")
        return True
        
    except Exception as e:
        print(f"✗ CourseSearchTool execution test failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("=== RAG System Diagnostic Tests ===\n")
    
    tests = [
        test_imports,
        test_search_tool_definition,
        test_outline_tool_definition,
        test_tool_manager,
        test_search_results_class,
        test_mock_search_tool_execution
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
        print("-" * 50)
    
    print(f"\n=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("All basic components are working. Issue likely in:")
        print("1. Vector store data/configuration")
        print("2. AI API integration")
        print("3. Real data processing")
    else:
        print("Found issues in basic components that need fixing.")

if __name__ == '__main__':
    main()