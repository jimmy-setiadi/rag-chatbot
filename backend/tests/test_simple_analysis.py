#!/usr/bin/env python3
"""Simple code analysis without Unicode characters"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_search_tools():
    """Check search_tools.py structure"""
    print("=== Checking search_tools.py ===")
    
    try:
        with open('../search_tools.py', 'r') as f:
            content = f.read()
        
        issues = []
        
        # Check for required classes
        if 'class CourseSearchTool' not in content:
            issues.append("CourseSearchTool class missing")
        else:
            print("OK: CourseSearchTool class found")
            
        if 'class CourseOutlineTool' not in content:
            issues.append("CourseOutlineTool class missing")
        else:
            print("OK: CourseOutlineTool class found")
            
        if 'class ToolManager' not in content:
            issues.append("ToolManager class missing")
        else:
            print("OK: ToolManager class found")
        
        # Check for execute methods
        if 'def execute(' not in content:
            issues.append("execute method missing")
        else:
            print("OK: execute method found")
            
        # Check tool names
        if 'search_course_content' not in content:
            issues.append("search_course_content tool name missing")
        else:
            print("OK: search_course_content tool name found")
            
        if 'get_course_outline' not in content:
            issues.append("get_course_outline tool name missing")
        else:
            print("OK: get_course_outline tool name found")
        
        if issues:
            print("ISSUES FOUND:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("PASS: search_tools.py structure is correct")
            return True
            
    except Exception as e:
        print(f"ERROR: Could not analyze search_tools.py: {e}")
        return False

def check_ai_generator():
    """Check ai_generator.py structure"""
    print("\n=== Checking ai_generator.py ===")
    
    try:
        with open('../ai_generator.py', 'r') as f:
            content = f.read()
        
        issues = []
        
        # Check for tool handling
        if 'tool_use' not in content:
            issues.append("No tool_use handling found")
        else:
            print("OK: tool_use handling found")
            
        if '_handle_tool_execution' not in content:
            issues.append("_handle_tool_execution method missing")
        else:
            print("OK: _handle_tool_execution method found")
            
        if 'tool_manager' not in content:
            issues.append("tool_manager parameter not handled")
        else:
            print("OK: tool_manager parameter found")
        
        # Check system prompt mentions tools
        if 'search_course_content' not in content or 'get_course_outline' not in content:
            issues.append("System prompt may not mention both tools")
        else:
            print("OK: Both tools mentioned in system prompt")
        
        if issues:
            print("ISSUES FOUND:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("PASS: ai_generator.py structure is correct")
            return True
            
    except Exception as e:
        print(f"ERROR: Could not analyze ai_generator.py: {e}")
        return False

def check_rag_system():
    """Check rag_system.py structure"""
    print("\n=== Checking rag_system.py ===")
    
    try:
        with open('../rag_system.py', 'r') as f:
            content = f.read()
        
        issues = []
        
        # Check imports
        if 'CourseSearchTool' not in content:
            issues.append("CourseSearchTool not imported")
        else:
            print("OK: CourseSearchTool imported")
            
        if 'CourseOutlineTool' not in content:
            issues.append("CourseOutlineTool not imported")
        else:
            print("OK: CourseOutlineTool imported")
        
        # Check tool registration
        if 'register_tool(self.search_tool)' not in content:
            issues.append("search_tool not registered")
        else:
            print("OK: search_tool registered")
            
        if 'register_tool(self.outline_tool)' not in content:
            issues.append("outline_tool not registered")
        else:
            print("OK: outline_tool registered")
        
        # Check query method passes tools
        if 'get_tool_definitions()' not in content:
            issues.append("Tools not passed to AI generator")
        else:
            print("OK: Tools passed to AI generator")
            
        if 'tool_manager=' not in content:
            issues.append("tool_manager not passed to AI generator")
        else:
            print("OK: tool_manager passed to AI generator")
        
        if issues:
            print("ISSUES FOUND:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("PASS: rag_system.py structure is correct")
            return True
            
    except Exception as e:
        print(f"ERROR: Could not analyze rag_system.py: {e}")
        return False

def check_vector_store():
    """Check vector_store.py structure"""
    print("\n=== Checking vector_store.py ===")
    
    try:
        with open('../vector_store.py', 'r') as f:
            content = f.read()
        
        issues = []
        
        # Check for search method
        if 'def search(' not in content:
            issues.append("search method missing")
        else:
            print("OK: search method found")
            
        # Check SearchResults class
        if 'class SearchResults' not in content:
            issues.append("SearchResults class missing")
        else:
            print("OK: SearchResults class found")
            
        # Check error handling
        if 'error=' not in content:
            issues.append("Error handling may be missing")
        else:
            print("OK: Error handling found")
        
        if issues:
            print("ISSUES FOUND:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("PASS: vector_store.py structure is correct")
            return True
            
    except Exception as e:
        print(f"ERROR: Could not analyze vector_store.py: {e}")
        return False

def main():
    """Run all checks"""
    print("=== RAG System Structure Analysis ===")
    
    checks = [
        check_search_tools,
        check_ai_generator,
        check_rag_system,
        check_vector_store
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
    
    print(f"\n=== Results: {passed}/{total} components passed ===")
    
    if passed == total:
        print("\nCode structure is correct. The 'query failed' issue is likely:")
        print("1. Empty or missing vector database")
        print("2. API configuration problems")
        print("3. Missing course documents")
        print("4. Runtime errors in tool execution")
        
        print("\nRecommended fixes:")
        print("1. Check if documents are loaded: vector_store.get_course_count()")
        print("2. Verify API key is set in .env file")
        print("3. Add error logging to tool execution")
        print("4. Test with mock data first")
    else:
        print("\nStructural issues found that need fixing first.")

if __name__ == '__main__':
    main()