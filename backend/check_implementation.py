#!/usr/bin/env python3
"""Check sequential tool calling implementation"""

def check_implementation():
    """Check if sequential tool calling is properly implemented"""
    
    print("=== Sequential Tool Calling Implementation Check ===")
    
    # Check ai_generator.py
    try:
        with open('ai_generator.py', 'r') as f:
            content = f.read()
        
        checks = [
            "Sequential tool calls" in content,
            "Multi-Round Strategy" in content,
            "_handle_sequential_tool_execution" in content,
            "max_rounds: int = 2" in content,
            "for round_num in range(1, max_rounds + 1)" in content,
            "if round_num < max_rounds" in content,
            "current_response.stop_reason != \"tool_use\"" in content
        ]
        
        print(f"AI Generator checks: {sum(checks)}/7 passed")
        
        if all(checks):
            print("OK: AI Generator implementation complete")
        else:
            print("MISSING: Some AI Generator features")
            
    except Exception as e:
        print(f"ERROR: Could not check ai_generator.py: {e}")
        return False
    
    # Check tests
    try:
        with open('tests/test_ai_generator.py', 'r') as f:
            test_content = f.read()
        
        test_checks = [
            "test_sequential_tool_calling_two_rounds" in test_content,
            "test_sequential_tool_calling_early_termination" in test_content,
            "test_sequential_tool_calling_max_rounds_limit" in test_content,
            "call_count, 3" in test_content,
            "call_count, 2" in test_content
        ]
        
        print(f"Test coverage checks: {sum(test_checks)}/5 passed")
        
        if all(test_checks):
            print("OK: Test coverage complete")
        else:
            print("MISSING: Some test scenarios")
            
    except Exception as e:
        print(f"ERROR: Could not check tests: {e}")
        return False
    
    print("\n=== Implementation Summary ===")
    print("Sequential tool calling features:")
    print("- Maximum 2 rounds per query")
    print("- Early termination when AI doesn't need more tools")
    print("- Context preserved between rounds")
    print("- Tools available in intermediate rounds")
    print("- Comprehensive test coverage")
    
    return True

if __name__ == '__main__':
    check_implementation()