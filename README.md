# 🔍 GitHub OSINT Intelligence Tool

A powerful **Open Source Intelligence (OSINT)** tool for searching and analyzing GitHub repositories, code patterns, files, and commits. Discover sensitive information, security vulnerabilities, API keys, private credentials, and dangerous code patterns across GitHub's public repositories.

---

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Examples](#-examples)
- [Advanced Features](#-advanced-features)
- [Output Formats](#-output-formats)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Capabilities
- **Multi-Source Search**: Search across code, repositories, issues, and commits
- **Pattern Detection**: Automatically detect dangerous patterns like private keys, mnemonics, API keys
- **File-Based Searching**: Find specific files by name (e.g., `.env`, `hardhat.config.js`, `.git`)
- **Content Extraction**: Fetch and analyze file contents directly from repositories
- **Smart Rate Limiting**: Automatic handling of GitHub API rate limits
- **State Management**: Track searched patterns and avoid duplicate results
- **Continuous Monitoring**: Run continuous searches with automatic state persistence

### 📊 Output Options
- **JSON Format**: Structured data export for programmatic analysis
- **CSV Format**: Spreadsheet-compatible export for data analysis
- **Enriched Metadata**: Enhanced results with repository stats, file details, and timestamps

### 🔐 Security Features
- Detects hardcoded credentials (API keys, mnemonics, private keys)
- Identifies sensitive configuration files
- Searches for dangerous code patterns
- Tracks repository updates for new vulnerable code

### ⚙️ Advanced Options
- Interactive mode for real-time queries
- Auto-search for all dangerous patterns
- Continuous monitoring mode with state persistence
- Customizable result limits (up to 1,000 per pattern)
- Optional file content fetching

---

## 📌 Prerequisites

Before installing, ensure you have:

### Required
- **Python 3.8 or higher**
- **GitHub Account** (for API token)
- **Internet Connection** (for GitHub API access)

### Recommended
- Git (for cloning the repository)
- pip (usually comes with Python)
- Virtual Environment (for isolated dependencies)

---

## 🚀 Installation

### Step 1: Install Python

#### **Windows**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **Important**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   pip --version
   ```

#### **macOS**
Using Homebrew (recommended):
```bash
brew install python3
```

Or download from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python3 --version
pip3 --version
```

#### **Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
python3 --version
pip3 --version
```

#### **Linux (Fedora/RHEL)**
```bash
sudo dnf install python3 python3-pip -y
python3 --version
pip3 --version
```

---

### Step 2: Clone the Repository

```bash
# Using Git
git clone https://github.com/amirofski/github_osint.git
cd github_osint

# OR download the ZIP file and extract it
```

---

### Step 3: Create Virtual Environment (Recommended)

#### **Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

#### **macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal should show `(venv)` prefix.

---

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - HTTP library for API calls
- `python-dotenv` - Environment variable management

---

### Step 5: Get GitHub API Token

1. Go to [GitHub Settings - Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "OSINT Tool")
4. Select scopes:
   - ✅ `public_repo` - Access public repositories
   - ✅ `read:user` - Read user data
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

---

### Step 6: Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# Windows
echo GITHUB_TOKEN=your_token_here > .env
echo OUTPUT_FORMAT=json >> .env
echo OUTPUT_FILE=results.json >> .env

# macOS/Linux
cat > .env << EOF
GITHUB_TOKEN=your_token_here
OUTPUT_FORMAT=json
OUTPUT_FILE=results.json
EOF
```

**Replace `your_token_here` with your actual GitHub token**

Or manually create `.env` with this content:
```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OUTPUT_FORMAT=json
OUTPUT_FILE=results.json
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `GITHUB_TOKEN` | GitHub API token (required) | None | `ghp_xxx...` |
| `OUTPUT_FORMAT` | Output file format | `json` | `json` or `csv` |
| `OUTPUT_FILE` | Default output filename | Auto-generated | `results.json` |

---

## 📖 Usage

### **Interactive Mode**

Best for exploring and testing queries:

```bash
python main.py --interactive
```

Interactive commands:
- Type search queries directly
- Use `auto` to search all dangerous patterns
- Use `exit`, `quit`, or `q` to exit
- Customize results limit, format, and content fetching

---

### **CLI Mode - Basic Search**

Search for specific patterns:

```bash
# Search for private keys
python main.py "privateKey"

# Search for specific files
python main.py filename:hardhat.config.js

# Search with custom max results
python main.py "mnemonic" --max-results 500

# Output to CSV
python main.py "alchemy" --format csv --output results.csv
```

---

### **CLI Mode - Auto-Search**

Search all dangerous patterns automatically:

```bash
# Single run
python main.py --auto

# With custom settings
python main.py --auto --max-results 200 --format csv --output danger.csv

# Skip file content fetching (faster)
python main.py --auto --no-fetch-content
```

---

### **Continuous Monitoring Mode**

Keep searching and tracking new results:

```bash
# Start continuous monitoring
python main.py --auto --continuous --output ongoing_results.json

# With state file for persistence
python main.py --auto --continuous --state-file my_state.json --output results.json
```

Press `Ctrl+C` to stop continuous mode.

---

## 💡 Examples

### Example 1: Search for Hardcoded API Keys

```bash
python main.py "infura" --max-results 100 --format json --output infura_keys.json
```

**Output**: All repositories containing "infura" with file content and metadata.

---

### Example 2: Find Environment Configuration Files

```bash
python main.py filename:.env --max-results 500
```

**Output**: All `.env` files found publicly on GitHub.

---

### Example 3: Search for Private Key Patterns

```bash
python main.py "-----BEGIN PRIVATE KEY-----" --max-results 200 --output pem_keys.csv --format csv
```

---

### Example 4: Comprehensive Pattern Detection

```bash
python main.py --auto --continuous \
  --max-results 100 \
  --format json \
  --output comprehensive_scan.json \
  --state-file tracking.json
```

---

### Example 5: Interactive Session with Customization

```bash
python main.py --interactive
```

Then interact:
```
Enter search query: filename:hardhat.config.js
Max results (default 100, max 1000): 50
Fetch file content? (y/n, default: y): y
Output format (json/csv, default: json): json
```

---

## 🔧 Advanced Features

### State Management

Track what you've already searched to avoid duplicates:

```bash
python main.py --auto --continuous \
  --state-file github_intel_state.json \
  --output results.json
```

**State file tracks**:
- Searched patterns
- Last page processed
- Last result time
- Unique repositories seen

---

### Rate Limit Handling

The tool automatically manages GitHub API rate limits:
- **Authenticated**: 5,000 requests/hour
- **Unauthenticated**: 60 requests/hour (not recommended)
- Auto-waits when limit is approaching
- Handles rate limit reset gracefully

---

### Content Fetching Control

```bash
# Fetch content (default) - more data, slower
python main.py "privateKey"

# Skip content - faster, basic info only
python main.py "privateKey" --no-fetch-content
```

---

## 📊 Output Formats

### JSON Format (Default)

```json
[
  {
    "search_type": "code",
    "repository": {
      "name": "example-repo",
      "owner": "username",
      "full_name": "username/example-repo",
      "url": "https://github.com/username/example-repo",
      "stars": 150,
      "forks": 45,
      "language": "JavaScript",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    "file": {
      "name": ".env",
      "path": ".env",
      "url": "https://github.com/username/example-repo/blob/main/.env",
      "sha": "abc123...",
      "content": "PRIVATE_KEY=0x1234567890..."
    },
    "matched_pattern": "filename:.env"
  }
]
```

### CSV Format

```csv
search_type,repo_owner,repo_name,file_name,file_path,file_url,repo_url,content,matched_pattern
code,username,example-repo,.env,.env,https://...,https://...,PRIVATE_KEY=0x...,filename:.env
```

---

## 🐛 Troubleshooting

### ❌ Error: "GITHUB_TOKEN environment variable is required"

**Solution**:
```bash
# Create .env file with your token
echo GITHUB_TOKEN=your_token_here > .env

# Or set environment variable directly
# Windows
set GITHUB_TOKEN=your_token_here
python main.py --auto

# macOS/Linux
export GITHUB_TOKEN=your_token_here
python main.py --auto
```

---

### ❌ Error: "Rate limit exceeded"

**Solution**: The tool automatically waits, but you can:
1. Use fewer results: `--max-results 50`
2. Use `--no-fetch-content` to reduce API calls
3. Wait 1 hour for rate limit reset
4. Use a token with higher rate limits

---

### ❌ Error: "No module named 'requests'"

**Solution**:
```bash
pip install -r requirements.txt
```

---

### ❌ Error: "ModuleNotFoundError: No module named 'dotenv'"

**Solution**:
```bash
pip install python-dotenv
# or reinstall all
pip install -r requirements.txt
```

---

### ❌ Error: "Invalid query format"

**Solution**: Use proper GitHub search syntax:
```bash
# ✅ Correct
python main.py "privateKey"
python main.py filename:hardhat.config.js
python main.py filename:.env

# ❌ Avoid
python main.py "user@email.com" # Special characters need escaping
```

---

### ❌ Error: "Connection timeout"

**Solution**:
1. Check internet connection
2. GitHub API might be down
3. Try again in a few moments
4. Use `--no-fetch-content` to reduce time

---

## 📁 Project Structure

```
github_osint/
├── main.py                 # Main entry point, CLI interface
├── github_client.py        # GitHub API interaction
├── search_engine.py        # Search logic and pattern matching
├── config.py               # Configuration and constants
├── patterns.py             # Dangerous patterns definition
├── output_handler.py       # Result export (JSON/CSV)
├── state_manager.py        # State persistence for tracking
├── extractor.py            # Data extraction utilities
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create locally)
└── README.md              # This file
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more dangerous patterns
- [ ] Support for additional output formats (XML, SQLite)
- [ ] Proxy support
- [ ] Database integration
- [ ] Web UI
- [ ] Result filtering and analytics

---

## 📝 License

This project is provided for educational and security research purposes.

**Disclaimer**: Use responsibly and only on repositories where you have permission. Unauthorized access to computer systems is illegal.

---

## ⚠️ Legal & Ethical Notice

- **Educational Purpose Only**: This tool is designed for security researchers and authorized penetration testing.
- **Legal Compliance**: Only search public repositories and ensure you have authorization.
- **Responsible Disclosure**: If you find real vulnerabilities, report them to the affected parties.
- **No Warranty**: Use at your own risk. The author assumes no liability.

---

## 🔗 Quick Links

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Token Settings](https://github.com/settings/tokens)
- [GitHub Search Syntax](https://docs.github.com/en/search-github/searching-on-github/searching-code)

---

## 📞 Support

For issues and questions:
1. Check the **Troubleshooting** section above
2. Review GitHub Issues
3. Check existing documentation
4. Create a new issue with detailed information

---

## 🙏 Acknowledgments

Built for security researchers and the open-source community to discover and remediate vulnerabilities in publicly shared code.

---

**Last Updated**: January 2026  
**Version**: 1.0.0  
**Author**: amirofski
