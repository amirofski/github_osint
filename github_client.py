import time
import requests
from typing import Dict, List, Optional, Any
from config import (
    GITHUB_API_BASE,
    GITHUB_SEARCH_API,
    get_github_token,
    RATE_LIMIT_AUTHENTICATED,
    RESULTS_PER_PAGE
)

class GitHubClient:
    def __init__(self):
        self.token = get_github_token()
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Intelligence-Tool"
        })
        self.rate_limit_remaining = RATE_LIMIT_AUTHENTICATED
        self.rate_limit_reset = 0
        self.last_request_time = 0
        self.min_request_interval = 0.1

    def _check_rate_limit(self):
        if self.rate_limit_remaining <= 10:
            if time.time() < self.rate_limit_reset:
                wait_time = max(0, self.rate_limit_reset - time.time() + 1)
                if wait_time > 0:
                    print(f"Rate limit low. Waiting {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
            else:
                self._update_rate_limit()

        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

    def _update_rate_limit(self, response: Optional[requests.Response] = None):
        if response:
            remaining = response.headers.get("X-RateLimit-Remaining")
            reset = response.headers.get("X-RateLimit-Reset")
            if remaining:
                self.rate_limit_remaining = int(remaining)
            if reset:
                self.rate_limit_reset = int(reset)

    def _make_request(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        self._check_rate_limit()
        
        response = self.session.get(url, params=params)
        self.last_request_time = time.time()
        self._update_rate_limit(response)
        
        if response.status_code == 403:
            if "rate limit" in response.text.lower():
                wait_time = max(0, self.rate_limit_reset - time.time() + 1)
                if wait_time > 0:
                    print(f"Rate limit exceeded. Waiting {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Rate limit reset time has passed. Retrying...")
                    time.sleep(1)
                return self._make_request(url, params)
            else:
                raise Exception(f"Forbidden: {response.text}")
        
        response.raise_for_status()
        return response

    def search_code(self, query: str, max_results: int = 1000, start_page: int = 1, sort: str = None, order: str = None) -> List[Dict[str, Any]]:
        all_results = []
        page = start_page
        
        print(f"Searching GitHub for: {query}")
        if start_page > 1:
            print(f"  Starting from page {start_page}")
        
        while len(all_results) < max_results:
            params = {
                "q": query,
                "per_page": min(RESULTS_PER_PAGE, max_results - len(all_results)),
                "page": page
            }
            
            if sort:
                params["sort"] = sort
            if order:
                params["order"] = order
            
            try:
                response = self._make_request(f"{GITHUB_SEARCH_API}/code", params)
                data = response.json()
                
                items = data.get("items", [])
                if not items:
                    break
                
                all_results.extend(items)
                print(f"  Found {len(all_results)} results so far...")
                
                if len(items) < RESULTS_PER_PAGE:
                    break
                
                page += 1
                
            except requests.exceptions.RequestException as e:
                if "422" in str(e):
                    print(f"  ⚠️  Invalid query format. Skipping this pattern.")
                    break
                print(f"Error fetching page {page}: {e}")
                break
        
        return all_results[:max_results]

    def search_repositories(self, query: str, max_results: int = 1000) -> List[Dict[str, Any]]:
        all_results = []
        page = 1
        
        print(f"Searching GitHub repositories for: {query}")
        
        while len(all_results) < max_results:
            params = {
                "q": query,
                "per_page": min(RESULTS_PER_PAGE, max_results - len(all_results)),
                "page": page,
                "sort": "updated",
                "order": "desc"
            }
            
            try:
                response = self._make_request(f"{GITHUB_SEARCH_API}/repositories", params)
                data = response.json()
                
                items = data.get("items", [])
                if not items:
                    break
                
                all_results.extend(items)
                print(f"  Found {len(all_results)} repositories so far...")
                
                if len(items) < RESULTS_PER_PAGE:
                    break
                
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page}: {e}")
                break
        
        return all_results[:max_results]

    def search_issues(self, query: str, max_results: int = 1000, start_page: int = 1, sort: str = "updated", order: str = "desc") -> List[Dict[str, Any]]:
        all_results = []
        page = start_page
        
        print(f"Searching GitHub issues for: {query}")
        if start_page > 1:
            print(f"  Starting from page {start_page}")
        
        while len(all_results) < max_results:
            params = {
                "q": query,
                "per_page": min(RESULTS_PER_PAGE, max_results - len(all_results)),
                "page": page,
                "sort": sort,
                "order": order
            }
            
            try:
                response = self._make_request(f"{GITHUB_SEARCH_API}/issues", params)
                data = response.json()
                
                items = data.get("items", [])
                if not items:
                    break
                
                all_results.extend(items)
                print(f"  Found {len(all_results)} issues so far...")
                
                if len(items) < RESULTS_PER_PAGE:
                    break
                
                page += 1
                
            except requests.exceptions.RequestException as e:
                if "422" in str(e):
                    print(f"  ⚠️  Invalid query format. Skipping this pattern.")
                    break
                print(f"Error fetching page {page}: {e}")
                break
        
        return all_results[:max_results]
    
    def search_commits(self, query: str, max_results: int = 1000, start_page: int = 1, sort: str = "author-date", order: str = "desc") -> List[Dict[str, Any]]:
        all_results = []
        page = start_page
        
        print(f"Searching GitHub commits for: {query}")
        if start_page > 1:
            print(f"  Starting from page {start_page}")
        
        while len(all_results) < max_results:
            params = {
                "q": query,
                "per_page": min(RESULTS_PER_PAGE, max_results - len(all_results)),
                "page": page,
                "sort": sort,
                "order": order
            }
            
            try:
                response = self._make_request(f"{GITHUB_SEARCH_API}/commits", params)
                data = response.json()
                
                items = data.get("items", [])
                if not items:
                    break
                
                all_results.extend(items)
                print(f"  Found {len(all_results)} commits so far...")
                
                if len(items) < RESULTS_PER_PAGE:
                    break
                
                page += 1
                
            except requests.exceptions.RequestException as e:
                if "422" in str(e):
                    print(f"  ⚠️  Invalid query format. Skipping this pattern.")
                    break
                print(f"Error fetching page {page}: {e}")
                break
        
        return all_results[:max_results]

    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
        response = self._make_request(url)
        return response.json()

    def get_file_content(self, owner: str, repo: str, path: str) -> Optional[str]:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
        
        try:
            response = self._make_request(url)
            data = response.json()
            
            if isinstance(data, list):
                return None
            
            if isinstance(data, dict) and data.get("type") == "file":
                import base64
                content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
                return content
            return None
            
        except requests.exceptions.RequestException as e:
            if "404" in str(e):
                return None
            print(f"Error fetching file {owner}/{repo}/{path}: {e}")
            return None
        except (KeyError, TypeError, ValueError) as e:
            return None

    def get_rate_limit_status(self) -> Dict[str, Any]:
        url = f"{GITHUB_API_BASE}/rate_limit"
        response = self._make_request(url)
        return response.json()

