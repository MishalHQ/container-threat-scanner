# 🛡️ LayerGuard

**Elite Layer-Aware Container Image Forensic Threat Scanner**

A professional-grade security analysis tool for Docker container images with an **elite cybersecurity-themed interface**. LayerGuard identifies malicious or insecure packages within individual container layers, analyzes inherited vulnerabilities across image build history, and generates **stunning interactive HTML reports** with advanced animations.


## 🎯 What is LayerGuard?

Modern container images are built in layers, with each layer potentially introducing security vulnerabilities. LayerGuard provides:

- **🔍 Layer-Aware Analysis**: Identifies which vulnerabilities come from base images vs. application layers
- **📋 Comprehensive SBOM**: Generates complete Software Bill of Materials using Syft
- **🚨 Vulnerability Detection**: Scans for CVEs using Trivy with severity classification
- **💡 Intelligent Remediation**: Provides actionable, prioritized security recommendations
- **🎨 Elite HTML Reports**: Professional cybersecurity-themed interactive reports with advanced animations
- **🌐 Cross-Platform**: Works seamlessly on Windows and macOS

## ✨ Key Features

### 🎨 Elite Interactive HTML Reports
- **Live Matrix rain** background animation (HTML5 Canvas)
- **Animated cyber grid** with moving patterns
- **Scanning line effect** sweeping continuously
- **50 floating particles** creating atmospheric depth
- **Glassmorphic cards** with backdrop blur
- **Interactive hover effects** - Cards lift, glow, and transform
- **Gradient text** with cyber green/blue colors
- **Glitch animations** on headers
- **Color-coded severity** indicators (Red, Orange, Blue, Green)
- **Smooth transitions** - Professional cubic-bezier easing
- **Auto-opens in browser** after each scan
- **Responsive design** - Works on all screen sizes
- **Print-friendly** - Professional documentation output

### 🔬 Advanced Analysis
- **Fixed base image detection** using `docker inspect`
- **Layer classification** (base, dependency, application, build, runtime)
- **Vulnerability attribution** (inherited vs application-introduced)
- **SBOM generation** for compliance and auditing
- **Plain English explanations** for non-technical users

### 🛠️ Developer-Friendly
- **Clean CLI interface** with progress indicators
- **JSON reports** for automation and CI/CD integration
- **Verbose logging** for debugging
- **Exit codes** for pipeline integration
- **Zero external dependencies** for HTML reports

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
│   ├── report_generator.py    # Elite HTML report generator
│   └── utils.py               # Utilities and validation
│
├── reports/                    # Generated security reports
│   ├── sbom_*.json            # Software Bill of Materials
│   ├── vuln_*.json            # Vulnerability data
│   └── report_*.html          # Elite HTML security reports
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
   ```

3. **Trivy** (Vulnerability Scanner)
   ```bash
   # macOS
   brew install trivy
   
   # Windows (using Chocolatey)
   choco install trivy
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

2. **Run your first scan**
   ```bash
   python main.py --image nginx:latest
   ```
   
   **Your browser will automatically open with a stunning cybersecurity-themed report!** 🔥

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
7. 🎨 Creates **elite HTML report** with animations
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

### Elite HTML Report Features

The auto-generated HTML report includes:

#### **🎨 Visual Design**
- **Dark cybersecurity theme** - Deep space background (#0a0e27)
- **Live Matrix rain** - Green cascading code animation
- **Animated grid pattern** - Moving cyber grid
- **Scanning line** - Continuous sweep effect
- **Floating particles** - 50 animated particles
- **Glassmorphic cards** - Frosted glass effect with backdrop blur
- **Neon color palette** - Cyber green, blue, pink, purple
- **Gradient text** - Green-to-blue transitions
- **Glitch effects** - Professional cyberpunk animations

#### **⚡ Interactive Elements**
- **Hover transformations** - Cards lift, glow, and scale
- **Rotating gradients** - Background animations on hover
- **Expanding borders** - Left border grows on interaction
- **Ripple effects** - Badges pulse on hover
- **Smooth transitions** - 0.4s cubic-bezier easing
- **Color changes** - Dynamic border colors
- **Shadow blooms** - Glowing effects expand

#### **📊 Content Sections**
1. **Security Dashboard**
   - Total vulnerabilities with animated count-up
   - Severity breakdown (CRITICAL, HIGH, MEDIUM, LOW)
   - Base vs Application vulnerability counts
   - Animated status badge with pulse effect

2. **Top Vulnerabilities**
   - Top 5 HIGH/CRITICAL issues
   - CVE IDs with flickering animation
   - Severity badges with glowing shadows
   - **Plain English explanations** of security impact
   - Package details with monospace font
   - Fix recommendations with version numbers

3. **Remediation Recommendations**
   - Base image update suggestions
   - Package update recommendations
   - Security best practices checklist
   - Interactive list items with hover effects

#### **🎯 Typography**
- **Orbitron** - Headers (900 weight, futuristic)
- **Rajdhani** - Body text (clean, modern)
- **Share Tech Mono** - Code/data (monospace)
- **Uppercase headers** with letter-spacing
- **High contrast** for readability

#### **📱 Responsive Design**
- Desktop: Multi-column grid layout
- Tablet: Adjusted columns
- Mobile: Single column, stacked cards
- All animations preserved across devices

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

### 4. Elite HTML Reporting
- **Professional cybersecurity theme**
- **Live animations** (Matrix rain, grid, scan line, particles)
- **Interactive elements** (hover effects, transformations)
- **Glassmorphism design** (modern frosted glass)
- **Auto-opens in browser**
- **Plain English explanations**
- **Visual severity indicators**
- **Actionable remediation steps**
- **Zero external dependencies**
- **Print-friendly output**

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

## 🎨 Elite Theme Highlights

### **What Makes It Industry-Grade**

✅ **Professional Aesthetics**
- Cybersecurity-focused color palette
- No childish elements
- Sophisticated animations
- Technical typography

✅ **Advanced Animations**
- Live Matrix rain (HTML5 Canvas)
- Animated cyber grid
- Scanning line effect
- Floating particle system
- Glitch text effects
- Rotating gradients
- Smooth transitions

✅ **Interactive Design**
- Hover transformations
- Color-changing borders
- Expanding elements
- Ripple effects
- Shadow blooms

✅ **Performance Optimized**
- 60 FPS animations
- GPU-accelerated transforms
- Efficient canvas rendering
- Minimal repaints

✅ **Zero Dependencies**
- Self-contained HTML file
- No external CSS/JS libraries
- Works offline
- Instant loading

## 🆕 What's New in v2.0

- ✅ **Elite cybersecurity theme** - Professional hacker aesthetic
- ✅ **Live Matrix rain** - Animated background with Canvas
- ✅ **Interactive animations** - Hover effects on all elements
- ✅ **Glassmorphism design** - Modern frosted glass cards
- ✅ **Fixed base image detection** - Reliable parsing with docker inspect
- ✅ **Auto-open in browser** - Reports open automatically
- ✅ **Plain English explanations** - Non-technical vulnerability descriptions
- ✅ **Gradient text effects** - Cyber green/blue color schemes
- ✅ **Responsive design** - Works on all devices
- ✅ **Print optimization** - Professional documentation output

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

**Experience elite cybersecurity reporting. Run a scan now.** 🛡️⚡🔥
