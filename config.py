import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

_package_dir = Path(__file__).parent
_project_root = _package_dir.parent

_env_files = [
    _package_dir / ".env",
    _project_root / ".env",
]

for env_file in _env_files:
    if env_file.exists():
        load_dotenv(env_file)
        break

GITHUB_API_BASE = "https://api.github.com"
GITHUB_SEARCH_API = f"{GITHUB_API_BASE}/search"
GITHUB_REPOS_API = f"{GITHUB_API_BASE}/repos"

RATE_LIMIT_AUTHENTICATED = 5000
RATE_LIMIT_UNAUTHENTICATED = 60

RESULTS_PER_PAGE = 100
MAX_RESULTS_PER_QUERY = 1000

def get_github_token() -> Optional[str]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError(
            "GITHUB_TOKEN environment variable is required. "
            "Get a token from: https://github.com/settings/tokens\n"
            f"Or create a .env file in {_package_dir} or {_project_root} with: GITHUB_TOKEN=your_token"
        )
    return token

def get_output_format() -> str:
    return os.getenv("OUTPUT_FORMAT", "json").lower()

def get_output_file() -> Optional[str]:
    return os.getenv("OUTPUT_FILE")

