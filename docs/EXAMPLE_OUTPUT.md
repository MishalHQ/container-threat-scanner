# Example Scanner Output

This document shows a complete example of the Container Image Threat Scanner output.

## Command

```bash
python main.py --image nginx:latest
```

## Complete Output

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        Container Image Threat Scanner v1.0                   ║
║        Layer-Aware Forensic Security Analysis                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

2026-02-25 14:30:15,123 - __main__ - INFO - Step 1/5: Validating environment...
2026-02-25 14:30:15,234 - scanner.utils - INFO - ✓ docker is installed
2026-02-25 14:30:15,345 - scanner.utils - INFO - ✓ Docker daemon is running
2026-02-25 14:30:15,456 - scanner.utils - INFO - ✓ syft is installed
2026-02-25 14:30:15,567 - scanner.utils - INFO - ✓ trivy is installed
2026-02-25 14:30:15,678 - scanner.utils - INFO - ✓ All required tools are installed and ready

2026-02-25 14:30:15,789 - __main__ - INFO - Step 2/5: Pulling Docker image...
2026-02-25 14:30:15,890 - scanner.layer_analysis - INFO - Pulling image: nginx:latest
latest: Pulling from library/nginx
Digest: sha256:abc123...
Status: Image is up to date for nginx:latest
2026-02-25 14:30:18,123 - scanner.layer_analysis - INFO - ✓ Image pulled successfully

2026-02-25 14:30:18,234 - __main__ - INFO - Step 3/5: Analyzing image layers...
2026-02-25 14:30:18,345 - scanner.layer_analysis - INFO - Analyzing layers for: nginx:latest
2026-02-25 14:30:19,456 - scanner.layer_analysis - INFO - ✓ Analyzed 8 layers

2026-02-25 14:30:19,567 - __main__ - INFO - Step 4/5: Generating Software Bill of Materials (SBOM)...
2026-02-25 14:30:19,678 - scanner.sbom - INFO - Generating SBOM for: nginx:latest
 ✔ Loaded image            nginx:latest
 ✔ Parsed image            [8 layers]
 ✔ Cataloged packages      [156 packages]
2026-02-25 14:30:25,789 - scanner.sbom - INFO - ✓ SBOM saved to: reports/sbom_nginx_latest.json
2026-02-25 14:30:25,890 - __main__ - INFO - Found 156 packages in image

2026-02-25 14:30:25,901 - __main__ - INFO - Step 5/5: Scanning for vulnerabilities...
2026-02-25 14:30:26,012 - scanner.vulnerability - INFO - Scanning for vulnerabilities: nginx:latest
2026-02-25 14:30:35,123 - scanner.vulnerability - INFO - ✓ Vulnerability report saved to: reports/vuln_nginx_latest.json

2026-02-25 14:30:35,234 - scanner.remediation - INFO - Generating remediation suggestions...
2026-02-25 14:30:35,345 - scanner.remediation - INFO - ✓ Generated 6 remediation suggestions

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
   • openssl: 1.1.1n → 1.1.1t (CRITICAL, CVE-2023-0286)
   • libssl1.1: 1.1.1n → 1.1.1t (CRITICAL, CVE-2023-0286)

[HIGH PRIORITY]

1. Update 12 vulnerable package(s) with available fixes
   Category: Package Updates
   • curl: 7.74.0 → 7.88.1 (HIGH, CVE-2023-27533)
   • libcurl4: 7.74.0 → 7.88.1 (HIGH, CVE-2023-27533)
   • nginx: 1.23.1 → 1.23.4 (HIGH, CVE-2023-44487)
   ... and 9 more

2. Base image contains 98 vulnerabilities
   Category: Base Image
   • Consider updating to a newer version of the base image: debian:bookworm-slim
   • Check for security-focused base image variants (e.g., -alpine, -slim)
   • Review base image security advisories

[MEDIUM PRIORITY]

1. Consider using a minimal base image
   Category: Image Optimization
   • Alpine Linux images are typically smaller and have fewer vulnerabilities
   • Distroless images contain only application dependencies
   • Example: Replace debian:latest with debian:stable-slim or alpine:latest

2. Minimize installed packages
   Category: Attack Surface Reduction
   • Remove development tools and build dependencies in final image
   • Use multi-stage builds to separate build and runtime environments
   • Audit installed packages and remove unused ones

[LOW PRIORITY]

1. Implement continuous security scanning
   Category: Best Practices
   • Integrate this scanner into CI/CD pipeline
   • Set up automated scanning on image push
   • Establish vulnerability SLA policies

📄 REPORTS
----------------------------------------------------------------------
Reports saved in: /Users/mishal/container-threat-scanner/reports
  ├─ SBOM:              sbom_nginx_latest.json
  └─ Vulnerabilities:   vuln_nginx_latest.json

======================================================================

❌ SECURITY STATUS: CRITICAL - Immediate action required!
======================================================================

2026-02-25 14:30:35,456 - __main__ - WARNING - Critical vulnerabilities detected!
```

## Generated Report Files

### 1. SBOM Report (sbom_nginx_latest.json)

Contains complete Software Bill of Materials with:
- All 156 packages detected
- Package versions
- Package types (deb, npm, python, etc.)
- File locations
- Metadata

### 2. Vulnerability Report (vuln_nginx_latest.json)

Contains detailed vulnerability information:
- CVE IDs
- Severity ratings
- Affected packages
- Fixed versions
- CVSS scores
- Descriptions
- References

## Exit Codes

- **Exit Code 2**: Critical vulnerabilities detected (as shown in this example)
- **Exit Code 0**: Scan completed successfully, no critical issues
- **Exit Code 1**: Scan failed due to error
- **Exit Code 130**: User interrupted scan

## Verbose Mode Output

When running with `--verbose` flag, additional debug information is shown:

```bash
python main.py --image nginx:latest --verbose
```

This includes:
- Detailed command execution logs
- Docker layer parsing details
- SBOM generation progress
- Trivy scanning details
- Remediation logic decisions

## Next Steps After Scan

1. **Review Critical Vulnerabilities**: Address the 2 CRITICAL issues immediately
2. **Update Packages**: Apply the 12 available package updates
3. **Consider Base Image**: Evaluate switching to a more secure base image
4. **Implement CI/CD**: Integrate scanner into your pipeline
5. **Regular Scanning**: Schedule periodic scans for new vulnerabilities