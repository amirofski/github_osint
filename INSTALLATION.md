# 📦 Installation & Setup Guide

Complete step-by-step instructions for setting up GitHub OSINT Intelligence Tool on Windows, macOS, and Linux.

---

## 🎯 Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/amirofski/github_osint.git
cd github_osint

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure GitHub token
cp .env.example .env
# Edit .env and add your GitHub token

# 6. Run the tool
python main.py --interactive
```

---

## 📋 Full Installation Guide

### Table of Contents
1. [Python Installation](#python-installation)
2. [Repository Setup](#repository-setup)
3. [Virtual Environment](#virtual-environment)
4. [Dependency Installation](#dependency-installation)
5. [GitHub Token Setup](#github-token-setup)
6. [Verification](#verification)
7. [First Run](#first-run)

---

## 🐍 Python Installation

### Windows

#### Option 1: Official Installer (Recommended)

1. **Download Python**
   - Visit [python.org](https://www.python.org/downloads/)
   - Click "Download Python 3.12" (or latest version)
   - The `.exe` file will download

2. **Run Installer**
   - Double-click the downloaded `.exe` file
   - ⚠️ **IMPORTANT**: Check ✅ "Add Python to PATH"
   - Check ✅ "Install pip"
   - Click "Install Now"

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

   Expected output:
   ```
   Python 3.12.0
   pip 23.0 from ... (python 3.12)
   ```

#### Option 2: Windows Package Manager (winget)

```cmd
winget install Python.Python.3.12
```

Then verify:
```cmd
python --version
```

#### Option 3: Chocolatey

```cmd
choco install python
```

---

### macOS

#### Option 1: Homebrew (Recommended)

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python@3.12
   ```

3. **Verify**
   ```bash
   python3 --version
   pip3 --version
   ```

#### Option 2: Official Installer

