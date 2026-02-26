# 🛡️ LayerGuard

**Layer-Aware Container Image Forensic Threat Scanner**

A professional-grade security analysis tool for Docker container images. LayerGuard identifies malicious or insecure packages within individual container layers, analyzes inherited vulnerabilities across image build history, and generates actionable remediation steps with beautiful HTML reports.

## 🎯 What is LayerGuard?

Modern container images are built in layers, with each layer potentially introducing security vulnerabilities. LayerGuard provides:

- **🔍 Layer-Aware Analysis**: Identifies which vulnerabilities come from base images vs. application layers
- **📋 Comprehensive SBOM**: Generates complete Software Bill of Materials using Syft
- **🚨 Vulnerability Detection**: Scans for CVEs using Trivy with severity classification
- **💡 Intelligent Remediation**: Provides actionable, prioritized security recommendations
- **📊 Beautiful HTML Reports**: Professional, human-friendly security reports that auto-open in your browser
- **🌐 Cross-Platform**: Works seamlessly on Windows and macOS

## ✨ Key Features

### 🎨 Professional HTML Reports
- **Auto-opens in browser** after each scan
- **Modern, responsive design** with gradient styling
- **Security dashboard** with visual severity indicators
- **Top 5 high-severity vulnerabilities** with plain English explanations
- **Actionable remediation steps** for non-technical users

### 🔬 Advanced Analysis
- **Base image detection** using `docker inspect` for reliability
- **Layer classification** (base, dependency, application, build, runtime)
- **Vulnerability attribution** (inherited vs application-introduced)
- **SBOM generation** for compliance and auditing

### 🛠️ Developer-Friendly
- **Clean CLI interface** with progress indicators
- **JSON reports** for automation and CI/CD integration
- **Verbose logging** for debugging
- **Exit codes** for pipeline integration

## 🏗️ Architecture

```
container-threat-scanner/
│
├── scanner/                    # Core scanning modules
│   ├── __init__.py            # Package initialization
│   ├── layer_analysis.py      # Docker layer forensics (FIXED base image detection)
│   ├── sbom.py                # SBOM generation (Syft)
│   ├── vulnerability.py       # Vulnerability scanning (Trivy)
│   ├── remediation.py         # Remediation engine
│   ├── report_generator.py    # HTML report generator (NEW)
│   └── utils.py               # Utilities and validation
│
├── reports/                    # Generated security reports
│   ├── sbom_*.json            # Software Bill of Materials
│   ├── vuln_*.json            # Vulnerability data
│   └── report_*.html          # HTML security reports (NEW)
│
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## 🔧 Prerequisites

### Required Tools

1. **Docker Desktop**
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - macOS: https://docs.docker.com/desktop/install/mac-install/

2. **Syft** (SBOM Generator)
   ```bash
   # macOS
   brew install syft
   
   # Windows (using Scoop)
   scoop install syft
   
   # Or download from: https://github.com/anchore/syft/releases
   ```

3. **Trivy** (Vulnerability Scanner)
   ```bash
   # macOS
   brew install trivy
   
   # Windows (using Chocolatey)
   choco install trivy
   
   # Or download from: https://github.com/aquasecurity/trivy/releases
   ```

4. **Python 3.10+**
   - Download from: https://www.python.org/downloads/

### Verify Installation

```bash
docker --version
syft version
trivy --version
python --version
```

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MishalHQ/container-threat-scanner.git
   cd container-threat-scanner
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   *Note: This project uses only Python standard library, so no external packages are required.*

3. **Run your first scan**
   ```bash
   python main.py --image nginx:latest
   ```

## 🚀 Usage

### Basic Scan

```bash
python main.py --image nginx:latest
```

**What happens:**
1. ✅ Validates environment (Docker, Syft, Trivy)
2. 🐳 Pulls the Docker image
3. 📦 Analyzes image layers
4. 📋 Generates SBOM
5. 🔍 Scans for vulnerabilities
6. 💡 Generates remediation suggestions
7. 📊 Creates HTML report
8. 🌐 **Auto-opens report in your browser**

### Verbose Mode

```bash
python main.py --image ubuntu:22.04 --verbose
```

### Scan Custom Images

```bash
python main.py --image mycompany/myapp:1.0.0
```

## 📊 Output Example

### Console Output

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    🛡️  LayerGuard v2.0                       ║
║        Layer-Aware Container Image Forensic Scanner          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Step 1/6: Validating environment...
✓ docker is installed
✓ Docker daemon is running
✓ syft is installed
✓ trivy is installed

Step 2/6: Pulling Docker image...
Step 3/6: Analyzing image layers...
Step 4/6: Generating Software Bill of Materials (SBOM)...
Step 5/6: Scanning for vulnerabilities...
Step 6/6: Generating HTML security report...

======================================================================
SECURITY ANALYSIS REPORT: nginx:latest
======================================================================

📦 LAYER SUMMARY
----------------------------------------------------------------------
Total Layers:        8
Base Image:          debian:bookworm-slim
Base Layers:         3
Application Layers:  5

🔍 VULNERABILITY SUMMARY
----------------------------------------------------------------------
Total Vulnerabilities: 127
  ├─ CRITICAL:         2
  ├─ HIGH:             15
  ├─ MEDIUM:           45
  └─ LOW:              65

🎯 INHERITED vs APPLICATION VULNERABILITIES
----------------------------------------------------------------------
Base Layer Vulnerabilities:        98
Application Layer Vulnerabilities: 29

📄 REPORTS
----------------------------------------------------------------------
Reports saved in: /path/to/reports
  ├─ SBOM:              sbom_nginx_latest.json
  ├─ Vulnerabilities:   vuln_nginx_latest.json
  └─ HTML Report:       report_nginx_latest.html

======================================================================

🎉 LayerGuard Scan Complete — Opened Security Report in Browser
======================================================================
```

