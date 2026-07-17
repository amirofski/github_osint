# 🎯 Usage Examples & Practical Scenarios

Real-world examples and use cases for the GitHub OSINT Intelligence Tool.

---

## 📚 Table of Contents

1. [Basic Searches](#basic-searches)
2. [Security Vulnerability Detection](#security-vulnerability-detection)
3. [Configuration File Hunting](#configuration-file-hunting)
4. [Cryptocurrency & API Keys](#cryptocurrency--api-keys)
5. [Advanced Searches](#advanced-searches)
6. [Continuous Monitoring](#continuous-monitoring)
7. [Data Analysis](#data-analysis)

---

## 🔍 Basic Searches

### Example 1: Simple Pattern Search

Search for repositories containing the word "privateKey":

```bash
python main.py "privateKey"
```

**Output:**
```json
[
  {
    "search_type": "code",
    "repository": {
      "name": "web3-wallet",
      "owner": "devuser",
      "full_name": "devuser/web3-wallet",
      "url": "https://github.com/devuser/web3-wallet",
      "stars": 42,
      "language": "JavaScript"
    },
    "file": {
      "name": "wallet.js",
      "path": "src/wallet.js",
      "content": "const privateKey = '0x1234...';"
    }
  }
]
```

---

### Example 2: Filename Search

Find all `.env` files:

```bash
python main.py filename:.env --max-results 100
```

**Use Cases:**
- Detect exposed environment files
- Find configuration files with secrets
- Identify development artifacts in public repos

---

### Example 3: Repository Search

Search for repositories related to blockchain:

```bash
python main.py repo:ethereum --max-results 50
```

---

### Example 4: Search with Custom Results Limit

```bash
python main.py "API_KEY" --max-results 500
```

Retrieve up to 500 results instead of default 100.

---

## 🔐 Security Vulnerability Detection

### Example 1: Find Exposed AWS Keys

```bash
python main.py "AKIA" --max-results 200 --format json --output aws_keys.json
```

**What it detects:**
- AWS Access Key IDs (start with AKIA)
- Exposed credentials in code
- Misconfigured IAM tokens

---

### Example 2: Detect Hardcoded Database Passwords

```bash
python main.py "mongodb+srv://" --max-results 150
```

**What it finds:**
- MongoDB connection strings with credentials
- Database URLs with embedded passwords
- Exposed connection details

---

### Example 3: Search for Private SSH Keys

```bash
python main.py "-----BEGIN PRIVATE KEY-----" --max-results 300 --format csv --output ssh_keys.csv
```

**Detects:**
- RSA Private Keys
- DSA Private Keys
- OpenSSH format private keys
- PEM encoded keys

---

### Example 4: Find SQL Injection Vulnerable Code Patterns

```bash
python main.py "SELECT * FROM" --max-results 200
```

Look for patterns that might indicate SQL injection vulnerabilities.

---

## 📁 Configuration File Hunting

### Example 1: Find Docker Secrets

```bash
python main.py filename:Dockerfile --max-results 100
```

Search for Dockerfiles that might contain exposed secrets:

```bash
python main.py "ENV SECRET" --max-results 100
```

---

### Example 2: Find Kubernetes Secrets

```bash
python main.py filename:secrets.yaml --max-results 100
```

```bash
python main.py "apiVersion: v1" --max-results 200
```

---

### Example 3: Find Package Manager Credentials

```bash
python main.py filename:.npmrc --max-results 50
```

```bash
python main.py filename:.pypirc --max-results 50
```

```bash
python main.py filename:settings.xml --max-results 50
```

---

### Example 4: Find Configuration Files

```bash
# Application configuration
python main.py filename:config.yml --max-results 100
python main.py filename:settings.json --max-results 100

# Deployment files
python main.py filename:.env.production --max-results 100

# API configuration
python main.py filename:api.config --max-results 50
```

---

## 💰 Cryptocurrency & API Keys

### Example 1: Find Hardhat Configuration Files

Hardhat is an Ethereum development framework that often contains private keys:

```bash
python main.py filename:hardhat.config.js --max-results 200
```

---

### Example 2: Search for Mnemonic Phrases

BIP39 mnemonic phrases for wallet recovery:

```bash
python main.py "mnemonic" --max-results 150 --format json --output mnemonics.json
```

---

### Example 3: Find Wallet Private Keys

```bash
python main.py "0x[a-fA-F0-9]{64}" --max-results 200
```

---

### Example 4: Detect Infura & Alchemy API Keys

```bash
# Infura keys
python main.py "infura" --max-results 100

# Alchemy keys
python main.py "alchemy" --max-results 100

# Together
python main.py filename:infura --max-results 150
python main.py filename:alchemy --max-results 150
```

---

### Example 5: Find Etherscan API Keys

```bash
python main.py "ETHERSCAN" --max-results 100
```

---

## 🚀 Advanced Searches

### Example 1: Multi-Pattern Auto-Search

Search all dangerous patterns automatically:

```bash
python main.py --auto --max-results 100
```

**Searches:**
- Dangerous filenames (.env, .git, secrets.yaml, etc.)
- Dangerous code patterns (privateKey, mnemonic, etc.)
- API credentials (Infura, Alchemy, etc.)
- SSH/RSA keys
- And more...

---

### Example 2: Auto-Search with CSV Output

```bash
python main.py --auto --max-results 200 --format csv --output vulnerability_scan.csv
```

Perfect for:
- Data analysis in Excel
- Sharing with security teams
- Creating reports

---

### Example 3: Search Without Fetching Content (Faster)

```bash
python main.py "privateKey" --no-fetch-content --max-results 500
```

**Trade-off:**
- ✅ Much faster (fewer API calls)
- ✅ Scan more results
- ❌ No file content included

---

### Example 4: Combine Multiple Search Terms

```bash
# Search for potential secrets
python main.py "secret" --max-results 200

# Search for tokens
python main.py "token" --max-results 200

# Search for credentials
python main.py "credentials" --max-results 200
```

---

## 📊 Continuous Monitoring

### Example 1: Basic Continuous Mode

Run searches continuously every 5 seconds:

```bash
python main.py --auto --continuous --output ongoing_results.json
```

**Features:**
- Keeps running until Ctrl+C
- Saves results to file
- Tracks new patterns automatically

---

### Example 2: Continuous with State Persistence

Track what you've searched to avoid duplicates:

```bash
python main.py --auto --continuous \
  --state-file tracking.json \
  --output results.json \
  --max-results 50
```

**Tracks:**
- Searched patterns
- Last page processed
- Last result timestamp
- Unique repositories

---

### Example 3: Specific Pattern Continuous Search

Monitor for new Ethereum private keys:

```bash
python main.py "0x[a-fA-F0-9]{64}" --continuous \
  --state-file ethereum_monitor.json \
  --output ethereum_keys.json \
  --max-results 100
```

---

### Example 4: Stop and Resume

```bash
# Start monitoring (runs for a while)
python main.py --auto --continuous --state-file state.json

# Later, resume from where you left off
python main.py --auto --continuous --state-file state.json
```

---

## 📈 Data Analysis

### Example 1: Export to CSV for Analysis

```bash
python main.py --auto --format csv --output analysis.csv
```

Then analyze in:
- Microsoft Excel
- Google Sheets
- Pandas (Python)
- Power BI

---

### Example 2: JSON Export for Programmatic Analysis

```bash
python main.py "privateKey" --format json --output results.json
```

**Analyze with Python:**
```python
import json

with open('results.json', 'r') as f:
    data = json.load(f)

# Count by repository
repos = {}
for item in data:
    repo = item['repository']['full_name']
    repos[repo] = repos.get(repo, 0) + 1

# Find most vulnerable repos
top_repos = sorted(repos.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 Most Vulnerable Repositories:")
for repo, count in top_repos:
    print(f"  {repo}: {count} findings")
```

---

### Example 3: Security Audit Report

```bash
# 1. Run comprehensive scan
python main.py --auto --format json --output audit.json

# 2. Analyze results
python analyze_audit.py audit.json

# 3. Generate report
python generate_report.py audit.json > security_report.html
```

---

## 🎓 Learning & Exploration

### Example 1: Explore Popular Patterns

See what patterns are most commonly exposed:

```bash
python main.py "password" --max-results 100
python main.py "secret" --max-results 100
python main.py "token" --max-results 100
```

---

### Example 2: Repository Security Research

Audit a specific user's repositories:

```bash
python main.py "repo:username/repo-name" --max-results 50
```

---

### Example 3: Language-Specific Searches

```bash
# JavaScript
python main.py filename:.env --max-results 50

# Python
python main.py filename:settings.py --max-results 50

# Java
python main.py filename:application.properties --max-results 50

# Go
python main.py filename:.env.go --max-results 50
```

---

## 🔄 Workflow Examples

### Complete Security Audit Workflow

```bash
#!/bin/bash

# 1. Full scan of all patterns
echo "🔍 Running comprehensive scan..."
python main.py --auto --max-results 100 --format json --output scan_$(date +%Y%m%d).json

# 2. Export to CSV for analysis
echo "📊 Exporting to CSV..."
python main.py --auto --max-results 100 --format csv --output analysis_$(date +%Y%m%d).csv

# 3. Archive results
echo "📦 Archiving results..."
tar -czf results_$(date +%Y%m%d).tar.gz scan_*.json analysis_*.csv

echo "✅ Audit complete!"
```

---

### Continuous Monitoring Workflow

```bash
#!/bin/bash

# Monitor for new vulnerabilities
python main.py --auto --continuous \
  --state-file monitoring_state.json \
  --output monitoring_$(date +%Y%m%d).json \
  --max-results 50

# On exit, analyze results
if [ -f "monitoring_$(date +%Y%m%d).json" ]; then
    python analyze_results.py monitoring_$(date +%Y%m%d).json
fi
```

---

## 💡 Pro Tips

### 1. Use Multiple Terminal Windows

```bash
# Terminal 1: Monitor for AWS keys
python main.py "AKIA" --continuous --output aws_monitor.json

# Terminal 2: Monitor for private keys
python main.py "BEGIN PRIVATE KEY" --continuous --output ssh_monitor.json
```

---

### 2. Combine with Other Tools

```bash
# Export and process with grep
python main.py "token" --format csv --output results.csv
grep "high_value" results.csv

# Process with jq (JSON)
python main.py "privateKey" --format json --output results.json
jq '.[] | select(.repository.stars > 100)' results.json
```

---

### 3. Create Custom Analysis Script

```python
import json
import sys

with open(sys.argv[1], 'r') as f:
    results = json.load(f)

# Analyze by language
by_language = {}
for item in results:
    lang = item['repository'].get('language', 'Unknown')
    by_language[lang] = by_language.get(lang, 0) + 1

print("Results by Language:")
for lang, count in sorted(by_language.items(), key=lambda x: x[1], reverse=True):
    print(f"  {lang}: {count}")
```

---

### 4. Schedule Regular Scans (Linux/macOS)

Add to crontab:
```bash
crontab -e

# Run daily at 2 AM
0 2 * * * cd /path/to/github_osint && python main.py --auto --output results_$(date +\%Y\%m\%d).json
```

---

### 5. Integrate with Security Tools

```bash
# Export for SIEM
python main.py --auto --format json --output siem_import.json

# Send to Slack
python main.py --auto --format json --output results.json && \
python notify_slack.py results.json
```

---

## 🎯 Common Scenarios

### Scenario 1: Suspected Data Breach

```bash
# Search for compromised company data
python main.py "company_name" --max-results 500 --format json --output breach_search.json

# Analyze results
python -c "
import json
with open('breach_search.json') as f:
    data = json.load(f)
print(f'Found {len(data)} potential leaks')
for item in data[:10]:
    print(f\"  - {item['repository']['full_name']}\")
"
```

---

### Scenario 2: Third-Party Library Audit

```bash
# Check if dependency leaked secrets
python main.py "library_name" --max-results 200 --format csv --output library_audit.csv
```

---

### Scenario 3: Developer Education

Show developers what NOT to commit:

```bash
python main.py "password" --max-results 50
python main.py filename:.env --max-results 50
python main.py "API_KEY" --max-results 50
```

---

## 📚 Further Reading

- [README.md](README.md) - Main documentation
- [INSTALLATION.md](INSTALLATION.md) - Setup guide
- [GitHub Search Syntax](https://docs.github.com/en/search-github/searching-on-github/searching-code)
- [GitHub API Documentation](https://docs.github.com/en/rest)

---

**Happy Hunting! 🔍**
