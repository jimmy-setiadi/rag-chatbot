#!/usr/bin/env python3
"""Git worktree manager for parallel feature development"""

import os
import subprocess
import json
from typing import Dict, List, Optional

class GitWorktreeManager:
    """Manages Git worktrees for parallel feature development"""
    
    def __init__(self, base_repo_path: str = "."):
        self.base_repo_path = os.path.abspath(base_repo_path)
        self.worktrees_file = os.path.join(self.base_repo_path, ".worktrees.json")
    
    def _run_git_command(self, cmd: List[str], cwd: str = None) -> tuple:
        """Run git command and return (success, output, error)"""
        try:
            result = subprocess.run(
                ["git"] + cmd,
                cwd=cwd or self.base_repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)
    
    def create_feature_worktree(self, feature_name: str, description: str = "") -> Dict:
        """Create a new worktree for feature development"""
        # Sanitize feature name for branch/directory
        safe_name = feature_name.lower().replace(" ", "-").replace("_", "-")
        branch_name = f"feature/{safe_name}"
        worktree_path = os.path.join(self.base_repo_path, "..", f"feature-{safe_name}")
        
        # Create branch from current HEAD
        success, output, error = self._run_git_command(["checkout", "-b", branch_name])
        if not success:
            return {"success": False, "error": f"Failed to create branch: {error}"}
        
        # Switch back to main/master
        success, output, error = self._run_git_command(["checkout", "master"])
        if not success:
            success, output, error = self._run_git_command(["checkout", "main"])
        
        # Create worktree
        success, output, error = self._run_git_command([
            "worktree", "add", worktree_path, branch_name
        ])
        
        if not success:
            # Cleanup branch if worktree creation failed
            self._run_git_command(["branch", "-D", branch_name])
            return {"success": False, "error": f"Failed to create worktree: {error}"}
        
        # Save worktree info
        worktree_info = {
            "feature_name": feature_name,
            "description": description,
            "branch_name": branch_name,
            "worktree_path": worktree_path,
            "created_at": subprocess.run(["date"], capture_output=True, text=True).stdout.strip()
        }
        
        self._save_worktree_info(safe_name, worktree_info)
        
        return {
            "success": True,
            "worktree_path": worktree_path,
            "branch_name": branch_name,
            "message": f"Created worktree for '{feature_name}' at {worktree_path}"
        }
    
    def list_worktrees(self) -> List[Dict]:
        """List all active worktrees"""
        success, output, error = self._run_git_command(["worktree", "list", "--porcelain"])
        
        if not success:
            return []
        
        worktrees = []
        current_worktree = {}
        
        for line in output.split('\n'):
            if line.startswith('worktree '):
                if current_worktree:
                    worktrees.append(current_worktree)
                current_worktree = {"path": line[9:]}
            elif line.startswith('branch '):
                current_worktree["branch"] = line[7:]
            elif line.startswith('HEAD '):
                current_worktree["head"] = line[4:]
        
        if current_worktree:
            worktrees.append(current_worktree)
        
        return worktrees
    
    def remove_worktree(self, feature_name: str) -> Dict:
        """Remove a worktree and its branch"""
        safe_name = feature_name.lower().replace(" ", "-").replace("_", "-")
        branch_name = f"feature/{safe_name}"
        worktree_path = os.path.join(self.base_repo_path, "..", f"feature-{safe_name}")
        
        # Remove worktree
        success, output, error = self._run_git_command(["worktree", "remove", worktree_path])
        if not success:
            return {"success": False, "error": f"Failed to remove worktree: {error}"}
        
        # Delete branch
        success, output, error = self._run_git_command(["branch", "-D", branch_name])
        if not success:
            return {"success": False, "error": f"Failed to delete branch: {error}"}
        
        # Remove from tracking
        self._remove_worktree_info(safe_name)
        
        return {"success": True, "message": f"Removed worktree for '{feature_name}'"}
    
    def _save_worktree_info(self, safe_name: str, info: Dict):
        """Save worktree information to tracking file"""
        try:
            if os.path.exists(self.worktrees_file):
                with open(self.worktrees_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            data[safe_name] = info
            
            with open(self.worktrees_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass  # Non-critical
    
    def _remove_worktree_info(self, safe_name: str):
        """Remove worktree information from tracking file"""
        try:
            if os.path.exists(self.worktrees_file):
                with open(self.worktrees_file, 'r') as f:
                    data = json.load(f)
                
                if safe_name in data:
                    del data[safe_name]
                    
                    with open(self.worktrees_file, 'w') as f:
                        json.dump(data, f, indent=2)
        except Exception:
            pass  # Non-critical