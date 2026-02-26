#!/usr/bin/env python3
"""
LayerGuard - Layer-Aware Container Image Forensic Threat Scanner
A professional security analysis tool for container images

Usage:
    python main.py --image nginx:latest
    python main.py --image nginx:latest --verbose
"""

import argparse
import sys
import logging
import webbrowser
from pathlib import Path

from scanner import (
    LayerAnalyzer,
    SBOMGenerator,
    VulnerabilityScanner,
    RemediationEngine,
    HTMLReportGenerator,
    validate_environment,
    setup_logging
)


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    🛡️  LayerGuard v2.0                       ║
║        Layer-Aware Container Image Forensic Scanner          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_summary(image_name, layer_analysis, vuln_summary, classified_vulns, suggestions):
    """
    Print comprehensive security analysis summary
    
    Args:
        image_name (str): Docker image name
        layer_analysis (dict): Layer analysis results
        vuln_summary (dict): Vulnerability summary
        classified_vulns (dict): Classified vulnerabilities
        suggestions (list): Remediation suggestions
    """
    print("\n" + "="*70)
    print(f"SECURITY ANALYSIS REPORT: {image_name}")
    print("="*70)
    
    # Layer Summary
    print("\n📦 LAYER SUMMARY")
    print("-" * 70)
    print(f"Total Layers:        {layer_analysis['total_layers']}")
    print(f"Base Image:          {layer_analysis['base_image']}")
    print(f"Base Layers:         {len([l for l in layer_analysis['layers'] if l['type'] == 'base'])}")
    print(f"Application Layers:  {len([l for l in layer_analysis['layers'] if l['type'] in ['application', 'dependency', 'build']])}")
    
    # Vulnerability Summary
    print("\n🔍 VULNERABILITY SUMMARY")
    print("-" * 70)
    print(f"Total Vulnerabilities: {vuln_summary['total']}")
    print(f"  ├─ CRITICAL:         {vuln_summary['CRITICAL']}")
    print(f"  ├─ HIGH:             {vuln_summary['HIGH']}")
    print(f"  ├─ MEDIUM:           {vuln_summary['MEDIUM']}")
    print(f"  └─ LOW:              {vuln_summary['LOW']}")
    
    # Layer-based Classification
    print("\n🎯 INHERITED vs APPLICATION VULNERABILITIES")
    print("-" * 70)
    print(f"Base Layer Vulnerabilities:        {classified_vulns['base_count']}")
    print(f"Application Layer Vulnerabilities: {classified_vulns['app_count']}")
    
    if classified_vulns['base_count'] > 0:
        print("\n⚠️  Base layer vulnerabilities are inherited from the base image.")
        print("   Consider updating the base image or switching to a more secure variant.")
    
    # Remediation Suggestions
    print("\n💡 REMEDIATION SUGGESTIONS")
    print("-" * 70)
    
    # Group by priority
    critical_suggestions = [s for s in suggestions if s['priority'] == 'CRITICAL']
    high_suggestions = [s for s in suggestions if s['priority'] == 'HIGH']
    medium_suggestions = [s for s in suggestions if s['priority'] == 'MEDIUM']
    low_suggestions = [s for s in suggestions if s['priority'] == 'LOW']
    
    for priority_group, priority_name in [
        (critical_suggestions, 'CRITICAL'),
        (high_suggestions, 'HIGH'),
        (medium_suggestions, 'MEDIUM'),
        (low_suggestions, 'LOW')
    ]:
        if priority_group:
            print(f"\n[{priority_name} PRIORITY]")
            for idx, suggestion in enumerate(priority_group, 1):
                print(f"\n{idx}. {suggestion['title']}")
                print(f"   Category: {suggestion['category']}")
                
                details = suggestion['details']
                if isinstance(details, list):
                    for detail in details[:3]:  # Show top 3
                        if isinstance(detail, dict):
                            print(
                                f"   • {detail['package']}: "
                                f"{detail['current']} → {detail['fixed']} "
                                f"({detail['severity']})"
                            )
                        else:
                            print(f"   • {detail}")
                    
                    if len(details) > 3:
                        print(f"   ... and {len(details) - 3} more")
    
    # Reports Location
    print("\n📄 REPORTS")
    print("-" * 70)
    print(f"Reports saved in: {Path('reports').absolute()}")
    print(f"  ├─ SBOM:              sbom_{image_name.replace(':', '_').replace('/', '_')}.json")
    print(f"  ├─ Vulnerabilities:   vuln_{image_name.replace(':', '_').replace('/', '_')}.json")
    print(f"  └─ HTML Report:       report_{image_name.replace(':', '_').replace('/', '_')}.html")
    
    print("\n" + "="*70)
    
    # Security Status
    if vuln_summary['CRITICAL'] > 0:
        print("\n❌ SECURITY STATUS: CRITICAL - Immediate action required!")
    elif vuln_summary['HIGH'] > 0:
        print("\n⚠️  SECURITY STATUS: HIGH RISK - Action recommended")
    elif vuln_summary['MEDIUM'] > 0:
        print("\n⚡ SECURITY STATUS: MODERATE RISK - Review recommended")
    else:
        print("\n✅ SECURITY STATUS: LOW RISK - Continue monitoring")
    
    print("="*70 + "\n")


