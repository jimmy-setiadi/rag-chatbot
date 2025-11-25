#!/usr/bin/env python3
"""Code analysis tests to identify issues without running the system"""

import sys
import os
import ast
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def analyze_search_tools():
    """Analyze search_tools.py for potential issues"""
    print("=== Analyzing search_tools.py ===")
    
    try:
        with open('../search_tools.py', 'r') as f:
            content = f.read()
        
        # Parse the AST
        tree = ast.parse(content)
        
        # Find class definitions
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        class_names = [cls.name for cls in classes]
        
        print(f"Found classes: {class_names}")
        
        # Check for CourseSearchTool and CourseOutlineTool
        if 'CourseSearchTool' not in class_names:
            print("X CourseSearchTool class not found")
            return False
            
        if 'CourseOutlineTool' not in class_names:
            print("X CourseOutlineTool class not found")
            return False
            
        if 'ToolManager' not in class_names:
            print("X ToolManager class not found")
            return False
        
        print("✓ All required classes found")
        
        # Check for execute methods
        for cls in classes:
            if cls.name in ['CourseSearchTool', 'CourseOutlineTool']:
                methods = [node.name for node in cls.body if isinstance(node, ast.FunctionDef)]
                if 'execute' not in methods:
                    print(f"X {cls.name} missing execute method")
                    return False
                if 'get_tool_definition' not in methods:
                    print(f"X {cls.name} missing get_tool_definition method")
                    return False
        
        print("✓ All required methods found")
        return True
        
    except Exception as e:
        print(f"X Error analyzing search_tools.py: {e}")
        return False

def analyze_ai_generator():
    """Analyze ai_generator.py for potential issues"""
    print("\n=== Analyzing ai_generator.py ===")
    
    try:
        with open('../ai_generator.py', 'r') as f:
            content = f.read()
        
        # Check for tool handling
        if 'tool_use' not in content:
            print("X No tool_use handling found")
            return False
            
        if '_handle_tool_execution' not in content:
            print("X No _handle_tool_execution method found")
            return False
            
        if 'tool_manager' not in content:
            print("X No tool_manager parameter handling found")
            return False
        
        print("✓ Tool handling code found")
        
        # Check system prompt
        if 'SYSTEM_PROMPT' not in content:
            print("X No SYSTEM_PROMPT found")
            return False
            
        # Check for tool-related instructions in prompt
        if 'search_course_content' not in content and 'get_course_outline' not in content:
            print("? System prompt may not mention the tools")
        
        print("✓ AI generator structure looks correct")
        return True
        
    except Exception as e:
        print(f"X Error analyzing ai_generator.py: {e}")
        return False

def analyze_rag_system():
    """Analyze rag_system.py for potential issues"""
    print("\n=== Analyzing rag_system.py ===")
    
    try:
        with open('../rag_system.py', 'r') as f:
            content = f.read()
        
        # Check for tool registration
        if 'register_tool' not in content:
            print("X No tool registration found")
            return False
            
        if 'CourseSearchTool' not in content:
            print("X CourseSearchTool not imported/used")
            return False
            
        if 'CourseOutlineTool' not in content:
            print("X CourseOutlineTool not imported/used")
            return False
        
        # Check query method
        if 'def query(' not in content:
            print("X No query method found")
            return False
            
        # Check if tools are passed to AI generator
        if 'get_tool_definitions' not in content:
            print("X Tools not passed to AI generator")
            return False
            
        if 'tool_manager=' not in content:
            print("X tool_manager not passed to AI generator")
            return False
        
        print("✓ RAG system structure looks correct")
        return True
        
    except Exception as e:
        print(f"X Error analyzing rag_system.py: {e}")
        return False

def check_tool_definitions():
    """Check if tool definitions are properly formatted"""
    print("\n=== Checking Tool Definitions ===")
    
    # Mock the imports to check tool definitions
    try:
        # Read and check CourseSearchTool definition
        with open('../search_tools.py', 'r') as f:
            content = f.read()
        
        # Look for tool definition structure
        if '"name":' not in content:
            print("X Tool definitions missing name field")
            return False
            
        if '"description":' not in content:
            print("X Tool definitions missing description field")
            return False
            
        if '"input_schema":' not in content:
            print("X Tool definitions missing input_schema field")
            return False
        
        # Check for specific tool names
        if 'search_course_content' not in content:
            print("X search_course_content tool name not found")
            return False
            
        if 'get_course_outline' not in content:
            print("X get_course_outline tool name not found")
            return False
        
        print("✓ Tool definitions structure looks correct")
        return True
        
    except Exception as e:
        print(f"X Error checking tool definitions: {e}")
        return False

def analyze_vector_store_integration():
    """Analyze vector store integration"""
    print("\n=== Analyzing Vector Store Integration ===")
    
    try:
        with open('../search_tools.py', 'r') as f:
            search_content = f.read()
            
        with open('../vector_store.py', 'r') as f:
            vector_content = f.read()
        
        # Check if CourseSearchTool uses vector store correctly
        if 'self.store.search(' not in search_content:
            print("X CourseSearchTool doesn't call vector store search")
            return False
            
        # Check if vector store has search method
        if 'def search(' not in vector_content:
            print("X Vector store missing search method")
            return False
            
        # Check SearchResults class
        if 'class SearchResults' not in vector_content:
            print("X SearchResults class not found")
            return False
        
        print("✓ Vector store integration looks correct")
        return True
        
    except Exception as e:
        print(f"X Error analyzing vector store integration: {e}")
        return False

def main():
    """Run all code analysis tests"""
    print("=== RAG System Code Analysis ===")
    
    tests = [
        analyze_search_tools,
        analyze_ai_generator,
        analyze_rag_system,
        check_tool_definitions,
        analyze_vector_store_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Code Analysis Results: {passed}/{total} checks passed ===")
    
    if passed == total:
        print("\nCode structure appears correct. Likely issues:")
        print("1. Missing or empty vector database")
        print("2. API key configuration problems")
        print("3. Runtime dependency issues")
        print("4. Data loading problems")
    else:
        print("\nFound structural issues in the code that need fixing.")
    
    print("\nNext steps:")
    print("1. Check if documents are loaded in vector store")
    print("2. Verify API key configuration")
    print("3. Test with minimal data")

if __name__ == '__main__':
    main()