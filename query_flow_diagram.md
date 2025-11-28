# RAG System Query Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RAG SYSTEM QUERY FLOW                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    1. User Query     ┌─────────────┐    2. Process      ┌─────────────┐
│  FRONTEND   │ ──────────────────► │   FastAPI   │ ─────────────────► │ RAG System  │
│ (script.js) │                     │  (app.py)   │                    │(rag_system) │
│             │ ◄────────────────── │             │ ◄───────────────── │             │
└─────────────┘   11. JSON Response └─────────────┘   10. Answer+Sources└─────────────┘
       │                                                                       │
       │ POST /api/query                                                       │ 3. Get History
       │ {query, session_id}                                                   ▼
       │                                                              ┌─────────────┐
       │                                                              │   Session   │
       │                                                              │  Manager    │
       │                                                              └─────────────┘
       │                                                                       │
       │                                                                       │ 4. Generate
       │                                                                       ▼
┌─────────────┐                                                      ┌─────────────┐
│    USER     │                                                      │AI Generator │
│  Interface  │                                                      │(Claude API) │
│             │                                                      │             │
└─────────────┘                                                      └─────────────┘
       │                                                                       │
       │ 12. Display Answer                                                    │ 5. Tool Call
       │     with Sources                                                      ▼
       │                                                              ┌─────────────┐
       │                                                              │Tool Manager │
       │                                                              │             │
       │                                                              └─────────────┘
       │                                                                       │
       │                                                                       │ 6. Execute
       │                                                                       ▼
       │                                                              ┌─────────────┐
       │                                                              │Search Tool  │
       │                                                              │             │
       │                                                              └─────────────┘
       │                                                                       │
       │                                                                       │ 7. Vector Search
       │                                                                       ▼
       │                                                              ┌─────────────┐
       │                                                              │Vector Store │
       │                                                              │ (ChromaDB)  │
       │                                                              │             │
       │                                                              └─────────────┘
       │                                                                       │
       │                                                                       │ 8. Return Results
       │                                                                       │
       │                                                              ┌─────────────┐
       │                                                              │   Course    │
       │                                                              │ Documents   │
       │                                                              │ (Processed) │
       │                                                              └─────────────┘

═══════════════════════════════════════════════════════════════════════════════════

DETAILED FLOW BREAKDOWN:

1. 🖥️  FRONTEND (script.js)
   ├── User types query in chat interface
   ├── sendMessage() function triggered
   └── POST request to /api/query with {query, session_id}

2. 🌐 API LAYER (app.py)
   ├── FastAPI receives POST /api/query
   ├── query_documents() endpoint processes request
   └── Calls rag_system.query(query, session_id)

3. 🧠 RAG ORCHESTRATION (rag_system.py)
   ├── Gets conversation history from session_manager
   ├── Calls ai_generator.generate_response()
   └── Returns (answer, sources) tuple

4. 🤖 AI GENERATION (ai_generator.py)
   ├── Sends query to Claude API with available tools
   ├── Claude decides to use search_course_content tool
   └── Handles tool execution workflow

5. 🔧 TOOL EXECUTION (search_tools.py)
   ├── CourseSearchTool.execute() called
   ├── Parameters: {query, course_name?, lesson_number?}
   └── Calls vector_store.search()

6. 🔍 VECTOR SEARCH (vector_store.py)
   ├── Resolves course name if provided
   ├── Builds search filters
   ├── Queries ChromaDB collections:
   │   ├── course_catalog (metadata)
   │   └── course_content (chunks)
   └── Returns SearchResults object

7. 📊 SEARCH RESULTS
   ├── Formatted with course/lesson context
   ├── Sources tracked for UI display
   └── Returned to AI for synthesis

8. 🔄 RESPONSE GENERATION
   ├── Claude synthesizes final answer from search results
   ├── Tool manager collects sources
   └── Session manager updates conversation history

9. 📤 API RESPONSE
   ├── Returns QueryResponse JSON:
   │   ├── answer: Generated response
   │   ├── sources: List of source references
   │   └── session_id: Session identifier
   └── HTTP 200 with response data

10. 🎨 FRONTEND DISPLAY
    ├── Receives JSON response
    ├── Renders answer with markdown formatting
    ├── Shows sources in collapsible section
    └── Updates chat interface

═══════════════════════════════════════════════════════════════════════════════════

DATA STRUCTURES:

Query Request:
{
  "query": "What is covered in lesson 3 of the MCP course?",
  "session_id": "uuid-string" | null
}

Query Response:
{
  "answer": "Lesson 3 covers multimodal requests...",
  "sources": ["MCP Course - Lesson 3", "Building Computer Use - Lesson 3"],
  "session_id": "uuid-string"
}

Tool Call Example:
{
  "name": "search_course_content",
  "input": {
    "query": "lesson 3 content",
    "course_name": "MCP",
    "lesson_number": 3
  }
}

═══════════════════════════════════════════════════════════════════════════════════

KEY COMPONENTS:

🎯 SESSION MANAGEMENT
- Tracks conversation history per user
- Maintains context across queries
- 5-minute TTL for sessions

🔍 SEMANTIC SEARCH
- ChromaDB with sentence transformers
- Course name fuzzy matching
- Lesson-level filtering

🤖 AI INTEGRATION
- Claude 3.5 Sonnet with tool calling
- Structured prompts for consistency
- Chain-of-thought reasoning

📚 DOCUMENT PROCESSING
- Structured course parsing
- Text chunking with overlap
- Metadata preservation

🌐 WEB INTERFACE
- Real-time chat interface
- Source attribution
- Course statistics sidebar
```