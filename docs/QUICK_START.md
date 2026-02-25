# Quick Start Guide

Get up and running with Container Image Threat Scanner in 5 minutes!

## ⚡ Prerequisites Check

Before starting, verify you have these tools installed:

```bash
# Check Docker
docker --version
# Expected: Docker version 20.10.x or higher

# Check Syft
syft version
# Expected: syft 0.x.x or higher

# Check Trivy
trivy --version
# Expected: Version: 0.x.x or higher

# Check Python
python --version
# Expected: Python 3.10.x or higher
```

If any tool is missing, see [Installation Guide](#installation-guide) below.

## 🚀 Quick Start (3 Steps)

### Step 1: Clone the Repository

```bash
git clone https://github.com/MishalHQ/container-threat-scanner.git
cd container-threat-scanner
```

### Step 2: Run Your First Scan

```bash
python main.py --image nginx:latest
```

That's it! The scanner will:
1. ✅ Validate your environment
2. 🐳 Pull the Docker image
3. 📦 Analyze image layers
4. 📋 Generate SBOM
5. 🔍 Scan for vulnerabilities
6. 💡 Provide remediation suggestions

### Step 3: Review Results

Check the generated reports:

```bash
ls -la reports/
# You'll see:
# - sbom_nginx_latest.json
# - vuln_nginx_latest.json
```

## 📚 Common Use Cases

### Scan a Specific Image Version

```bash
python main.py --image ubuntu:22.04
```

### Scan Your Application Image

```bash
python main.py --image mycompany/myapp:1.0.0
```

### Enable Verbose Logging

```bash
python main.py --image nginx:latest --verbose
```

### Scan Private Registry Image

```bash
# Login first
docker login myregistry.com

# Then scan
python main.py --image myregistry.com/private/app:latest
```

## 🔧 Installation Guide

### Install Docker Desktop

**macOS:**
```bash
# Download from: https://docs.docker.com/desktop/install/mac-install/
# Or use Homebrew:
brew install --cask docker
```

**Windows:**
```powershell
# Download from: https://docs.docker.com/desktop/install/windows-install/
# Or use Chocolatey:
choco install docker-desktop
```

### Install Syft

**macOS:**
```bash
brew install syft
```

**Windows:**
```powershell
# Using Scoop
scoop install syft

# Or download from: https://github.com/anchore/syft/releases
```

**Linux:**
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

### Install Trivy

**macOS:**
```bash
brew install trivy
```

**Windows:**
```powershell
# Using Chocolatey
choco install trivy

# Or download from: https://github.com/aquasecurity/trivy/releases
```

**Linux:**
```bash
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

### Install Python 3.10+

**macOS:**
```bash
brew install python@3.10
```

**Windows:**
```powershell
# Download from: https://www.python.org/downloads/
# Or use Chocolatey:
choco install python
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.10
```

## 🎯 Understanding the Output

### Security Status Indicators

- ✅ **LOW RISK**: No critical or high vulnerabilities
- ⚡ **MODERATE RISK**: Medium severity vulnerabilities found
- ⚠️ **HIGH RISK**: High severity vulnerabilities detected
- ❌ **CRITICAL**: Critical vulnerabilities require immediate action

### Vulnerability Severity Levels

1. **CRITICAL** 🔴 - Immediate action required
2. **HIGH** 🟠 - Action recommended soon
3. **MEDIUM** 🟡 - Review and plan remediation
4. **LOW** 🟢 - Monitor and address when convenient

### Layer Classification

- **Base Layers**: From the base image (e.g., debian, alpine)
- **Dependency Layers**: Package installations (apt, pip, npm)
- **Application Layers**: Your application code (COPY/ADD)
- **Build Layers**: Compilation and build steps
- **Runtime Layers**: CMD/ENTRYPOINT configurations

## 🐛 Troubleshooting

### "Docker daemon is not running"

**Solution:**
```bash
# macOS/Windows: Start Docker Desktop application
# Linux: 
sudo systemctl start docker
```

### "syft is not installed or not in PATH"

**Solution:**
```bash
# Verify installation
which syft

# If not found, reinstall using package manager
# macOS:
brew install syft

# Windows:
scoop install syft
```

### "Permission denied accessing Docker"

**Solution (Linux):**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

### "Image pull failed"

**Solution:**
```bash
# For private images, login first:
docker login

# For specific registry:
docker login myregistry.com
```

## 📖 Next Steps

1. **Read the Full Documentation**: Check [README.md](../README.md)
2. **Explore Example Output**: See [EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md)
3. **Integrate with CI/CD**: See GitHub Actions workflow in `.github/workflows/`
4. **Contribute**: Read [CONTRIBUTING.md](../CONTRIBUTING.md)

## 💡 Pro Tips

### Batch Scanning

Create a script to scan multiple images:

```bash
#!/bin/bash
images=("nginx:latest" "ubuntu:22.04" "alpine:3.18" "python:3.10")

for image in "${images[@]}"; do
    echo "Scanning $image..."
    python main.py --image "$image"
    echo "---"
done
```

### Automated Daily Scans

Add to crontab for daily scans:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/container-threat-scanner && python main.py --image myapp:latest
```

### JSON Report Processing

Process reports programmatically:

```python
import json

# Load vulnerability report
with open('reports/vuln_nginx_latest.json', 'r') as f:
    data = json.load(f)

# Count critical vulnerabilities
critical_count = sum(
    1 for result in data.get('Results', [])
    for vuln in result.get('Vulnerabilities', [])
    if vuln.get('Severity') == 'CRITICAL'
)

print(f"Critical vulnerabilities: {critical_count}")
```

## 🆘 Need Help?

- 📖 Check the [README](../README.md)
- 🐛 Report issues on [GitHub Issues](https://github.com/MishalHQ/container-threat-scanner/issues)
- 💬 Ask questions in [Discussions](https://github.com/MishalHQ/container-threat-scanner/discussions)

---

**Happy Scanning! 🔍**