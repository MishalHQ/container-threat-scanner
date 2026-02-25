"""
Remediation suggestion engine
Generates actionable security recommendations
"""

import logging
from collections import defaultdict


class RemediationEngine:
    """
    Generates remediation suggestions based on vulnerability analysis
    """
    
    def __init__(self, vuln_scanner, layer_analyzer, sbom_generator):
        """
        Initialize remediation engine
        
        Args:
            vuln_scanner: VulnerabilityScanner instance
            layer_analyzer: LayerAnalyzer instance
            sbom_generator: SBOMGenerator instance
        """
        self.vuln_scanner = vuln_scanner
        self.layer_analyzer = layer_analyzer
        self.sbom_generator = sbom_generator
        self.logger = logging.getLogger(__name__)
    
    def generate_suggestions(self):
        """
        Generate remediation suggestions
        
        Returns:
            list: Remediation suggestions
        """
        self.logger.info("Generating remediation suggestions...")
        
        suggestions = []
        
        # Get vulnerability data
        vuln_summary = self.vuln_scanner.get_vulnerability_summary()
        vulnerable_packages = self.vuln_scanner.get_vulnerable_packages()
        classified_vulns = self.vuln_scanner.classify_vulnerabilities_by_layer(
            self.layer_analyzer
        )
        
        # Suggestion 1: Update packages with fixes available
        fixable_packages = self._get_fixable_packages(vulnerable_packages)
        if fixable_packages:
            suggestions.append({
                'priority': 'HIGH',
                'category': 'Package Updates',
                'title': f'Update {len(fixable_packages)} vulnerable package(s) with available fixes',
                'details': fixable_packages[:5]  # Top 5
            })
        
        # Suggestion 2: Base image vulnerabilities
        if classified_vulns['base_count'] > 0:
            suggestions.append({
                'priority': 'HIGH',
                'category': 'Base Image',
                'title': f'Base image contains {classified_vulns["base_count"]} vulnerabilities',
                'details': [
                    f'Consider updating to a newer version of the base image: {self.layer_analyzer.base_image}',
                    'Check for security-focused base image variants (e.g., -alpine, -slim)',
                    'Review base image security advisories'
                ]
            })
        
        # Suggestion 3: Critical vulnerabilities
        if vuln_summary.get('CRITICAL', 0) > 0:
            critical_packages = [
                v for v in vulnerable_packages 
                if v['severity'] == 'CRITICAL'
            ]
            suggestions.append({
                'priority': 'CRITICAL',
                'category': 'Critical Vulnerabilities',
                'title': f'Found {vuln_summary["CRITICAL"]} CRITICAL vulnerabilities',
                'details': [
                    f'{v["package"]} ({v["vulnerability_id"]}): {v["title"]}'
                    for v in critical_packages[:3]
                ]
            })
        
        # Suggestion 4: Use minimal base images
        if self._should_suggest_minimal_base():
            suggestions.append({
                'priority': 'MEDIUM',
                'category': 'Image Optimization',
                'title': 'Consider using a minimal base image',
                'details': [
                    'Alpine Linux images are typically smaller and have fewer vulnerabilities',
                    'Distroless images contain only application dependencies',
                    'Example: Replace debian:latest with debian:stable-slim or alpine:latest'
                ]
            })
        
        # Suggestion 5: Remove unused packages
        suggestions.append({
            'priority': 'MEDIUM',
            'category': 'Attack Surface Reduction',
            'title': 'Minimize installed packages',
            'details': [
                'Remove development tools and build dependencies in final image',
                'Use multi-stage builds to separate build and runtime environments',
                'Audit installed packages and remove unused ones'
            ]
        })
        
        # Suggestion 6: Regular scanning
        suggestions.append({
            'priority': 'LOW',
            'category': 'Best Practices',
            'title': 'Implement continuous security scanning',
            'details': [
                'Integrate this scanner into CI/CD pipeline',
                'Set up automated scanning on image push',
                'Establish vulnerability SLA policies',
                'Monitor for new CVEs affecting deployed images'
            ]
        })
        
        self.logger.info(f"✓ Generated {len(suggestions)} remediation suggestions")
        
        return suggestions
    
    def _get_fixable_packages(self, vulnerable_packages):
        """
        Get packages with available fixes
        
        Args:
            vulnerable_packages (list): List of vulnerable packages
            
        Returns:
            list: Packages with fixes
        """
        fixable = []
        
        for vuln in vulnerable_packages:
            if vuln.get('fixed_version') and vuln['fixed_version'] != '':
                fixable.append({
                    'package': vuln['package'],
                    'current': vuln['installed_version'],
                    'fixed': vuln['fixed_version'],
                    'severity': vuln['severity'],
                    'cve': vuln['vulnerability_id']
                })
        
        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        fixable.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        return fixable
    
    def _should_suggest_minimal_base(self):
        """
        Determine if minimal base image suggestion is appropriate
        
        Returns:
            bool: True if suggestion should be made
        """
        base_image = self.layer_analyzer.base_image.lower()
        
        # Don't suggest if already using minimal images
        minimal_indicators = ['alpine', 'distroless', 'scratch', 'slim']
        
        return not any(indicator in base_image for indicator in minimal_indicators)
    
    def format_suggestions(self, suggestions):
        """
        Format suggestions for display
        
        Args:
            suggestions (list): Remediation suggestions
            
        Returns:
            str: Formatted suggestions
        """
        output = []
        
        for idx, suggestion in enumerate(suggestions, 1):
            priority = suggestion['priority']
            category = suggestion['category']
            title = suggestion['title']
            details = suggestion['details']
            
            output.append(f"\n[{priority}] {category}")
            output.append(f"{idx}. {title}")
            
            if isinstance(details, list):
                for detail in details:
                    if isinstance(detail, dict):
                        # Package update format
                        output.append(
                            f"   • {detail['package']}: "
                            f"{detail['current']} → {detail['fixed']} "
                            f"({detail['severity']}, {detail['cve']})"
                        )
                    else:
                        output.append(f"   • {detail}")
        
        return '\n'.join(output)