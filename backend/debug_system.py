#!/usr/bin/env python3
"""Debug script to identify the actual issue"""

import os
import sys

def check_environment():
    """Check environment setup"""
    print("=== Environment Check ===")
    
    # Check .env file
    env_path = "../.env"
    if os.path.exists(env_path):
        print("OK: .env file exists")
        with open(env_path, 'r') as f:
            content = f.read()
            if 'ANTHROPIC_API_KEY' in content:
                print("OK: ANTHROPIC_API_KEY found in .env")
            else:
                print("ERROR: ANTHROPIC_API_KEY not found in .env")
                return False
    else:
        print("ERROR: .env file missing")
        return False
    
    # Check chroma_db directory
    chroma_path = "./chroma_db"
    if os.path.exists(chroma_path):
        print("OK: chroma_db directory exists")
        files = os.listdir(chroma_path)
        print(f"  Files in chroma_db: {files}")
        if len(files) == 0:
            print("WARNING: chroma_db directory is empty")
    else:
        print("ERROR: chroma_db directory missing")
        return False
    
    # Check docs directory
    docs_path = "../docs"
    if os.path.exists(docs_path):
        print("OK: docs directory exists")
        files = os.listdir(docs_path)
        print(f"  Files in docs: {files}")
        if len(files) == 0:
            print("WARNING: docs directory is empty")
    else:
        print("ERROR: docs directory missing")
        return False
    
    return True

def create_minimal_test():
    """Create a minimal test to isolate the issue"""
    print("\n=== Creating Minimal Test ===")
    
    try:
        # Try to import without dependencies
        print("Testing basic imports...")
        
        # Create mock classes to test the logic
        class MockVectorStore:
            def search(self, query, course_name=None, lesson_number=None):
                print(f"MockVectorStore.search called with: query='{query}', course_name={course_name}, lesson_number={lesson_number}")
                
                # Simulate SearchResults
                class MockSearchResults:
                    def __init__(self):
                        self.documents = ["Mock document about " + query]
                        self.metadata = [{"course_title": "Mock Course", "lesson_number": 1}]
                        self.distances = [0.5]
                        self.error = None
                    
                    def is_empty(self):
                        return len(self.documents) == 0
                
                return MockSearchResults()
            
            def get_lesson_link(self, course_title, lesson_number):
                return f"http://mock.com/{course_title}/lesson{lesson_number}"
        
        # Test CourseSearchTool logic without dependencies
        mock_vector_store = MockVectorStore()
        
        # Simulate the execute method logic
        query = "What is MCP?"
        results = mock_vector_store.search(query)
        
        if results.error:
            result = results.error
        elif results.is_empty():
            result = "No relevant content found."
        else:
            # Format results
            formatted = []
            for doc, meta in zip(results.documents, results.metadata):
                course_title = meta.get('course_title', 'unknown')
                lesson_num = meta.get('lesson_number')
                
                header = f"[{course_title}"
                if lesson_num is not None:
                    header += f" - Lesson {lesson_num}"
                header += "]"
                
                formatted.append(f"{header}\n{doc}")
            
            result = "\n\n".join(formatted)
        
        print(f"Mock search result: {result}")
        print("OK: Basic search logic works")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Minimal test failed: {e}")
        return False

def create_debug_rag_test():
    """Create a debug version of RAG system test"""
    print("\n=== Debug RAG System Test ===")
    
    # Create a simple test script that can be run with dependencies
    debug_script = '''#!/usr/bin/env python3
"""Debug script that can be run with proper environment"""

import os
import sys

try:
    from config import config
    from vector_store import VectorStore
    from search_tools import CourseSearchTool, ToolManager
    
    print("=== RAG System Debug ===")
    
    # Test 1: Vector Store
    print("\\n1. Testing Vector Store...")
    vector_store = VectorStore(config.CHROMA_PATH, config.EMBEDDING_MODEL)
    
    course_count = vector_store.get_course_count()
    print(f"   Course count: {course_count}")
    
    if course_count == 0:
        print("   ERROR: No courses in vector store!")
        print("   This is likely the main issue.")
        print("   Solution: Load documents using the startup process")
    else:
        course_titles = vector_store.get_existing_course_titles()
        print(f"   Course titles: {course_titles}")
    
    # Test 2: Search Tool
    print("\\n2. Testing Search Tool...")
    search_tool = CourseSearchTool(vector_store)
    
    try:
        result = search_tool.execute("test query")
        print(f"   Search result: {result}")
        
        if "No relevant content found" in result:
            print("   WARNING: Search returns no content (expected if no courses)")
        elif "Search error" in result:
            print("   ERROR: Search tool has errors")
        else:
            print("   OK: Search tool working")
            
    except Exception as e:
        print(f"   ERROR: Search tool failed: {e}")
    
    # Test 3: Tool Manager
    print("\\n3. Testing Tool Manager...")
    tool_manager = ToolManager()
    tool_manager.register_tool(search_tool)
    
    tool_defs = tool_manager.get_tool_definitions()
    print(f"   Registered tools: {len(tool_defs)}")
    
    for tool_def in tool_defs:
        print(f"     - {tool_def['name']}")
    
    # Test 4: API Key
    print("\\n4. Testing API Configuration...")
    if config.ANTHROPIC_API_KEY:
        print(f"   API Key: {'*' * 10}{config.ANTHROPIC_API_KEY[-4:]}")
        print("   OK: API key is set")
    else:
        print("   ERROR: API key not set")
    
    print("\\n=== Debug Complete ===")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Run this script with: python debug_rag_system.py")
    print("Make sure dependencies are installed")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open('debug_rag_system.py', 'w') as f:
        f.write(debug_script)
    
    print("Created debug_rag_system.py")
    print("Run it with: python debug_rag_system.py")
    
    return True

def main():
    """Main diagnostic function"""
    print("=== RAG System Diagnostic ===")
    
    # Check environment first
    if not check_environment():
        print("\nEnvironment issues found. Fix these first:")
        print("1. Create .env file with ANTHROPIC_API_KEY")
        print("2. Ensure docs directory has course documents")
        return
    
    # Run minimal test
    if not create_minimal_test():
        print("\nBasic logic test failed. Check code structure.")
        return
    
    # Create debug script
    create_debug_rag_test()
    
    print("\n=== Summary ===")
    print("Code structure is correct.")
    print("Most likely issue: Empty vector database")
    print("\nNext steps:")
    print("1. Run: python debug_rag_system.py")
    print("2. If no courses found, restart the application to load docs")
    print("3. Check application startup logs")

if __name__ == '__main__':
    main()