"""
LayerGuard HTML Report Generator
Generates professional, human-friendly security reports
"""

import logging
from pathlib import Path
from datetime import datetime
from .utils import ensure_reports_directory, sanitize_image_name


class HTMLReportGenerator:
    """
    Generates professional HTML security reports for LayerGuard
    """
    
    def __init__(self, image_name, layer_analysis, vuln_summary, classified_vulns, vulnerable_packages):
        """
        Initialize HTML report generator
        
        Args:
            image_name (str): Docker image name
            layer_analysis (dict): Layer analysis results
            vuln_summary (dict): Vulnerability summary
            classified_vulns (dict): Classified vulnerabilities
            vulnerable_packages (list): List of vulnerable packages
        """
        self.image_name = image_name
        self.layer_analysis = layer_analysis
        self.vuln_summary = vuln_summary
        self.classified_vulns = classified_vulns
        self.vulnerable_packages = vulnerable_packages
        self.logger = logging.getLogger(__name__)
        self.report_path = None
    
    def generate(self):
        """
        Generate HTML security report
        
        Returns:
            Path: Path to generated HTML report
        """
        self.logger.info("Generating HTML security report...")
        
        try:
            # Ensure reports directory exists
            reports_dir = ensure_reports_directory()
            
            # Generate output filename
            safe_name = sanitize_image_name(self.image_name)
            self.report_path = reports_dir / f"report_{safe_name}.html"
            
            # Generate HTML content
            html_content = self._generate_html()
            
            # Write to file
            with open(self.report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"✓ HTML report saved to: {self.report_path}")
            
            return self.report_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {str(e)}")
            raise
    
    def _generate_html(self):
        """
        Generate complete HTML report content
        
        Returns:
            str: HTML content
        """
        # Get top 5 HIGH/CRITICAL vulnerabilities
        top_vulns = self._get_top_vulnerabilities(5)
        
        # Determine security status
        security_status = self._get_security_status()
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LayerGuard Security Report - {self.image_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .header .image-name {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 6px;
            margin-top: 20px;
            display: inline-block;
            font-family: 'Courier New', monospace;
            font-size: 1.2em;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .card {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .card.critical {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        
        .card.high {{
            border-left-color: #fd7e14;
            background: #fff8f0;
        }}
        
        .card.medium {{
            border-left-color: #ffc107;
            background: #fffbf0;
        }}
        
        .card.low {{
            border-left-color: #28a745;
            background: #f0fff4;
        }}
        
        .card-title {{
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .card-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #333;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 1.1em;
            margin-top: 10px;
        }}
        
        .status-critical {{
            background: #dc3545;
            color: white;
        }}
        
        .status-high {{
            background: #fd7e14;
            color: white;
        }}
        
        .status-moderate {{
            background: #ffc107;
            color: #333;
        }}
        
        .status-low {{
            background: #28a745;
            color: white;
        }}
        
        .vuln-list {{
            list-style: none;
        }}
        
        .vuln-item {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .vuln-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .vuln-item.critical {{
            border-left: 5px solid #dc3545;
        }}
        
        .vuln-item.high {{
            border-left: 5px solid #fd7e14;
        }}
        
        .vuln-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .vuln-cve {{
            font-size: 1.2em;
            font-weight: 700;
            color: #333;
            font-family: 'Courier New', monospace;
        }}
        
        .severity-badge {{
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .severity-critical {{
            background: #dc3545;
            color: white;
        }}
        
        .severity-high {{
            background: #fd7e14;
            color: white;
        }}
        
        .severity-medium {{
            background: #ffc107;
            color: #333;
        }}
        
        .severity-low {{
            background: #28a745;
            color: white;
        }}
        
        .vuln-details {{
            margin-top: 15px;
        }}
        
        .vuln-row {{
            display: flex;
            margin-bottom: 8px;
        }}
        
        .vuln-label {{
            font-weight: 600;
            color: #6c757d;
            min-width: 150px;
        }}
        
        .vuln-value {{
            color: #333;
            font-family: 'Courier New', monospace;
        }}
        
        .vuln-description {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
            line-height: 1.6;
            color: #495057;
        }}
        
        .remediation-box {{
            background: #e7f3ff;
            border-left: 4px solid #0066cc;
            padding: 20px;
            border-radius: 6px;
            margin-top: 10px;
        }}
        
        .remediation-box strong {{
            color: #0066cc;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }}
        
        .footer .timestamp {{
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .no-vulns {{
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-size: 1.1em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ LayerGuard</h1>
            <div class="subtitle">Layer-Aware Container Image Forensic Threat Scanner</div>
            <div class="image-name">{self.image_name}</div>
        </div>
        
        <div class="content">
            <!-- Security Summary Dashboard -->
            <div class="section">
                <h2 class="section-title">Security Summary</h2>
                <div class="dashboard">
                    <div class="card">
                        <div class="card-title">Total Vulnerabilities</div>
                        <div class="card-value">{self.vuln_summary['total']}</div>
                    </div>
                    <div class="card critical">
                        <div class="card-title">Critical</div>
                        <div class="card-value">{self.vuln_summary['CRITICAL']}</div>
                    </div>
                    <div class="card high">
                        <div class="card-title">High</div>
                        <div class="card-value">{self.vuln_summary['HIGH']}</div>
                    </div>
                    <div class="card medium">
                        <div class="card-title">Medium</div>
                        <div class="card-value">{self.vuln_summary['MEDIUM']}</div>
                    </div>
                    <div class="card low">
                        <div class="card-title">Low</div>
                        <div class="card-value">{self.vuln_summary['LOW']}</div>
                    </div>
                </div>
                
                <div class="dashboard">
                    <div class="card">
                        <div class="card-title">Base Layer Vulnerabilities</div>
                        <div class="card-value">{self.classified_vulns['base_count']}</div>
                        <div style="margin-top: 10px; color: #6c757d; font-size: 0.9em;">
                            Inherited from base image
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Application Layer Vulnerabilities</div>
                        <div class="card-value">{self.classified_vulns['app_count']}</div>
                        <div style="margin-top: 10px; color: #6c757d; font-size: 0.9em;">
                            From application dependencies
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Total Layers</div>
                        <div class="card-value">{self.layer_analysis['total_layers']}</div>
                        <div style="margin-top: 10px; color: #6c757d; font-size: 0.9em;">
                            Base: {self.layer_analysis['base_image']}
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <div class="status-badge {security_status['class']}">{security_status['text']}</div>
                </div>
            </div>
            
            <!-- Top Vulnerabilities -->
            <div class="section">
                <h2 class="section-title">Top High-Severity Vulnerabilities</h2>
                {self._generate_vulnerability_list(top_vulns)}
            </div>
            
            <!-- Remediation Recommendations -->
            <div class="section">
                <h2 class="section-title">Remediation Recommendations</h2>
                {self._generate_remediation_section()}
            </div>
        </div>
        
        <div class="footer">
            <strong>LayerGuard</strong> - Layer-Aware Container Image Forensic Threat Scanner
            <div class="timestamp">Report generated: {timestamp}</div>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _get_top_vulnerabilities(self, count=5):
        """
        Get top N high-severity vulnerabilities
        
        Args:
            count (int): Number of vulnerabilities to return
            
        Returns:
            list: Top vulnerabilities
        """
        # Filter HIGH and CRITICAL vulnerabilities
        high_severity = [
            v for v in self.vulnerable_packages
            if v['severity'] in ['CRITICAL', 'HIGH']
        ]
        
        # Sort by severity (CRITICAL first, then HIGH)
        severity_order = {'CRITICAL': 0, 'HIGH': 1}
        high_severity.sort(key=lambda x: severity_order.get(x['severity'], 2))
        
        return high_severity[:count]
    
    def _get_security_status(self):
        """
        Determine overall security status
        
        Returns:
            dict: Status text and CSS class
        """
        if self.vuln_summary['CRITICAL'] > 0:
            return {
                'text': '❌ CRITICAL - Immediate Action Required',
                'class': 'status-critical'
            }
        elif self.vuln_summary['HIGH'] > 0:
            return {
                'text': '⚠️ HIGH RISK - Action Recommended',
                'class': 'status-high'
            }
        elif self.vuln_summary['MEDIUM'] > 0:
            return {
                'text': '⚡ MODERATE RISK - Review Recommended',
                'class': 'status-moderate'
            }
        else:
            return {
                'text': '✅ LOW RISK - Continue Monitoring',
                'class': 'status-low'
            }
    
    def _generate_vulnerability_list(self, vulnerabilities):
        """
        Generate HTML for vulnerability list
        
        Args:
            vulnerabilities (list): List of vulnerabilities
            
        Returns:
            str: HTML content
        """
        if not vulnerabilities:
            return '<div class="no-vulns">✅ No high-severity vulnerabilities found!</div>'
        
        html_items = []
        
        for vuln in vulnerabilities:
            severity_class = vuln['severity'].lower()
            cve_id = vuln['vulnerability_id']
            package = vuln['package']
            installed = vuln['installed_version']
            fixed = vuln['fixed_version'] or 'Not available'
            title = vuln.get('title', 'No title available')
            description = vuln.get('description', 'No description available')
            
            # Generate plain English explanation
            explanation = self._generate_explanation(vuln)
            
            html_items.append(f"""
                <li class="vuln-item {severity_class}">
                    <div class="vuln-header">
                        <div class="vuln-cve">{cve_id}</div>
                        <div class="severity-badge severity-{severity_class}">{vuln['severity']}</div>
                    </div>
                    
                    <div class="vuln-details">
                        <div class="vuln-row">
                            <div class="vuln-label">Affected Package:</div>
                            <div class="vuln-value">{package}</div>
                        </div>
                        <div class="vuln-row">
                            <div class="vuln-label">Installed Version:</div>
                            <div class="vuln-value">{installed}</div>
                        </div>
                        <div class="vuln-row">
                            <div class="vuln-label">Fixed Version:</div>
                            <div class="vuln-value">{fixed}</div>
                        </div>
                    </div>
                    
                    <div class="vuln-description">
                        <strong>What this means:</strong> {explanation}
                    </div>
                    
                    {self._generate_remediation_box(vuln)}
                </li>
            """)
        
        return f'<ul class="vuln-list">{"".join(html_items)}</ul>'
    
    def _generate_explanation(self, vuln):
        """
        Generate plain English explanation of vulnerability impact
        
        Args:
            vuln (dict): Vulnerability information
            
        Returns:
            str: Human-readable explanation
        """
        package = vuln['package']
        severity = vuln['severity']
        
        # Generate contextual explanation based on package type and severity
        if severity == 'CRITICAL':
            return f"This is a critical security flaw in {package} that could allow attackers to gain unauthorized access, execute malicious code, or compromise your system. Immediate action is required to update or replace this package."
        elif severity == 'HIGH':
            return f"This high-severity vulnerability in {package} poses a significant security risk and could be exploited by attackers to compromise your application or data. You should prioritize fixing this issue."
        else:
            return f"This vulnerability in {package} has been identified and should be addressed to maintain security best practices."
    
    def _generate_remediation_box(self, vuln):
        """
        Generate remediation recommendation box
        
        Args:
            vuln (dict): Vulnerability information
            
        Returns:
            str: HTML content
        """
        fixed = vuln['fixed_version']
        package = vuln['package']
        
        if fixed and fixed != 'Not available':
            return f"""
                <div class="remediation-box">
                    <strong>✅ Fix Available:</strong> Update {package} to version {fixed} or higher to resolve this vulnerability.
                </div>
            """
        else:
            return f"""
                <div class="remediation-box">
                    <strong>⚠️ No Fix Available:</strong> Consider using an alternative package or implementing additional security controls until a patch is released.
                </div>
            """
    
    def _generate_remediation_section(self):
        """
        Generate overall remediation recommendations
        
        Returns:
            str: HTML content
        """
        recommendations = []
        
        # Base image recommendation
        if self.classified_vulns['base_count'] > 0:
            recommendations.append(f"""
                <div class="remediation-box">
                    <strong>🔄 Update Base Image:</strong> {self.classified_vulns['base_count']} vulnerabilities are inherited from the base image ({self.layer_analysis['base_image']}). Consider updating to a newer version or switching to a more secure base image variant (e.g., Alpine, Distroless).
                </div>
            """)
        
        # Package updates
        fixable = [v for v in self.vulnerable_packages if v.get('fixed_version')]
        if fixable:
            recommendations.append(f"""
                <div class="remediation-box">
                    <strong>📦 Update Packages:</strong> {len(fixable)} vulnerable packages have fixes available. Update these packages to their fixed versions to resolve known vulnerabilities.
                </div>
            """)
        
        # General best practices
        recommendations.append("""
            <div class="remediation-box">
                <strong>🔒 Security Best Practices:</strong>
                <ul style="margin-top: 10px; margin-left: 20px;">
                    <li>Use multi-stage builds to minimize attack surface</li>
                    <li>Remove unnecessary packages and dependencies</li>
                    <li>Implement regular security scanning in CI/CD pipeline</li>
                    <li>Keep base images and dependencies up to date</li>
                    <li>Follow principle of least privilege for container permissions</li>
                </ul>
            </div>
        """)
        
        return ''.join(recommendations)