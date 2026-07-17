import json
import os
from pathlib import Path
from typing import Set, Dict, Any, Optional

class StateManager:
    def __init__(self, state_file: str = "github_intel_state.json"):
        self.state_file = Path(state_file)
        self.seen_keys: Set[str] = set()
        self.seen_repos: Set[str] = set()
        self.search_state: Dict[str, Dict[str, Any]] = {}
        self.load_state()
    
    def _get_unique_key(self, result: Dict[str, Any]) -> str:
        search_type = result.get("search_type", "code")
        repo_full_name = result.get("repository", {}).get("full_name", "")
        
        if search_type == "issues":
            issue_number = result.get("number", "")
            issue_url = result.get("html_url", "")
            return f"{search_type}:{repo_full_name}:{issue_number}:{issue_url}"
        elif search_type == "commits":
            commit_sha = result.get("sha", "")
            return f"{search_type}:{repo_full_name}:{commit_sha}"
        elif search_type == "repositories":
            updated_at = result.get("updated_at", "")
            return f"{search_type}:{repo_full_name}:{updated_at}"
        else:
            file_path = result.get("path", "")
            file_sha = result.get("sha", "")
            updated_at = result.get("repository", {}).get("updated_at", "")
            return f"{search_type}:{repo_full_name}:{file_path}:{file_sha}:{updated_at}"
    
    def load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.seen_keys = set(data.get("seen_keys", []))
                    self.seen_repos = set(data.get("seen_repos", []))
                    self.search_state = data.get("search_state", {})
                    print(f"Loaded {len(self.seen_keys)} previously seen results and {len(self.seen_repos)} repositories from state file.")
                    if self.search_state:
                        print(f"Loaded search state for {len(self.search_state)} patterns.")
            except Exception as e:
                print(f"Error loading state: {e}")
                self.seen_keys = set()
                self.seen_repos = set()
                self.search_state = {}
        else:
            self.seen_keys = set()
            self.seen_repos = set()
            self.search_state = {}
    
    def save_state(self):
        try:
            data = {
                "seen_keys": list(self.seen_keys),
                "total_seen": len(self.seen_keys),
                "seen_repos": list(self.seen_repos),
                "total_repos": len(self.seen_repos),
                "search_state": self.search_state
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def is_new_repo(self, result: Dict[str, Any]) -> bool:
        repo_full_name = result.get("repository", {}).get("full_name", "")
        return repo_full_name not in self.seen_repos
    
    def mark_repo_as_seen(self, result: Dict[str, Any]):
        repo_full_name = result.get("repository", {}).get("full_name", "")
        if repo_full_name:
            self.seen_repos.add(repo_full_name)
    
    def is_new_result(self, result: Dict[str, Any]) -> bool:
        key = self._get_unique_key(result)
        return key not in self.seen_keys
    
    def mark_as_seen(self, result: Dict[str, Any]):
        key = self._get_unique_key(result)
        self.seen_keys.add(key)
    
    def get_last_page(self, pattern: str) -> int:
        return self.search_state.get(pattern, {}).get("last_page", 0)
    
    def set_last_page(self, pattern: str, page: int):
        if pattern not in self.search_state:
            self.search_state[pattern] = {}
        self.search_state[pattern]["last_page"] = page
    
    def get_last_result_time(self, pattern: str) -> Optional[str]:
        return self.search_state.get(pattern, {}).get("last_result_time")
    
    def set_last_result_time(self, pattern: str, time_str: str):
        if pattern not in self.search_state:
            self.search_state[pattern] = {}
        self.search_state[pattern]["last_result_time"] = time_str
    
    def filter_new_results(self, results: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        new_results = []
        for result in results:
            if self.is_new_result(result):
                new_results.append(result)
                self.mark_as_seen(result)
        return new_results
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_seen": len(self.seen_keys),
            "state_file": str(self.state_file),
            "patterns_tracked": len(self.search_state)
        }

