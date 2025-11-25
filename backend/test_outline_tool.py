#!/usr/bin/env python3
"""Quick test for the new CourseOutlineTool"""

from config import config
from vector_store import VectorStore
from search_tools import CourseOutlineTool

def test_outline_tool():
    """Test the course outline tool functionality"""
    
    # Initialize vector store
    vector_store = VectorStore(config.CHROMA_PATH, config.EMBEDDING_MODEL)
    
    # Initialize outline tool
    outline_tool = CourseOutlineTool(vector_store)
    
    # Test tool definition
    tool_def = outline_tool.get_tool_definition()
    print("Tool Definition:")
    print(f"Name: {tool_def['name']}")
    print(f"Description: {tool_def['description']}")
    print()
    
    # Get all courses to test with
    courses_metadata = vector_store.get_all_courses_metadata()
    if not courses_metadata:
        print("No courses found in vector store")
        return
    
    # Test with first course
    first_course = courses_metadata[0]
    course_title = first_course['title']
    
    print(f"Testing with course: {course_title}")
    print("=" * 50)
    
    # Execute outline tool
    result = outline_tool.execute(course_title=course_title)
    print(result)

if __name__ == "__main__":
    test_outline_tool()