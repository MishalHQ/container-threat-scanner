# Changelog

All notable changes to LayerGuard will be documented in this file.

## [2.0.0] - 2026-02-25

### 🎉 Major Release - LayerGuard Rebranding

### Added
- ✨ **Professional HTML Security Reports**
  - Beautiful, modern design with gradient styling
  - Auto-opens in default browser after scan
  - Plain English vulnerability explanations for non-technical users
  - Visual severity indicators (color-coded cards and badges)
  - Top 5 HIGH/CRITICAL vulnerabilities with detailed impact analysis
  - Actionable remediation recommendations
  - Responsive design for all screen sizes
  - Print-friendly CSS for documentation

- 🌐 **Auto-Open Browser Feature**
  - Cross-platform support (macOS, Windows, Linux)
  - Automatically opens HTML report after scan completion
  - Graceful fallback if browser can't be opened

- 📊 **Enhanced Reporting**
  - New `scanner/report_generator.py` module
  - HTML reports saved as `reports/report_<image_name>.html`
  - Professional branding as "LayerGuard"

### Fixed
- 🐛 **Base Image Detection Bug** (CRITICAL FIX)
  - Previously showed broken output like "Base Image: $server"
  - Now uses `docker inspect` for reliable base image detection
  - Multiple fallback methods for parsing
  - Validation to prevent broken string artifacts
  - Shows "Unknown (Parsing Issue)" if parsing fails
  - Improved error handling and logging

### Changed
- 🎨 **Rebranded to LayerGuard**
  - Updated all branding from "Container Image Threat Scanner" to "LayerGuard"
  - New tagline: "Layer-Aware Container Image Forensic Threat Scanner"
  - Updated version to 2.0.0
  - Professional security tool positioning

- 📝 **Improved Console Output**
  - Updated banner with LayerGuard branding
  - Added Step 6/6 for HTML report generation
  - Final message: "🎉 LayerGuard Scan Complete — Opened Security Report in Browser"
  - Cleaner, more professional terminal display

- 📚 **Documentation Updates**
  - Comprehensive README.md rewrite
  - New HTML_REPORT_PREVIEW.md documentation
  - Updated QUICK_START.md with new features
  - Enhanced CONTRIBUTING.md

### Technical Improvements
- 🔧 **Layer Analysis Module** (`scanner/layer_analysis.py`)
  - Refactored `_identify_base_image()` method
  - Added `_resolve_base_from_history()` fallback
  - Added `_is_valid_base_image()` validation
  - Improved regex patterns for base image extraction
  - Better error handling and logging

- 🏗️ **Architecture**
  - New modular `report_generator.py` for HTML generation
  - Clean separation of concerns
  - Updated `__init__.py` to include HTMLReportGenerator
  - Maintained backward compatibility with existing CLI

### Security
- 🔒 No security vulnerabilities introduced
- All existing security features maintained
- Enhanced vulnerability reporting with plain English explanations

---

## [1.0.0] - 2026-02-24

### Initial Release

### Added
- ✅ Docker image layer analysis
- ✅ SBOM generation using Syft
- ✅ Vulnerability scanning using Trivy
- ✅ Base vs application vulnerability classification
- ✅ Remediation suggestion engine
- ✅ JSON report generation
- ✅ Cross-platform support (Windows, macOS)
- ✅ CLI interface with argparse
- ✅ Comprehensive logging
- ✅ Exit codes for CI/CD integration
- ✅ GitHub Actions workflow
- ✅ Professional documentation

### Features
- Layer-aware forensic analysis
- Severity-based vulnerability classification
- Actionable remediation recommendations
- Environment validation
- Progress indicators
- Verbose mode for debugging

---

## Upgrade Guide

### From 1.0.0 to 2.0.0

**No breaking changes!** All existing functionality is preserved.

**New features you get automatically:**
1. HTML reports generated after every scan
2. Auto-open browser feature
3. Fixed base image detection
4. LayerGuard branding

**What you need to do:**
```bash
# Pull latest changes
git pull origin main

# Run a scan - that's it!
python main.py --image nginx:latest
```

**New files created:**
- `reports/report_<image_name>.html` - HTML security report

**Existing files still work:**
- `reports/sbom_<image_name>.json` - SBOM data
- `reports/vuln_<image_name>.json` - Vulnerability data

---

## Future Roadmap

### Planned for v2.1.0
- [ ] PDF report generation
- [ ] Email report delivery
- [ ] Custom report templates
- [ ] Vulnerability trend tracking

### Planned for v2.2.0
- [ ] Multi-image comparison
- [ ] Historical vulnerability tracking
- [ ] Integration with vulnerability databases
- [ ] Custom severity thresholds

### Planned for v3.0.0
- [ ] Web dashboard
- [ ] Real-time scanning
- [ ] Container registry integration
- [ ] Team collaboration features

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to LayerGuard.

## License

MIT License - See [LICENSE](LICENSE) for details.