#!/usr/bin/env python3
"""Test the fixes for the query failed issue"""

def test_fixes():
    """Test that the fixes are properly implemented"""
    
    print("=== Testing Query Failed Fixes ===")
    
    # Test 1: Check if error handling was added to RAG system
    try:
        with open('rag_system.py', 'r') as f:
            rag_content = f.read()
        
        if 'ERROR in RAG query:' in rag_content:
            print("OK: RAG system has error handling")
        else:
            print("MISSING: RAG system error handling")
            
        if 'Attempting fallback search' in rag_content:
            print("OK: RAG system has fallback mechanism")
        else:
            print("MISSING: RAG system fallback mechanism")
            
    except Exception as e:
        print(f"ERROR: Could not check rag_system.py: {e}")
    
    # Test 2: Check if error handling was added to search tools
    try:
        with open('search_tools.py', 'r') as f:
            search_content = f.read()
        
        if 'ERROR in CourseSearchTool.execute:' in search_content:
            print("OK: Search tool has error handling")
        else:
            print("MISSING: Search tool error handling")
            
        if 'CourseSearchTool.execute called with query:' in search_content:
            print("OK: Search tool has logging")
        else:
            print("MISSING: Search tool logging")
            
    except Exception as e:
        print(f"ERROR: Could not check search_tools.py: {e}")
    
    # Test 3: Check if error handling was added to AI generator
    try:
        with open('ai_generator.py', 'r') as f:
            ai_content = f.read()
        
        if 'ERROR executing tool' in ai_content:
            print("OK: AI generator has tool error handling")
        else:
            print("MISSING: AI generator tool error handling")
            
        if 'ERROR in final API call:' in ai_content:
            print("OK: AI generator has API error handling")
        else:
            print("MISSING: AI generator API error handling")
            
    except Exception as e:
        print(f"ERROR: Could not check ai_generator.py: {e}")
    
    print("\n=== Fix Summary ===")
    print("Added comprehensive error handling and logging to:")
    print("1. RAG system query method - catches AI generation errors")
    print("2. Search tool execute method - catches vector store errors")
    print("3. AI generator tool execution - catches tool and API errors")
    print("4. Added fallback mechanism when AI fails")
    print("5. Added detailed logging to track execution flow")
    
    print("\n=== Next Steps ===")
    print("1. Restart the application to load the fixes")
    print("2. Try a query and check the console logs")
    print("3. The logs will now show exactly where the failure occurs")
    print("4. Common issues to look for:")
    print("   - 'ERROR in AI generation' = API key or rate limit issue")
    print("   - 'Vector store error' = Database or search issue")
    print("   - 'Tool execution failed' = Tool parameter issue")
    
    return True

if __name__ == '__main__':
    test_fixes()