# Container Image Threat Scanner

A professional-grade, layer-aware forensic security analysis tool for Docker container images. This tool identifies malicious or insecure packages within individual container layers, analyzes inherited vulnerabilities across image build history, and generates actionable remediation steps to enhance container security visibility and integrity.

## 🎯 Project Overview

Modern container images are built in layers, with each layer potentially introducing security vulnerabilities. This scanner provides:

- **Layer-Aware Analysis**: Identifies which vulnerabilities come from base images vs. application layers
- **Comprehensive SBOM**: Generates complete Software Bill of Materials using Syft
- **Vulnerability Detection**: Scans for CVEs using Trivy with severity classification
- **Intelligent Remediation**: Provides actionable, prioritized security recommendations
- **Cross-Platform**: Works seamlessly on Windows and macOS

## 🏗️ Architecture

```
container-threat-scanner/
│
├── scanner/                    # Core scanning modules
│   ├── __init__.py            # Package initialization
│   ├── layer_analysis.py      # Docker layer forensics
│   ├── sbom.py                # SBOM generation (Syft)
│   ├── vulnerability.py       # Vulnerability scanning (Trivy)
│   ├── remediation.py         # Remediation engine
│   └── utils.py               # Utilities and validation
│
├── reports/                    # Generated security reports
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

3. **Verify environment**
   ```bash
   python main.py --image nginx:latest
   ```

## 🚀 Usage

### Basic Scan

```bash
python main.py --image nginx:latest
```

### Verbose Mode

```bash
python main.py --image ubuntu:22.04 --verbose
```

### Scan Custom Images

```bash
python main.py --image mycompany/myapp:1.0.0
```

## 📊 Output Example

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        Container Image Threat Scanner v1.0                   ║
║        Layer-Aware Forensic Security Analysis                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

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

⚠️  Base layer vulnerabilities are inherited from the base image.
   Consider updating the base image or switching to a more secure variant.

💡 REMEDIATION SUGGESTIONS
----------------------------------------------------------------------

[CRITICAL PRIORITY]

1. Found 2 CRITICAL vulnerabilities
   Category: Critical Vulnerabilities
   • openssl: 1.1.1n → 1.1.1t (CRITICAL)
   • libssl1.1: 1.1.1n → 1.1.1t (CRITICAL)

[HIGH PRIORITY]

1. Update 12 vulnerable package(s) with available fixes
   Category: Package Updates
   • curl: 7.74.0 → 7.88.1 (HIGH)
   • libcurl4: 7.74.0 → 7.88.1 (HIGH)
   • nginx: 1.23.1 → 1.23.4 (HIGH)

2. Base image contains 98 vulnerabilities
   Category: Base Image
   • Consider updating to a newer version of the base image: debian:bookworm-slim
   • Check for security-focused base image variants (e.g., -alpine, -slim)
   • Review base image security advisories

📄 REPORTS
----------------------------------------------------------------------
Reports saved in: /path/to/reports
  ├─ SBOM:              sbom_nginx_latest.json
  └─ Vulnerabilities:   vuln_nginx_latest.json

======================================================================

❌ SECURITY STATUS: CRITICAL - Immediate action required!
======================================================================
```

## 🔬 How Layer-Aware Analysis Works

### Layer Classification

The scanner analyzes Docker image history to classify layers:

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

### 4. Exit Codes
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
      
      - name: Run security scan
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

## 🤝 Contributing

This is an educational/internship project. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

DevSecOps Engineering Team

## 🔗 References

- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Syft Documentation](https://github.com/anchore/syft)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [NIST Container Security Guide](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)

---

**Built with ❤️ for Container Security**