1. Download from [python.org](https://www.python.org/downloads/)
2. Run the `.pkg` installer
3. Follow the setup wizard
4. Verify: `python3 --version`

#### Option 3: MacPorts

```bash
sudo port install python312
```

---

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Verify installation
python3 --version
pip3 --version
```

### Linux (Fedora/RHEL/CentOS)

```bash
# Install Python and pip
sudo dnf install python3 python3-pip -y

# Verify installation
python3 --version
pip3 --version
```

### Linux (Arch)

```bash
# Install Python
sudo pacman -S python python-pip

# Verify installation
python --version
pip --version
```

---

## 📁 Repository Setup

### Clone with Git

```bash
# Clone the repository
git clone https://github.com/amirofski/github_osint.git

# Navigate to directory
cd github_osint

# View files
ls -la
```

### Download ZIP (Alternative)

1. Visit [github.com/amirofski/github_osint](https://github.com/amirofski/github_osint)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in the extracted folder

---

## 🔄 Virtual Environment Setup

Creating a virtual environment isolates project dependencies from your system Python.

### Windows

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) prefix in your command prompt
```

**Deactivate** (when done):
```cmd
deactivate
```

### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) prefix in your terminal
```

**Deactivate** (when done):
```bash
deactivate
```

---

## 📚 Dependency Installation

### Install All Dependencies

With virtual environment activated:

```bash
pip install -r requirements.txt
```

### What Gets Installed

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | 2.31.0 | HTTP library for GitHub API |
| `python-dotenv` | 1.0.0 | Environment variable management |

### Manual Installation (if needed)

```bash
pip install requests==2.31.0
pip install python-dotenv==1.0.0
```

### Verify Installation

```bash
python -c "import requests; import dotenv; print('✓ All dependencies installed')"
```

---

## 🔐 GitHub Token Setup

### Step 1: Generate Personal Access Token

1. **Go to GitHub Settings**
   - Log in to [github.com](https://github.com)
   - Click your profile → Settings
   - Or direct: https://github.com/settings/tokens

2. **Create New Token**
   - Click "Generate new token (classic)"
   - Name: `GitHub OSINT Tool` (or any name)
   - Expiration: `No expiration` (optional)

3. **Select Scopes**
   - ✅ `public_repo` - Access public repositories
   - ✅ `read:user` - Read user information
   - Other scopes are optional

4. **Generate Token**
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (shown only once!)
   - Store it in a safe place

### Step 2: Configure .env File

#### Option 1: Copy Template

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

#### Option 2: Manual Creation

```bash
# Windows
echo GITHUB_TOKEN=your_token_here > .env

# macOS/Linux
cat > .env << EOF
GITHUB_TOKEN=your_token_here
OUTPUT_FORMAT=json
OUTPUT_FILE=results.json
EOF
```

#### Option 3: Edit in Text Editor

1. Open `.env.example` with any text editor
2. Replace `your_token_here` with your actual token
3. Save as `.env`

### Example .env File

```env
GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwxyz
OUTPUT_FORMAT=json
OUTPUT_FILE=results.json
```

### Verify Configuration

```bash
python -c "from config import get_github_token; print('✓ Token configured'); get_github_token()"
```

---

## ✅ Verification

### Test Basic Setup

```bash
# With virtual environment activated:
python -c "
import requests
import dotenv
from config import get_github_token
from github_client import GitHubClient

print('✓ All imports successful')
token = get_github_token()
print(f'✓ GitHub token loaded: {token[:10]}...')
client = GitHubClient()
print('✓ GitHub client initialized')
"
```

### Check API Access

```bash
python main.py --help
```

Expected output:
```
usage: main.py [-h] [-a] [-c] [--state-file STATE_FILE] [-i]
               [-m MAX_RESULTS] [-f {json,csv}] [-o OUTPUT]
               [--no-fetch-content]
               [query]

GitHub Intelligence Tool - Search repositories...
```

---

## 🚀 First Run

### Interactive Mode (Recommended for First Time)

```bash
python main.py --interactive
```

**You should see:**
```
╔═══════════════════════════════════════════════════════════╗
║         GitHub Intelligence Tool                          ║
║         Search repositories, files, and code patterns      ║
╚═══════════════════════════════════════════════════════════╝

Interactive Mode - Enter search queries (type 'exit' to quit)

Special commands:
  auto          - Auto-search all dangerous patterns
  exit/quit/q   - Exit program
```

**Try a simple query:**
```
Enter search query: filename:.env
Max results (default 100, max 1000): 10
Fetch file content? (y/n, default: y): y
Output format (json/csv, default: json): json
```

### Command Line Mode

```bash
# Simple search
python main.py "privateKey" --max-results 20

# Should output results to file like:
# Results saved to: results_2024_01_17_103045.json
```

---

## 🔧 Troubleshooting Installation

### ❌ "Python not recognized"

**Windows:**
- Reinstall Python with "Add Python to PATH" checked
- Or add Python to PATH manually:
  1. Search "Environment Variables" in Windows
  2. Click "Edit the system environment variables"
  3. Click "Environment Variables"
  4. Add Python installation path to `PATH`

**macOS/Linux:**
```bash
which python3
# Should show: /usr/bin/python3
```

---

### ❌ "No module named 'requests'"

```bash
# Make sure virtual environment is activated first
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

---

### ❌ "GITHUB_TOKEN not found"

```bash
# Check if .env file exists
ls -la .env  # macOS/Linux
dir .env    # Windows

# If not, create it:
cp .env.example .env

# Edit .env and add your GitHub token
```

---

### ❌ "pip: command not found"

```bash
# Try pip3
pip3 install -r requirements.txt

# Or use Python module syntax
python -m pip install -r requirements.txt
```

---

### ❌ Virtual Environment Not Working

**Windows:**
```cmd
# Delete old environment
rmdir /s venv

# Create new one
python -m venv venv

# Activate
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Delete old environment
rm -rf venv

# Create new one
python3 -m venv venv

# Activate
source venv/bin/activate
```

---

## 🆘 Uninstall / Clean Up

### Remove Everything

```bash
# Deactivate virtual environment
deactivate

# Windows: Delete folder
rmdir /s venv

# macOS/Linux: Delete folder
rm -rf venv

# Delete generated files
rm -rf results_*.json
rm -rf github_intel_state.json
```

---

## 📦 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8 | 3.11+ |
| RAM | 512 MB | 2 GB+ |
| Disk Space | 100 MB | 500 MB+ |
| Internet | 1 Mbps | 5 Mbps+ |
| OS | Windows 7+ | Windows 10, macOS 10.14+, Ubuntu 18.04+ |

---

## 🎓 Next Steps

1. **Read Usage Guide**: Check [README.md](README.md)
2. **Try Examples**: Run example commands
3. **Explore Patterns**: Modify `patterns.py` for custom searches
4. **Check Results**: Analyze output in JSON or CSV format

---

## 💬 Getting Help

1. Check error messages carefully
2. Review this guide's troubleshooting section
3. Check GitHub Issues
4. Create detailed issue with:
   - Your OS and Python version
   - Complete error message
   - Steps to reproduce

---

## ✨ Tips & Tricks

### Speed Up Installation

```bash
# Use cached packages (faster on second install)
pip install --cache-dir ~/.pip/cache -r requirements.txt
```

### Create Alias (macOS/Linux)

```bash
# Add to ~/.bashrc or ~/.zshrc
alias osint='python /path/to/github_osint/main.py'

# Then use:
osint --interactive
```

### Multiple Projects

```bash
# Keep separate virtual environments
python -m venv venv_osint
source venv_osint/bin/activate
```

---

**Happy Hunting! 🔍**

For more information, see [README.md](README.md)