def open_report_in_browser(report_path):
    """
    Open HTML report in default browser
    
    Args:
        report_path (Path): Path to HTML report
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Convert to absolute path and file:// URL
        abs_path = report_path.absolute()
        file_url = abs_path.as_uri()
        
        # Open in default browser
        webbrowser.open(file_url)
        logger.info(f"✓ Opened report in browser: {abs_path}")
        
    except Exception as e:
        logger.warning(f"Could not auto-open browser: {str(e)}")
        logger.info(f"Please manually open: {report_path}")


def main():
    """Main application entry point"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='LayerGuard - Layer-aware container security analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --image nginx:latest
  python main.py --image ubuntu:22.04 --verbose
  python main.py --image myapp:1.0.0
        """
    )
    
    parser.add_argument(
        '--image',
        required=True,
        help='Docker image name and tag (e.g., nginx:latest)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)
    
    # Print banner
    print_banner()
    
    try:
        # Validate environment
        logger.info("Step 1/6: Validating environment...")
        if not validate_environment():
            logger.error("Environment validation failed. Please install required tools.")
            sys.exit(1)
        
        # Initialize analyzers
        image_name = args.image
        
        layer_analyzer = LayerAnalyzer(image_name)
        sbom_generator = SBOMGenerator(image_name)
        vuln_scanner = VulnerabilityScanner(image_name)
        
        # Pull image
        logger.info("Step 2/6: Pulling Docker image...")
        layer_analyzer.pull_image()
        
        # Analyze layers
        logger.info("Step 3/6: Analyzing image layers...")
        layer_analysis = layer_analyzer.analyze_layers()
        
        # Generate SBOM
        logger.info("Step 4/6: Generating Software Bill of Materials (SBOM)...")
        sbom_data = sbom_generator.generate()
        package_count = sbom_generator.get_package_count()
        logger.info(f"Found {package_count} packages in image")
        
        # Scan vulnerabilities
        logger.info("Step 5/6: Scanning for vulnerabilities...")
        vuln_data = vuln_scanner.scan()
        vuln_summary = vuln_scanner.get_vulnerability_summary()
        classified_vulns = vuln_scanner.classify_vulnerabilities_by_layer(layer_analyzer)
        vulnerable_packages = vuln_scanner.get_vulnerable_packages()
        
        # Generate remediation suggestions
        remediation_engine = RemediationEngine(
            vuln_scanner,
            layer_analyzer,
            sbom_generator
        )
        suggestions = remediation_engine.generate_suggestions()
        
        # Generate HTML report
        logger.info("Step 6/6: Generating HTML security report...")
        html_generator = HTMLReportGenerator(
            image_name,
            layer_analysis,
            vuln_summary,
            classified_vulns,
            vulnerable_packages
        )
        report_path = html_generator.generate()
        
        # Print comprehensive summary
        print_summary(
            image_name,
            layer_analysis,
            vuln_summary,
            classified_vulns,
            suggestions
        )
        
        # Auto-open HTML report in browser
        open_report_in_browser(report_path)
        
        # Final success message
        print("\n" + "="*70)
        print("🎉 LayerGuard Scan Complete — Opened Security Report in Browser")
        print("="*70 + "\n")
        
        # Exit with non-zero code if critical vulnerabilities found
        if vuln_scanner.has_critical_vulnerabilities():
            logger.warning("Critical vulnerabilities detected!")
            sys.exit(2)
        
        logger.info("Scan completed successfully")
        sys.exit(0)
        
    except KeyboardInterrupt:
        logger.warning("\nScan interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Scan failed: {str(e)}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == '__main__':
    main()