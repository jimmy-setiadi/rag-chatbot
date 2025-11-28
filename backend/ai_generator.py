import anthropic
from typing import List, Optional, Dict, Any

class AIGenerator:
    """Handles interactions with Anthropic's Claude API for generating responses"""
    
    # Static system prompt to avoid rebuilding on each call
    SYSTEM_PROMPT = """ You are an AI assistant specialized in course materials and educational content with access to search tools for course information.

Tool Usage:
- **Course content questions**: Use search_course_content for specific course materials
- **Course outline questions**: Use get_course_outline for course structure, lesson lists, or course overviews
- **Sequential tool calls**: You can make multiple tool calls across rounds to gather comprehensive information
- **Complex queries**: For multi-part questions or comparisons, gather information step by step
- Synthesize results into accurate, fact-based responses
- If tools yield no results, state this clearly without offering alternatives

For Course Outline Queries:
- Always return: course title, course link (if available), and complete lesson list
- Format each lesson as: "Lesson [number]: [title]"
- Include total lesson count

Multi-Round Strategy:
- If you need more information after seeing initial results, make another tool call
- Use previous results to inform subsequent searches
- Build comprehensive answers from multiple information sources

Response Protocol:
- **General knowledge questions**: Answer using existing knowledge without tools
- **Course-specific questions**: Use appropriate tools to gather information
- **No meta-commentary**:
 - Provide direct answers only — no reasoning process, tool explanations, or question-type analysis
 - Do not mention "based on the search results" or "using the tool"

All responses must be:
1. **Brief, Concise and focused** - Get to the point quickly
2. **Educational** - Maintain instructional value
3. **Clear** - Use accessible language
4. **Example-supported** - Include relevant examples when they aid understanding
Provide only the direct answer to what was asked.
"""
    
    def __init__(self, api_key: str, model: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        
        # Pre-build base API parameters
        self.base_params = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 800
        }
    
    def generate_response(self, query: str,
                         conversation_history: Optional[str] = None,
                         tools: Optional[List] = None,
                         tool_manager=None) -> str:
        """
        Generate AI response with optional tool usage and conversation context.
        
        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            tools: Available tools the AI can use
            tool_manager: Manager to execute tools
            
        Returns:
            Generated response as string
        """
        
        # Build system content efficiently - avoid string ops when possible
        system_content = (
            f"{self.SYSTEM_PROMPT}\n\nPrevious conversation:\n{conversation_history}"
            if conversation_history 
            else self.SYSTEM_PROMPT
        )
        
        # Prepare API call parameters efficiently
        api_params = {
            **self.base_params,
            "messages": [{"role": "user", "content": query}],
            "system": system_content
        }
        
        # Add tools if available
        if tools:
            api_params["tools"] = tools
            api_params["tool_choice"] = {"type": "auto"}
        
        # Get response from Claude
        response = self.client.messages.create(**api_params)
        
        # Handle tool execution if needed
        if response.stop_reason == "tool_use" and tool_manager:
            return self._handle_sequential_tool_execution(response, api_params, tool_manager)
        
        # Return direct response
        return response.content[0].text
    
    def _handle_sequential_tool_execution(self, initial_response, base_params: Dict[str, Any], tool_manager, max_rounds: int = 2):
        """
        Handle sequential tool execution across multiple API rounds.
        
        Args:
            initial_response: The response containing tool use requests
            base_params: Base API parameters
            tool_manager: Manager to execute tools
            max_rounds: Maximum number of tool execution rounds
            
        Returns:
            Final response text after all tool execution rounds
        """
        try:
            messages = base_params["messages"].copy()
            current_response = initial_response
            
            for round_num in range(1, max_rounds + 1):
                print(f"Starting tool execution round {round_num}")
                
                # Check if current response has tool use
                if current_response.stop_reason != "tool_use":
                    print(f"No tool use in round {round_num}, returning response")
                    return current_response.content[0].text
                
                # Add AI's tool use response to messages
                messages.append({"role": "assistant", "content": current_response.content})
                
                # Execute tools and collect results
                tool_results = []
                for content_block in current_response.content:
                    if content_block.type == "tool_use":
                        try:
                            print(f"Round {round_num}: Executing tool {content_block.name}")
                            tool_result = tool_manager.execute_tool(
                                content_block.name, 
                                **content_block.input
                            )
                            print(f"Round {round_num}: Tool {content_block.name} executed successfully")
                            
                        except Exception as e:
                            print(f"ERROR in round {round_num} executing tool {content_block.name}: {e}")
                            tool_result = f"Tool execution failed: {str(e)}"
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": tool_result
                        })
                
                # Add tool results to messages
                if tool_results:
                    messages.append({"role": "user", "content": tool_results})
                
                # Prepare next API call
                next_params = {
                    **self.base_params,
                    "messages": messages,
                    "system": base_params["system"]
                }
                
                # Add tools for all rounds except the last
                if round_num < max_rounds and "tools" in base_params:
                    next_params["tools"] = base_params["tools"]
                    next_params["tool_choice"] = {"type": "auto"}
                
                # Make next API call
                try:
                    print(f"Making API call for round {round_num}")
                    current_response = self.client.messages.create(**next_params)
                    print(f"Round {round_num} response received")
                except Exception as e:
                    print(f"ERROR in round {round_num} API call: {e}")
                    return f"API call failed in round {round_num}: {str(e)}"
            
            # Return final response after max rounds
            print(f"Completed {max_rounds} rounds, returning final response")
            return current_response.content[0].text
            
        except Exception as e:
            print(f"ERROR in sequential tool execution: {e}")
            import traceback
            traceback.print_exc()
            return f"Sequential tool execution failed: {str(e)}"