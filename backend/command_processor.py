#!/usr/bin/env python3
"""Command processor for handling custom slash commands"""

import os
import re
from typing import Dict, Optional, Tuple
from git_worktree_manager import GitWorktreeManager

class CommandProcessor:
    """Processes custom slash commands similar to Claude's command system"""
    
    def __init__(self, commands_dir: str = "../commands"):
        self.commands_dir = commands_dir
        self.commands = self._load_commands()
        self.worktree_manager = GitWorktreeManager()
    
    def _load_commands(self) -> Dict[str, str]:
        """Load all command templates from the commands directory"""
        commands = {}
        
        if not os.path.exists(self.commands_dir):
            return commands
        
        for filename in os.listdir(self.commands_dir):
            if filename.endswith('.md'):
                command_name = filename[:-3]  # Remove .md extension
                command_path = os.path.join(self.commands_dir, filename)
                
                try:
                    with open(command_path, 'r', encoding='utf-8') as f:
                        commands[command_name] = f.read()
                except Exception as e:
                    print(f"Error loading command {command_name}: {e}")
        
        return commands
    
    def is_command(self, query: str) -> bool:
        """Check if the query is a slash command"""
        return query.strip().startswith('/')
    
    def parse_command(self, query: str) -> Tuple[Optional[str], Dict[str, str]]:
        """Parse a slash command and extract command name and arguments"""
        if not self.is_command(query):
            return None, {}
        
        # Remove leading slash and split into parts
        command_parts = query.strip()[1:].split()
        if not command_parts:
            return None, {}
        
        command_name = command_parts[0]
        
        # Parse arguments (simple key=value format)
        args = {}
        for part in command_parts[1:]:
            if '=' in part:
                key, value = part.split('=', 1)
                args[key.upper()] = value
            else:
                # If no key specified, use as QUERY
                if 'QUERY' not in args:
                    args['QUERY'] = part
                else:
                    args['QUERY'] += ' ' + part
        
        return command_name, args
    
    def process_command(self, query: str) -> Optional[str]:
        """Process a slash command and return the formatted prompt"""
        command_name, args = self.parse_command(query)
        
        if not command_name:
            return None
        
        # Handle special commands
        if command_name == "implement-feature":
            return self._handle_implement_feature(args)
        elif command_name == "list-worktrees":
            return self._handle_list_worktrees()
        elif command_name == "remove-worktree":
            return self._handle_remove_worktree(args)
        
        # Handle template-based commands
        if command_name not in self.commands:
            return None
        
        # Get command template
        template = self.commands[command_name]
        
        # Replace $ARGUMENTS with actual arguments
        if args:
            args_text = "\n".join([f"{key}: {value}" for key, value in args.items()])
            template = template.replace("$ARGUMENTS", args_text)
        else:
            template = template.replace("$ARGUMENTS", "No arguments provided")
        
        # Replace individual argument placeholders
        for key, value in args.items():
            template = template.replace(f"${key}", value)
        
        return template
    
    def get_available_commands(self) -> Dict[str, str]:
        """Get list of available commands with their descriptions"""
        command_info = {}
        
        for command_name, template in self.commands.items():
            # Extract first line as description
            lines = template.split('\n')
            description = lines[0] if lines else "No description available"
            command_info[command_name] = description
        
        # Add built-in commands
        command_info["implement-feature"] = "Create a new Git worktree for parallel feature development"
        command_info["list-worktrees"] = "List all active Git worktrees"
        command_info["remove-worktree"] = "Remove a Git worktree and its branch"
        
        return command_info
    
    def _handle_implement_feature(self, args: Dict[str, str]) -> str:
        """Handle implement-feature command"""
        feature_name = args.get("FEATURE", args.get("NAME", "new-feature"))
        description = args.get("DESCRIPTION", args.get("DESC", ""))
        
        result = self.worktree_manager.create_feature_worktree(feature_name, description)
        
        if result["success"]:
            return f"""Feature worktree created successfully!

Feature: {feature_name}
Branch: {result['branch_name']}
Path: {result['worktree_path']}

To work on this feature:
1. cd {result['worktree_path']}
2. Make your changes
3. Commit and push when ready

You can now implement the feature in parallel without affecting the main codebase."""
        else:
            return f"Failed to create feature worktree: {result['error']}"
    
    def _handle_list_worktrees(self) -> str:
        """Handle list-worktrees command"""
        worktrees = self.worktree_manager.list_worktrees()
        
        if not worktrees:
            return "No active worktrees found."
        
        result = "Active Git Worktrees:\n\n"
        for wt in worktrees:
            result += f"Path: {wt['path']}\n"
            if 'branch' in wt:
                result += f"Branch: {wt['branch']}\n"
            result += "\n"
        
        return result
    
    def _handle_remove_worktree(self, args: Dict[str, str]) -> str:
        """Handle remove-worktree command"""
        feature_name = args.get("FEATURE", args.get("NAME", ""))
        
        if not feature_name:
            return "Please specify a feature name: /remove-worktree FEATURE=feature-name"
        
        result = self.worktree_manager.remove_worktree(feature_name)
        
        if result["success"]:
            return result["message"]
        else:
            return f"Failed to remove worktree: {result['error']}"