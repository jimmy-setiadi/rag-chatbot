import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Define colors
frontend_color = '#E3F2FD'  # Light blue
backend_color = '#F3E5F5'   # Light purple
ai_color = '#E8F5E8'        # Light green
data_color = '#FFF3E0'      # Light orange

# Helper function to create rounded rectangles
def create_box(ax, x, y, width, height, text, color, fontsize=10):
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.1",
                         facecolor=color,
                         edgecolor='black',
                         linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
            ha='center', va='center', fontsize=fontsize, weight='bold')

# Helper function to create arrows
def create_arrow(ax, start_x, start_y, end_x, end_y, text='', offset=0.2):
    arrow = patches.FancyArrowPatch((start_x, start_y), (end_x, end_y),
                                   connectionstyle="arc3,rad=0", 
                                   arrowstyle='->', 
                                   mutation_scale=20,
                                   color='darkblue',
                                   linewidth=2)
    ax.add_patch(arrow)
    if text:
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2 + offset
        ax.text(mid_x, mid_y, text, ha='center', va='center', 
                fontsize=8, style='italic', color='darkblue')

# Title
ax.text(5, 11.5, 'RAG System Query Flow', ha='center', va='center', 
        fontsize=18, weight='bold')

# 1. Frontend Layer
create_box(ax, 0.5, 10, 2, 0.8, 'Frontend\n(script.js)', frontend_color, 11)
ax.text(1.5, 9.5, '1. User types query\n2. POST /api/query', ha='center', va='center', fontsize=9)

# 2. API Layer
create_box(ax, 4, 10, 2, 0.8, 'FastAPI\n(app.py)', backend_color, 11)
ax.text(5, 9.5, 'query_documents()\nendpoint', ha='center', va='center', fontsize=9)

# 3. RAG System
create_box(ax, 7.5, 10, 2, 0.8, 'RAG System\n(rag_system.py)', backend_color, 11)
ax.text(8.5, 9.5, 'Orchestrates\nall components', ha='center', va='center', fontsize=9)

# 4. Session Manager
create_box(ax, 0.5, 8, 1.8, 0.8, 'Session Manager', backend_color, 10)
ax.text(1.4, 7.5, 'Get/update\nconversation\nhistory', ha='center', va='center', fontsize=8)

# 5. AI Generator
create_box(ax, 3, 8, 2, 0.8, 'AI Generator\n(ai_generator.py)', ai_color, 10)
ax.text(4, 7.5, 'Claude API\nwith tools', ha='center', va='center', fontsize=9)

# 6. Tool Manager
create_box(ax, 6, 8, 1.8, 0.8, 'Tool Manager', ai_color, 10)
ax.text(6.9, 7.5, 'Manages\navailable tools', ha='center', va='center', fontsize=8)

# 7. Search Tool
create_box(ax, 8.2, 8, 1.5, 0.8, 'Search Tool', ai_color, 10)
ax.text(8.95, 7.5, 'Course content\nsearch logic', ha='center', va='center', fontsize=8)

# 8. Vector Store
create_box(ax, 3, 5.5, 2.5, 1, 'Vector Store\n(vector_store.py)', data_color, 11)
ax.text(4.25, 4.8, 'ChromaDB\n• Course catalog\n• Course content', ha='center', va='center', fontsize=9)

# 9. Document Processor
create_box(ax, 6.5, 5.5, 2.5, 1, 'Document Processor', data_color, 11)
ax.text(7.75, 4.8, 'Text chunking\nCourse parsing\nMetadata extraction', ha='center', va='center', fontsize=9)

# 10. Course Documents
create_box(ax, 3.5, 3, 3, 0.8, 'Course Documents\n(docs/*.txt)', data_color, 11)
ax.text(5, 2.5, 'Raw course transcripts\nwith lessons and content', ha='center', va='center', fontsize=9)

# Flow arrows - Main query path
create_arrow(ax, 2.5, 10.4, 4, 10.4, '1. Query + Session')
create_arrow(ax, 6, 10.4, 7.5, 10.4, '2. Process')
create_arrow(ax, 8.5, 10, 8.5, 8.8, '3. Get history')
create_arrow(ax, 7.5, 8.4, 5, 8.4, '4. Generate response')
create_arrow(ax, 4, 8, 4, 6.5, '5. Tool execution')
create_arrow(ax, 4.25, 5.5, 4.25, 3.8, '6. Vector search')

# Return path arrows
create_arrow(ax, 4.75, 3.8, 4.75, 5.5, '7. Search results')
create_arrow(ax, 5, 6.5, 5, 8, '8. Formatted results')
create_arrow(ax, 6, 8.4, 7.5, 8.4, '9. Final response')
create_arrow(ax, 7.5, 10.4, 6, 10.4, '10. JSON response')
create_arrow(ax, 4, 10.4, 2.5, 10.4, '11. Display answer')

# Side processes
create_arrow(ax, 1.4, 8, 1.4, 9.5, 'Session\nmanagement', 0.3)
create_arrow(ax, 6.9, 8, 6.9, 9.5, 'Tool\ndefinitions', 0.3)

# Data flow indicators
ax.text(0.2, 6.5, 'Session\nContext', ha='center', va='center', fontsize=8, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))

ax.text(9.5, 6.5, 'Source\nTracking', ha='center', va='center', fontsize=8,
        bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))

# Legend
legend_y = 1.5
ax.text(0.5, legend_y, 'Legend:', fontsize=12, weight='bold')
create_box(ax, 0.5, legend_y-0.5, 1.2, 0.3, 'Frontend', frontend_color, 9)
create_box(ax, 2, legend_y-0.5, 1.2, 0.3, 'Backend', backend_color, 9)
create_box(ax, 3.5, legend_y-0.5, 1.2, 0.3, 'AI/Tools', ai_color, 9)
create_box(ax, 5, legend_y-0.5, 1.2, 0.3, 'Data Layer', data_color, 9)

# Key steps summary
steps_text = """Key Steps:
1. User submits query via web interface
2. FastAPI receives POST request
3. RAG system orchestrates processing
4. Session manager provides context
5. AI generator calls Claude with tools
6. Search tool queries vector store
7. ChromaDB returns relevant chunks
8. Tool formats results with sources
9. Claude generates final response
10. Response returned to frontend
11. UI displays answer with sources"""

ax.text(7.2, 2.5, steps_text, fontsize=9, va='top',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('rag_query_flow_diagram.png', dpi=300, bbox_inches='tight')
plt.show()

print("Query flow diagram saved as 'rag_query_flow_diagram.png'")