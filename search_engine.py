from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from github_client import GitHubClient
from patterns import PATTERNS, get_file_patterns, get_code_patterns
from state_manager import StateManager
from config import RESULTS_PER_PAGE

class SearchEngine:
    def __init__(self, client: GitHubClient, state_manager: Optional[StateManager] = None):
        self.client = client
        self.state_manager = state_manager

    def parse_query(self, query: str) -> Dict[str, Any]:
        query_type = "code"
        search_query = query
        
        if query.startswith("filename:"):
            filename = query.replace("filename:", "").strip()
            search_query = f'filename:"{filename}"'
        elif query.startswith("repo:"):
            repo_query = query.replace("repo:", "").strip()
            search_query = f'repo:{repo_query}'
            query_type = "code"
        elif query.startswith('"') and query.endswith('"'):
            search_query = query
        elif '"' in query:
            search_query = query
        else:
            search_query = query
        
        search_query = self._sanitize_query(search_query)
        
        return {
            "type": query_type,
            "query": search_query
        }
    
    def _sanitize_query(self, query: str) -> str:
        if query.startswith("filename:") or query.startswith("repo:"):
            return query
        
        query_clean = query.strip()
        
        if query_clean.startswith('"') and query_clean.endswith('"'):
            query_clean = query_clean[1:-1]
        
        query_clean = query_clean.replace('"', '')
        query_clean = query_clean.replace("'", "")
        query_clean = query_clean.replace("(", " ")
        query_clean = query_clean.replace(")", " ")
        query_clean = query_clean.replace("=", " ")
        query_clean = query_clean.replace(":", " ")
        query_clean = query_clean.replace(".", " ")
        query_clean = " ".join(query_clean.split())
        
        if query_clean.strip():
            return f'"{query_clean}"'
        
        return query

    def search_repos(self, query: str, max_results: int = 1000, start_page: int = 1, sort: str = None, order: str = None) -> List[Dict[str, Any]]:
        parsed = self.parse_query(query)
        
        if parsed["type"] == "code":
            results = self.client.search_code(parsed["query"], max_results, start_page, sort, order)
        else:
            results = self.client.search_repositories(parsed["query"], max_results)
        
        return results
    
    def search_all_types(self, query: str, max_results_per_type: int = 100, start_page: int = 1) -> List[Dict[str, Any]]:
        parsed = self.parse_query(query)
        search_query = parsed["query"]
        all_results = []
        
        search_types = [
            ("code", self.client.search_code),
            ("repositories", self.client.search_repositories),
            ("issues", self.client.search_issues),
            ("commits", self.client.search_commits),
        ]
        
        for type_name, search_func in search_types:
            try:
                print(f"  🔍 Searching {type_name}...")
                if type_name == "repositories":
                    results = search_func(search_query, max_results_per_type)
                elif type_name == "issues":
                    results = search_func(search_query, max_results_per_type, start_page, "updated", "desc")
                elif type_name == "commits":
                    results = search_func(search_query, max_results_per_type, start_page, "author-date", "desc")
                else:
                    results = search_func(search_query, max_results_per_type, start_page, None, None)
                
                for result in results:
                    result["search_type"] = type_name
                
                all_results.extend(results)
                print(f"  ✓ Found {len(results)} results in {type_name}")
            except Exception as e:
                print(f"  ⚠️  Error searching {type_name}: {e}")
                continue
        
        return all_results

    def enrich_results(self, results: List[Dict[str, Any]], fetch_content: bool = True) -> List[Dict[str, Any]]:
        enriched = []
        total = len(results)
        
        for idx, result in enumerate(results, 1):
            try:
                search_type = result.get("search_type", "code")
                repo = result.get("repository", {})
                
                if search_type == "issues":
                    enriched_result = {
                        "search_type": "issue",
                        "issue": {
                            "title": result.get("title", ""),
                            "body": result.get("body", ""),
                            "url": result.get("html_url", ""),
                            "number": result.get("number", 0),
                            "state": result.get("state", ""),
                            "created_at": result.get("created_at", ""),
                            "updated_at": result.get("updated_at", "")
                        },
                        "repository": {
                            "name": repo.get("name", "") if repo else "",
                            "owner": repo.get("owner", {}).get("login", "") if repo and isinstance(repo.get("owner"), dict) else "",
                            "full_name": repo.get("full_name", "") if repo else "",
                            "url": repo.get("html_url", "") if repo else ""
                        }
                    }
                elif search_type == "commits":
                    enriched_result = {
                        "search_type": "commit",
                        "commit": {
                            "sha": result.get("sha", ""),
                            "message": result.get("commit", {}).get("message", "") if result.get("commit") else "",
                            "url": result.get("html_url", ""),
                            "author": result.get("commit", {}).get("author", {}).get("name", "") if result.get("commit") else "",
                            "date": result.get("commit", {}).get("author", {}).get("date", "") if result.get("commit") else ""
                        },
                        "repository": {
                            "name": repo.get("name", "") if repo else "",
                            "owner": repo.get("owner", {}).get("login", "") if repo and isinstance(repo.get("owner"), dict) else "",
                            "full_name": repo.get("full_name", "") if repo else "",
                            "url": repo.get("html_url", "") if repo else ""
                        }
                    }
                elif search_type == "repositories":
                    enriched_result = {
                        "search_type": "repository",
                        "repository": {
                            "name": result.get("name", ""),
                            "owner": result.get("owner", {}).get("login", "") if isinstance(result.get("owner"), dict) else "",
                            "full_name": result.get("full_name", ""),
                            "url": result.get("html_url", ""),
                            "stars": result.get("stargazers_count", 0),
                            "forks": result.get("forks_count", 0),
                            "updated_at": result.get("updated_at", ""),
                            "created_at": result.get("created_at", ""),
                            "description": result.get("description", ""),
                            "language": result.get("language", ""),
                            "private": result.get("private", False)
                        }
                    }
                else:
                    if not repo:
                        continue
                    
                    owner = repo.get("owner", {})
                    if isinstance(owner, dict):
                        owner = owner.get("login", "")
                    else:
                        owner = ""
                    
                    repo_name = repo.get("name", "")
                    
                    enriched_result = {
                        "search_type": "code",
                        "repository": {
                            "name": repo_name,
                            "owner": owner,
                            "full_name": repo.get("full_name", ""),
                            "url": repo.get("html_url", ""),
                            "stars": repo.get("stargazers_count", 0),
                            "forks": repo.get("forks_count", 0),
                            "updated_at": repo.get("updated_at", ""),
                            "created_at": repo.get("created_at", ""),
                            "description": repo.get("description", ""),
                            "language": repo.get("language", ""),
                            "private": repo.get("private", False)
                        },
                        "file": {
                            "name": result.get("name", ""),
                            "path": result.get("path", ""),
                            "url": result.get("html_url", ""),
                            "sha": result.get("sha", "")
                        },
                        "matched_text": result.get("text_matches", [])
                    }
                    
                    if fetch_content and enriched_result["file"]["path"]:
                        try:
                            content = self.client.get_file_content(
                                owner,
                                repo_name,
                                enriched_result["file"]["path"]
                            )
                            enriched_result["file"]["content"] = content
                        except Exception as e:
                            enriched_result["file"]["content"] = None
                            if idx % 100 == 0:
                                print(f"  Enriching {idx}/{total}... (some files skipped due to errors)")
                
                enriched.append(enriched_result)
                
                if idx % 100 == 0:
                    print(f"  Enriched {idx}/{total} results...")
                    
            except Exception as e:
                if idx % 100 == 0:
                    print(f"  Error enriching result {idx}/{total}: {e}")
                continue
        
        return enriched

    def search_and_collect(self, query: str, max_results: int = 1000, fetch_content: bool = True) -> List[Dict[str, Any]]:
        print(f"\n{'='*60}")
        print(f"Starting search: {query}")
        print(f"{'='*60}\n")
        
        results = self.search_repos(query, max_results)
        
        if not results:
            print("No results found.")
            return []
        
        print(f"\nFound {len(results)} results. Enriching with metadata...")
        enriched = self.enrich_results(results, fetch_content)
        
        return enriched

    def search_all_dangerous_patterns(self, max_results_per_pattern: int = 100, fetch_content: bool = True, continuous: bool = False, output_handler=None) -> List[Dict[str, Any]]:
        print(f"\n{'='*60}")
        print("🔍 Auto-Searching All Dangerous Patterns")
        if continuous:
            print("🔄 Continuous Mode: Will run until manually stopped")
        print(f"{'='*60}\n")
        
        file_patterns = get_file_patterns()
        code_patterns = get_code_patterns()
        all_patterns = file_patterns + code_patterns
        
        iteration = 0
        
        while True:
            iteration += 1
            if continuous:
                print(f"\n{'='*60}")
                print(f"🔄 Iteration #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}\n")
            
            all_results = []
            seen_keys = set() if not self.state_manager else None
            
            total_patterns = len(all_patterns)
            current_pattern = 0
            
            print(f"📋 Total patterns to search: {total_patterns}\n")
            
            for pattern in all_patterns:
                current_pattern += 1
                print(f"[{current_pattern}/{total_patterns}] Searching: {pattern}")
                
                try:
                    pattern_results = []
                    new_results = []
                    
                    if continuous and self.state_manager:
                        last_page = self.state_manager.get_last_page(pattern)
                        last_result_time = self.state_manager.get_last_result_time(pattern)
                        
                        if last_result_time:
                            try:
                                last_time = datetime.fromisoformat(last_result_time.replace('Z', '+00:00'))
                                pushed_date = last_time.strftime('%Y-%m-%d')
                                newest_query = f"{pattern} pushed:>={pushed_date}"
                                print(f"  🔍 Phase 1: Searching newest/updated repositories (pushed after {pushed_date})...")
                            except Exception as e:
                                recent_date = datetime.now().strftime('%Y-%m-%d')
                                newest_query = f"{pattern} pushed:>={recent_date}"
                                print(f"  🔍 Phase 1: Searching newest/updated repositories (pushed after {recent_date})...")
                        else:
                            recent_date = datetime.now().strftime('%Y-%m-%d')
                            newest_query = f"{pattern} pushed:>={recent_date}"
                            print(f"  🔍 Phase 1: Searching newest/updated repositories (pushed after {recent_date})...")
                        
                        newest_results = self.search_all_types(
                            newest_query, 
                            max_results_per_pattern,
                            start_page=1
                        )
                        
                        newest_new = []
                        latest_time = None
                        for result in newest_results:
                            repo = result.get("repository", {})
                            repo_full_name = repo.get("full_name", "") if repo else ""
                            updated_at = repo.get("updated_at", "") if repo else ""
                            
                            is_new_file = self.state_manager.is_new_result(result)
                            is_new_repo = repo_full_name and self.state_manager.is_new_repo(result)
                            
                            if is_new_file or (is_new_repo and updated_at):
                                result["matched_pattern"] = pattern
                                newest_new.append(result)
                                self.state_manager.mark_as_seen(result)
                                
                                if is_new_repo:
                                    self.state_manager.mark_repo_as_seen(result)
                                
                                if repo and updated_at:
                                    try:
                                        result_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                                        if latest_time is None or result_time > latest_time:
                                            latest_time = result_time
                                    except:
                                        pass
                            elif is_new_repo:
                                self.state_manager.mark_repo_as_seen(result)
                        
                        new_results.extend(newest_new)
                        pattern_results.extend(newest_results)
                        print(f"  ✓ Found {len(newest_results)} results ({len(newest_new)} new) from newest repositories")
                        
                        if latest_time:
                            self.state_manager.set_last_result_time(pattern, latest_time.isoformat())
                        elif not last_result_time and newest_results:
                            for result in newest_results:
                                repo = result.get("repository", {})
                                if repo:
                                    updated_at = repo.get("updated_at", "")
                                    if updated_at:
                                        try:
                                            result_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                                            if latest_time is None or result_time > latest_time:
                                                latest_time = result_time
                                        except:
                                            pass
                            if latest_time:
                                self.state_manager.set_last_result_time(pattern, latest_time.isoformat())
                        
                        if last_page > 0:
                            print(f"  🔍 Phase 2: Continuing from page {last_page + 1} for remaining pages (using original query)...")
                            remaining_results = self.search_all_types(
                                pattern, 
                                max_results_per_pattern,
                                start_page=last_page + 1
                            )
                            
                            remaining_new = []
                            for result in remaining_results:
                                repo = result.get("repository", {})
                                repo_full_name = repo.get("full_name", "") if repo else ""
                                
                                if self.state_manager.is_new_result(result):
                                    result["matched_pattern"] = pattern
                                    remaining_new.append(result)
                                    self.state_manager.mark_as_seen(result)
                                    
                                    if repo_full_name and self.state_manager.is_new_repo(result):
                                        self.state_manager.mark_repo_as_seen(result)
                                elif repo_full_name and self.state_manager.is_new_repo(result):
                                    self.state_manager.mark_repo_as_seen(result)
                            
                            pattern_results.extend(remaining_results)
                            new_results.extend(remaining_new)
                            print(f"  ✓ Found {len(remaining_results)} results ({len(remaining_new)} new) from remaining pages")
                            
                            if remaining_results:
                                pages_fetched = (len(remaining_results) // RESULTS_PER_PAGE) + (1 if len(remaining_results) % RESULTS_PER_PAGE > 0 else 0)
                                new_last_page = last_page + pages_fetched
                                self.state_manager.set_last_page(pattern, new_last_page)
                            else:
                                print(f"  ℹ️  No more results found. Reached end of search for this pattern.")
                        else:
                            if newest_results:
                                total_pages_newest = (len(newest_results) // RESULTS_PER_PAGE) + (1 if len(newest_results) % RESULTS_PER_PAGE > 0 else 0)
                                if total_pages_newest > 0:
                                    self.state_manager.set_last_page(pattern, total_pages_newest)
                                    print(f"  ℹ️  Saved last page ({total_pages_newest}) for next iteration")
                            else:
                                print(f"  ℹ️  No results found. Will search from page 1 next time.")
                    else:
                        results = self.search_all_types(pattern, max_results_per_pattern, start_page=1)
                        pattern_results = results
                        
                        for result in results:
                            if self.state_manager:
                                if self.state_manager.is_new_result(result):
                                    result["matched_pattern"] = pattern
                                    new_results.append(result)
                                    self.state_manager.mark_as_seen(result)
                            else:
                                repo_full_name = result.get("repository", {}).get("full_name", "")
                                file_path = result.get("path", "")
                                unique_key = f"{repo_full_name}:{file_path}"
                                
                                if unique_key not in seen_keys:
                                    seen_keys.add(unique_key)
                                    result["matched_pattern"] = pattern
                                    new_results.append(result)
                    
                    all_results.extend(new_results)
                    print(f"  ✓ Total: {len(pattern_results)} results ({len(new_results)} new)\n")
                    
                    if new_results and output_handler and continuous:
                        print(f"  💾 Saving {len(new_results)} new results immediately...")
                        try:
                            enriched = self.enrich_results(new_results, fetch_content)
                            
                            pattern_map = {}
                            for r in new_results:
                                repo_full_name = r.get('repository', {}).get('full_name', '')
                                search_type = r.get("search_type", "code")
                                if search_type == "code":
                                    file_path = r.get('path', '')
                                    key = f"{repo_full_name}:{file_path}"
                                elif search_type == "issues":
                                    issue_number = r.get('number', '')
                                    key = f"{repo_full_name}:issue:{issue_number}"
                                elif search_type == "commits":
                                    commit_sha = r.get('sha', '')
                                    key = f"{repo_full_name}:commit:{commit_sha}"
                                else:
                                    key = f"{repo_full_name}:repo"
                                pattern_map[key] = r.get("matched_pattern", "unknown")
                            
                            for item in enriched:
                                search_type = item.get("search_type", "code")
                                repo_full_name = item["repository"]["full_name"]
                                
                                if search_type == "code":
                                    file_path = item.get("file", {}).get("path", "")
                                    key = f"{repo_full_name}:{file_path}"
                                elif search_type == "issue":
                                    issue_number = item.get("issue", {}).get("number", "")
                                    key = f"{repo_full_name}:issue:{issue_number}"
                                elif search_type == "commit":
                                    commit_sha = item.get("commit", {}).get("sha", "")
                                    key = f"{repo_full_name}:commit:{commit_sha}"
                                else:
                                    key = f"{repo_full_name}:repo"
                                
                                item["matched_pattern"] = pattern_map.get(key, "unknown")
                            
                            output_handler.save(enriched)
                            output_handler.existing_data.extend(enriched)
                            if self.state_manager:
                                self.state_manager.save_state()
                        except Exception as e:
                            print(f"  ⚠️  Error saving results: {e}")
                    
                except Exception as e:
                    print(f"  ✗ Error: {e}\n")
            
            if not continuous:
                break
            
            if all_results:
                print(f"\n{'='*60}")
                print(f"📊 Found {len(all_results)} new results in this iteration")
                print(f"{'='*60}\n")
                
                if not output_handler:
                    print("Enriching results with metadata...")
                    enriched = self.enrich_results(all_results, fetch_content)
                    
                    pattern_map = {}
                    for r in all_results:
                        repo_full_name = r.get('repository', {}).get('full_name', '')
                        search_type = r.get("search_type", "code")
                        if search_type == "code":
                            file_path = r.get('path', '')
                            key = f"{repo_full_name}:{file_path}"
                        elif search_type == "issues":
                            issue_number = r.get('number', '')
                            key = f"{repo_full_name}:issue:{issue_number}"
                        elif search_type == "commits":
                            commit_sha = r.get('sha', '')
                            key = f"{repo_full_name}:commit:{commit_sha}"
                        else:
                            key = f"{repo_full_name}:repo"
                        pattern_map[key] = r.get("matched_pattern", "unknown")
                    
                    for item in enriched:
                        search_type = item.get("search_type", "code")
                        repo_full_name = item["repository"]["full_name"]
                        
                        if search_type == "code":
                            file_path = item.get("file", {}).get("path", "")
                            key = f"{repo_full_name}:{file_path}"
                        elif search_type == "issue":
                            issue_number = item.get("issue", {}).get("number", "")
                            key = f"{repo_full_name}:issue:{issue_number}"
                        elif search_type == "commit":
                            commit_sha = item.get("commit", {}).get("sha", "")
                            key = f"{repo_full_name}:commit:{commit_sha}"
                        else:
                            key = f"{repo_full_name}:repo"
                        
                        item["matched_pattern"] = pattern_map.get(key, "unknown")
                else:
                    if not output_handler.append_mode:
                        print("Enriching results with metadata...")
                        enriched = self.enrich_results(all_results, fetch_content)
                        output_handler.save(enriched)
                        if self.state_manager:
                            self.state_manager.save_state()
            else:
                print(f"\n  ℹ️  No new results in this iteration")
            
            if self.state_manager:
                stats = self.state_manager.get_stats()
                print(f"\n  📊 Total unique results seen: {stats['total_seen']}")
            
            if not continuous:
                break
            
            print(f"\n  ⏳ Waiting before next iteration... (Press Ctrl+C to stop)")
            import time
            time.sleep(5)
        
        if not all_results:
            print("No results found.")
            return []
        
        if not continuous or not output_handler:
            print(f"\n{'='*60}")
            print(f"📊 Total unique results: {len(all_results)}")
            print(f"{'='*60}\n")
            print("Enriching results with metadata...")
            
            enriched = self.enrich_results(all_results, fetch_content)
            
            pattern_map = {}
            for r in all_results:
                repo_full_name = r.get('repository', {}).get('full_name', '')
                search_type = r.get("search_type", "code")
                if search_type == "code":
                    file_path = r.get('path', '')
                    key = f"{repo_full_name}:{file_path}"
                elif search_type == "issues":
                    issue_number = r.get('number', '')
                    key = f"{repo_full_name}:issue:{issue_number}"
                elif search_type == "commits":
                    commit_sha = r.get('sha', '')
                    key = f"{repo_full_name}:commit:{commit_sha}"
                else:
                    key = f"{repo_full_name}:repo"
                pattern_map[key] = r.get("matched_pattern", "unknown")
            
            for item in enriched:
                search_type = item.get("search_type", "code")
                repo_full_name = item["repository"]["full_name"]
                
                if search_type == "code":
                    file_path = item.get("file", {}).get("path", "")
                    key = f"{repo_full_name}:{file_path}"
                elif search_type == "issue":
                    issue_number = item.get("issue", {}).get("number", "")
                    key = f"{repo_full_name}:issue:{issue_number}"
                elif search_type == "commit":
                    commit_sha = item.get("commit", {}).get("sha", "")
                    key = f"{repo_full_name}:commit:{commit_sha}"
                else:
                    key = f"{repo_full_name}:repo"
                
                item["matched_pattern"] = pattern_map.get(key, "unknown")
            
            return enriched
        
        return []

