#!/usr/bin/env python3
"""Debug script that can be run with proper environment"""

import os
import sys

try:
    from config import config
    from vector_store import VectorStore
    from search_tools import CourseSearchTool, ToolManager
    
    print("=== RAG System Debug ===")
    
    # Test 1: Vector Store
    print("\n1. Testing Vector Store...")
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
    print("\n2. Testing Search Tool...")
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
    print("\n3. Testing Tool Manager...")
    tool_manager = ToolManager()
    tool_manager.register_tool(search_tool)
    
    tool_defs = tool_manager.get_tool_definitions()
    print(f"   Registered tools: {len(tool_defs)}")
    
    for tool_def in tool_defs:
        print(f"     - {tool_def['name']}")
    
    # Test 4: API Key
    print("\n4. Testing API Configuration...")
    if config.ANTHROPIC_API_KEY:
        print(f"   API Key: {'*' * 10}{config.ANTHROPIC_API_KEY[-4:]}")
        print("   OK: API key is set")
    else:
        print("   ERROR: API key not set")
    
    print("\n=== Debug Complete ===")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Run this script with: python debug_rag_system.py")
    print("Make sure dependencies are installed")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