### HTML Report Features

The auto-generated HTML report includes:

- **🎨 Modern Design**: Professional gradient styling with responsive layout
- **📊 Security Dashboard**: Visual cards showing vulnerability counts by severity
- **🎯 Layer Analysis**: Base vs application vulnerability breakdown
- **⚠️ Top Vulnerabilities**: Top 5 HIGH/CRITICAL issues with:
  - CVE ID and severity badge
  - Affected package and versions
  - **Plain English explanation** of the security impact
  - **Remediation recommendations** with fix versions
- **💡 Overall Recommendations**: Actionable steps to improve security
- **✅ Security Status Badge**: Clear visual indicator of risk level

## 🔬 How Layer-Aware Analysis Works

### Layer Classification

LayerGuard analyzes Docker image history to classify layers:

1. **Base Layers**: FROM instructions and base OS packages
2. **Dependency Layers**: Package installations (apt, yum, pip, npm)
3. **Application Layers**: COPY/ADD instructions with application code
4. **Build Layers**: RUN commands for compilation/building
5. **Runtime Layers**: CMD/ENTRYPOINT configurations

### Vulnerability Attribution

Vulnerabilities are classified as:

- **Base Layer Vulnerabilities**: Inherited from the base image (e.g., Debian, Alpine, Ubuntu)
  - These require updating the base image or switching to a more secure variant
  
- **Application Layer Vulnerabilities**: Introduced by application dependencies
  - These can be fixed by updating application packages

This distinction helps prioritize remediation efforts and understand the security posture of your container images.

## 🛡️ Security Features

### 1. SBOM Generation
- Complete inventory of all packages and dependencies
- Version tracking for compliance and auditing
- JSON format for integration with other tools

### 2. Vulnerability Detection
- CVE identification with severity ratings
- CVSS scoring integration
- Fixed version recommendations

### 3. Remediation Intelligence
- Prioritized action items (CRITICAL → LOW)
- Specific package upgrade paths
- Base image optimization suggestions
- Best practice recommendations

### 4. HTML Reporting (NEW)
- Professional, human-friendly reports
- Auto-opens in default browser
- Plain English vulnerability explanations
- Visual severity indicators
- Actionable remediation steps

### 5. Exit Codes
- `0`: Scan completed successfully, no critical issues
- `1`: Scan failed due to error
- `2`: Critical vulnerabilities detected
- `130`: User interrupted scan

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Container Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install tools
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
          curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
      
      - name: Run LayerGuard scan
        run: |
          python main.py --image ${{ env.IMAGE_NAME }}
        continue-on-error: true
      
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: reports/
```

## 📈 Advanced Usage

### Scanning Private Images

```bash
# Login to registry first
docker login myregistry.com

# Scan private image
python main.py --image myregistry.com/private/app:latest
```

### Batch Scanning

```bash
# Create a script to scan multiple images
for image in nginx:latest ubuntu:22.04 alpine:3.18; do
    echo "Scanning $image..."
    python main.py --image $image
done
```

### Custom Report Processing

```python
import json

# Load vulnerability report
with open('reports/vuln_nginx_latest.json', 'r') as f:
    vuln_data = json.load(f)

# Process vulnerabilities
for result in vuln_data['Results']:
    for vuln in result.get('Vulnerabilities', []):
        if vuln['Severity'] == 'CRITICAL':
            print(f"CRITICAL: {vuln['PkgName']} - {vuln['VulnerabilityID']}")
```

## 🐛 Troubleshooting

### Docker Not Running
```
Error: Docker daemon is not running
Solution: Start Docker Desktop
```

### Syft Not Found
```
Error: syft is not installed or not in PATH
Solution: Install Syft using package manager or download from GitHub
```

### Permission Denied
```
Error: Permission denied accessing Docker
Solution (Linux): Add user to docker group: sudo usermod -aG docker $USER
```

### Browser Doesn't Auto-Open
```
The HTML report is still generated in the reports/ directory.
Manually open: reports/report_<image_name>.html
```

## 🆕 What's New in v2.0

- ✅ **Fixed base image detection bug** - Now uses `docker inspect` for reliable parsing
- ✅ **Professional HTML reports** - Beautiful, human-friendly security reports
- ✅ **Auto-open in browser** - Reports automatically open after scan
- ✅ **Plain English explanations** - Non-technical vulnerability descriptions
- ✅ **Rebranded to LayerGuard** - Professional security tool branding
- ✅ **Improved console output** - Cleaner, more informative terminal display

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 👨‍💻 Author

LayerGuard Security Team

## 🔗 References

- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Syft Documentation](https://github.com/anchore/syft)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [NIST Container Security Guide](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)

---

**Built with ❤️ for Container Security by LayerGuard**