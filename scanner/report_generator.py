"""
LayerGuard HTML Report Generator
Generates professional, cybersecurity-themed interactive reports
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
        Generate complete HTML report content with elite cybersecurity theme
        
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
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-dark: #0a0e27;
            --bg-darker: #050814;
            --cyber-green: #00ff41;
            --cyber-blue: #00d9ff;
            --neon-pink: #ff006e;
            --neon-purple: #8b5cf6;
            --critical-red: #ff0040;
            --warning-orange: #ff9500;
            --success-green: #00ff88;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --card-bg: rgba(15, 23, 42, 0.8);
            --card-border: rgba(0, 217, 255, 0.3);
            --glow-color: rgba(0, 255, 65, 0.5);
        }}
        
        body {{
            font-family: 'Rajdhani', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            overflow-x: hidden;
            position: relative;
            min-height: 100vh;
        }}
        
        /* Animated Matrix Background */
        .matrix-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.15;
            pointer-events: none;
        }}
        
        .matrix-bg canvas {{
            display: block;
            width: 100%;
            height: 100%;
        }}
        
        /* Animated Grid Background */
        .grid-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 217, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 217, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            z-index: 0;
            pointer-events: none;
            animation: gridMove 20s linear infinite;
        }}
        
        @keyframes gridMove {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(50px); }}
        }}
        
        /* Scanning Line Effect */
        .scan-line {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, 
                transparent, 
                var(--cyber-blue), 
                transparent);
            box-shadow: 0 0 20px var(--cyber-blue);
            z-index: 1;
            animation: scan 4s linear infinite;
        }}
        
        @keyframes scan {{
            0% {{ transform: translateY(0); opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ transform: translateY(100vh); opacity: 0; }}
        }}
        
        /* Floating Particles */
        .particles {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }}
        
        .particle {{
            position: absolute;
            width: 2px;
            height: 2px;
            background: var(--cyber-green);
            border-radius: 50%;
            animation: float 15s infinite;
            opacity: 0.6;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0) translateX(0); opacity: 0; }}
            50% {{ opacity: 0.6; }}
            100% {{ transform: translateY(-100vh) translateX(100px); opacity: 0; }}
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }}
        
        /* Header with Glitch Effect */
        .header {{
            background: linear-gradient(135deg, 
                rgba(0, 217, 255, 0.1) 0%, 
                rgba(139, 92, 246, 0.1) 100%);
            backdrop-filter: blur(10px);
            border-bottom: 2px solid var(--cyber-blue);
            padding: 60px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 50px rgba(0, 217, 255, 0.2);
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(0, 217, 255, 0.1), 
                transparent);
            animation: shimmer 3s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        
        .header h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 4em;
            font-weight: 900;
            background: linear-gradient(135deg, var(--cyber-green), var(--cyber-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 5px;
            position: relative;
            animation: glitchText 5s infinite;
            text-shadow: 
                0 0 10px rgba(0, 255, 65, 0.5),
                0 0 20px rgba(0, 255, 65, 0.3),
                0 0 30px rgba(0, 255, 65, 0.2);
        }}
        
        @keyframes glitchText {{
            0%, 90%, 100% {{ transform: translate(0); }}
            92% {{ transform: translate(-2px, 2px); }}
            94% {{ transform: translate(2px, -2px); }}
            96% {{ transform: translate(-2px, -2px); }}
            98% {{ transform: translate(2px, 2px); }}
        }}
        
        .header .subtitle {{
            font-size: 1.3em;
            color: var(--cyber-blue);
            font-weight: 500;
            letter-spacing: 3px;
            text-transform: uppercase;
            opacity: 0.9;
        }}
        
        .header .image-name {{
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid var(--cyber-green);
            padding: 15px 30px;
            border-radius: 8px;
            margin-top: 30px;
            display: inline-block;
            font-family: 'Share Tech Mono', monospace;
            font-size: 1.4em;
            color: var(--cyber-green);
            box-shadow: 
                0 0 20px rgba(0, 255, 65, 0.3),
                inset 0 0 20px rgba(0, 255, 65, 0.1);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(0, 255, 65, 0.3), inset 0 0 20px rgba(0, 255, 65, 0.1); }}
            50% {{ box-shadow: 0 0 30px rgba(0, 255, 65, 0.5), inset 0 0 30px rgba(0, 255, 65, 0.2); }}
        }}
        
        .content {{
            padding: 60px 40px;
        }}
        
        .section {{
            margin-bottom: 60px;
            animation: fadeInUp 0.8s ease-out;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .section-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2em;
            color: var(--cyber-blue);
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--cyber-blue);
            text-transform: uppercase;
            letter-spacing: 3px;
            position: relative;
            display: inline-block;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 0;
            height: 3px;
            background: var(--cyber-green);
            animation: expandLine 2s ease-out forwards;
        }}
        
        @keyframes expandLine {{
            to {{ width: 100%; }}
        }}
        
        /* Dashboard Cards with Hover Effects */
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }}
        
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 12px;
            border: 2px solid var(--card-border);
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
        }}
        
        .card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 217, 255, 0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
        }}
        
        .card:hover::before {{
            opacity: 1;
            animation: rotate 4s linear infinite;
        }}
        
        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .card:hover {{
            transform: translateY(-10px) scale(1.02);
            border-color: var(--cyber-green);
            box-shadow: 
                0 20px 60px rgba(0, 217, 255, 0.3),
                0 0 40px rgba(0, 255, 65, 0.2);
        }}
        
        .card.critical {{
            border-color: var(--critical-red);
            background: rgba(255, 0, 64, 0.05);
        }}
        
        .card.critical:hover {{
            border-color: var(--critical-red);
            box-shadow: 
                0 20px 60px rgba(255, 0, 64, 0.4),
                0 0 40px rgba(255, 0, 64, 0.3);
        }}
        
        .card.high {{
            border-color: var(--warning-orange);
            background: rgba(255, 149, 0, 0.05);
        }}
        
        .card.high:hover {{
            border-color: var(--warning-orange);
            box-shadow: 
                0 20px 60px rgba(255, 149, 0, 0.4),
                0 0 40px rgba(255, 149, 0, 0.3);
        }}
        
        .card.medium {{
            border-color: var(--cyber-blue);
            background: rgba(0, 217, 255, 0.05);
        }}
        
        .card.low {{
            border-color: var(--success-green);
            background: rgba(0, 255, 136, 0.05);
        }}
        
        .card-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9em;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .card-value {{
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5em;
            font-weight: 900;
            background: linear-gradient(135deg, var(--cyber-green), var(--cyber-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            z-index: 1;
            animation: countUp 1s ease-out;
        }}
        
        @keyframes countUp {{
            from {{ opacity: 0; transform: scale(0.5); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        
        .card.critical .card-value {{
            background: linear-gradient(135deg, var(--critical-red), var(--neon-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .card.high .card-value {{
            background: linear-gradient(135deg, var(--warning-orange), var(--neon-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Status Badge with Animation */
        .status-badge {{
            display: inline-block;
            padding: 15px 40px;
            border-radius: 50px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 1.3em;
            margin-top: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            overflow: hidden;
            animation: badgePulse 2s infinite;
        }}
        
        @keyframes badgePulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .status-badge::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .status-badge:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .status-critical {{
            background: linear-gradient(135deg, var(--critical-red), var(--neon-pink));
            color: white;
            box-shadow: 0 10px 40px rgba(255, 0, 64, 0.5);
        }}
        
        .status-high {{
            background: linear-gradient(135deg, var(--warning-orange), var(--neon-pink));
            color: white;
            box-shadow: 0 10px 40px rgba(255, 149, 0, 0.5);
        }}
        
        .status-moderate {{
            background: linear-gradient(135deg, var(--cyber-blue), var(--neon-purple));
            color: white;
            box-shadow: 0 10px 40px rgba(0, 217, 255, 0.5);
        }}
        
        .status-low {{
            background: linear-gradient(135deg, var(--success-green), var(--cyber-green));
            color: var(--bg-dark);
            box-shadow: 0 10px 40px rgba(0, 255, 136, 0.5);
        }}
        
        /* Vulnerability List with Advanced Animations */
        .vuln-list {{
            list-style: none;
        }}
        
        .vuln-item {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 2px solid var(--card-border);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: slideIn 0.6s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        .vuln-item::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 5px;
            height: 100%;
            background: var(--cyber-blue);
            transition: width 0.4s;
        }}
        
        .vuln-item:hover {{
            transform: translateX(10px);
            border-color: var(--cyber-green);
            box-shadow: 
                -10px 0 40px rgba(0, 255, 65, 0.2),
                0 10px 40px rgba(0, 217, 255, 0.2);
        }}
        
        .vuln-item:hover::before {{
            width: 100%;
            opacity: 0.1;
        }}
        
        .vuln-item.critical::before {{
            background: var(--critical-red);
        }}
        
        .vuln-item.high::before {{
            background: var(--warning-orange);
        }}
        
        .vuln-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .vuln-cve {{
            font-family: 'Share Tech Mono', monospace;
            font-size: 1.4em;
            font-weight: 700;
            color: var(--cyber-green);
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            animation: flicker 3s infinite;
        }}
        
        @keyframes flicker {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
        }}
        
        .severity-badge {{
            padding: 8px 20px;
            border-radius: 20px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }}
        
        .severity-badge::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.2);
            transform: translate(-50%, -50%) scale(0);
            border-radius: 50%;
            transition: transform 0.6s;
        }}
        
        .severity-badge:hover::after {{
            transform: translate(-50%, -50%) scale(2);
        }}
        
        .severity-critical {{
            background: var(--critical-red);
            color: white;
            box-shadow: 0 0 20px rgba(255, 0, 64, 0.5);
        }}
        
        .severity-high {{
            background: var(--warning-orange);
            color: white;
            box-shadow: 0 0 20px rgba(255, 149, 0, 0.5);
        }}
        
        .severity-medium {{
            background: var(--cyber-blue);
            color: white;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
        }}
        
        .severity-low {{
            background: var(--success-green);
            color: var(--bg-dark);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        }}
        
        .vuln-details {{
            margin-top: 20px;
        }}
        
        .vuln-row {{
            display: flex;
            margin-bottom: 12px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 6px;
            transition: all 0.3s;
        }}
        
        .vuln-row:hover {{
            background: rgba(0, 217, 255, 0.1);
            transform: translateX(5px);
        }}
        
        .vuln-label {{
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            color: var(--cyber-blue);
            min-width: 180px;
            font-size: 0.95em;
        }}
        
        .vuln-value {{
            color: var(--text-primary);
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.95em;
        }}
        
        .vuln-description {{
            background: rgba(0, 217, 255, 0.05);
            border-left: 4px solid var(--cyber-blue);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            line-height: 1.8;
            color: var(--text-primary);
            position: relative;
            overflow: hidden;
        }}
        
        .vuln-description::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.1), transparent);
            animation: shimmer 3s infinite;
        }}
        
        .vuln-description strong {{
            color: var(--cyber-green);
            font-family: 'Orbitron', sans-serif;
        }}
        
        .remediation-box {{
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.1), rgba(0, 217, 255, 0.1));
            border: 2px solid var(--cyber-green);
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
            position: relative;
            overflow: hidden;
        }}
        
        .remediation-box::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 255, 65, 0.2) 0%, transparent 70%);
            animation: rotate 6s linear infinite;
        }}
        
        .remediation-box strong {{
            color: var(--cyber-green);
            font-family: 'Orbitron', sans-serif;
            position: relative;
            z-index: 1;
        }}
        
        .remediation-box ul {{
            margin-top: 15px;
            position: relative;
            z-index: 1;
        }}
        
        .remediation-box li {{
            margin-bottom: 8px;
            padding-left: 10px;
            border-left: 2px solid var(--cyber-green);
            transition: all 0.3s;
        }}
        
        .remediation-box li:hover {{
            border-left-width: 4px;
            padding-left: 15px;
            color: var(--cyber-green);
        }}
        
        .no-vulns {{
            text-align: center;
            padding: 60px;
            color: var(--success-green);
            font-size: 1.5em;
            font-family: 'Orbitron', sans-serif;
            animation: fadeIn 1s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        /* Footer with Glowing Effect */
        .footer {{
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            padding: 40px;
            text-align: center;
            color: var(--text-secondary);
            border-top: 2px solid var(--cyber-blue);
            position: relative;
            overflow: hidden;
        }}
        
        .footer::before {{
            content: '';
            position: absolute;
            top: -2px;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--cyber-green), transparent);
            animation: footerGlow 3s infinite;
        }}
        
        @keyframes footerGlow {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        
        .footer strong {{
            color: var(--cyber-green);
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2em;
        }}
        
        .footer .timestamp {{
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.9em;
            margin-top: 15px;
            color: var(--cyber-blue);
        }}
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {{
            width: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-darker);
            border-left: 1px solid var(--card-border);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, var(--cyber-green), var(--cyber-blue));
            border-radius: 6px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, var(--cyber-blue), var(--neon-purple));
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2.5em;
            }}
            
            .dashboard {{
                grid-template-columns: 1fr;
            }}
            
            .vuln-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            body {{
                background: white;
                color: black;
            }}
            
            .matrix-bg, .grid-bg, .scan-line, .particles {{
                display: none;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <!-- Animated Backgrounds -->
    <div class="matrix-bg">
        <canvas id="matrixCanvas"></canvas>
    </div>
    <div class="grid-bg"></div>
    <div class="scan-line"></div>
    <div class="particles" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <h1>🛡️ LAYERGUARD</h1>
            <div class="subtitle">Layer-Aware Container Forensic Threat Scanner</div>
            <div class="image-name">{self.image_name}</div>
        </div>
        
        <div class="content">
            <!-- Security Summary Dashboard -->
            <div class="section">
                <h2 class="section-title">⚡ Security Summary</h2>
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
                        <div style="margin-top: 15px; color: var(--text-secondary); font-size: 0.9em;">
                            Inherited from base image
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Application Layer Vulnerabilities</div>
                        <div class="card-value">{self.classified_vulns['app_count']}</div>
                        <div style="margin-top: 15px; color: var(--text-secondary); font-size: 0.9em;">
                            From application dependencies
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Total Layers</div>
                        <div class="card-value">{self.layer_analysis['total_layers']}</div>
                        <div style="margin-top: 15px; color: var(--text-secondary); font-size: 0.9em;">
                            Base: {self.layer_analysis['base_image']}
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 40px;">
                    <div class="status-badge {security_status['class']}">{security_status['text']}</div>
                </div>
            </div>
            
            <!-- Top Vulnerabilities -->
            <div class="section">
                <h2 class="section-title">🎯 Top High-Severity Vulnerabilities</h2>
                {self._generate_vulnerability_list(top_vulns)}
            </div>
            
            <!-- Remediation Recommendations -->
            <div class="section">
                <h2 class="section-title">💡 Remediation Recommendations</h2>
                {self._generate_remediation_section()}
            </div>
        </div>
        
        <div class="footer">
            <strong>LAYERGUARD</strong> - Elite Container Security Analysis
            <div class="timestamp">Report Generated: {timestamp}</div>
        </div>
    </div>
    
    <script>
        // Matrix Rain Effect
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        
        function drawMatrix() {{
            ctx.fillStyle = 'rgba(10, 14, 39, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ff41';
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {{
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {{
                    drops[i] = 0;
                }}
                drops[i]++;
            }}
        }}
        
        setInterval(drawMatrix, 50);
        
        window.addEventListener('resize', () => {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }});
        
        // Generate Floating Particles
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 50; i++) {{
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (15 + Math.random() * 10) + 's';
            particlesContainer.appendChild(particle);
        }}
        
        // Smooth Scroll Animation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});
        
        // Intersection Observer for Animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        document.querySelectorAll('.section').forEach(section => {{
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
            section.style.transition = 'opacity 0.8s, transform 0.8s';
            observer.observe(section);
        }});
    </script>
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
                'text': '❌ CRITICAL THREAT DETECTED',
                'class': 'status-critical'
            }
        elif self.vuln_summary['HIGH'] > 0:
            return {
                'text': '⚠️ HIGH RISK IDENTIFIED',
                'class': 'status-high'
            }
        elif self.vuln_summary['MEDIUM'] > 0:
            return {
                'text': '⚡ MODERATE RISK LEVEL',
                'class': 'status-moderate'
            }
        else:
            return {
                'text': '✅ SECURE - LOW RISK',
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
            return '<div class="no-vulns">✅ No high-severity vulnerabilities detected!</div>'
        
        html_items = []
        
        for vuln in vulnerabilities:
            severity_class = vuln['severity'].lower()
            cve_id = vuln['vulnerability_id']
            package = vuln['package']
            installed = vuln['installed_version']
            fixed = vuln['fixed_version'] or 'Not available'
            
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
                        <strong>Security Impact:</strong> {explanation}
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
        
        if severity == 'CRITICAL':
            return f"This is a critical security flaw in {package} that could allow attackers to gain unauthorized access, execute malicious code, or completely compromise your system. Immediate remediation is required to prevent potential exploitation."
        elif severity == 'HIGH':
            return f"This high-severity vulnerability in {package} poses a significant security risk and could be exploited by attackers to compromise your application, steal sensitive data, or disrupt operations. Priority remediation is strongly recommended."
        else:
            return f"This vulnerability in {package} has been identified and should be addressed to maintain security best practices and reduce attack surface."
    
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
                    <strong>✅ PATCH AVAILABLE:</strong> Update {package} to version {fixed} or higher to eliminate this vulnerability.
                </div>
            """
        else:
            return f"""
                <div class="remediation-box">
                    <strong>⚠️ NO PATCH AVAILABLE:</strong> Consider implementing compensating controls, using alternative packages, or isolating this component until a security patch is released.
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
                    <strong>🔄 BASE IMAGE UPDATE REQUIRED:</strong> {self.classified_vulns['base_count']} vulnerabilities are inherited from the base image ({self.layer_analysis['base_image']}). Consider updating to the latest stable version or migrating to a more secure base image variant (Alpine, Distroless, or hardened images).
                </div>
            """)
        
        # Package updates
        fixable = [v for v in self.vulnerable_packages if v.get('fixed_version')]
        if fixable:
            recommendations.append(f"""
                <div class="remediation-box">
                    <strong>📦 PACKAGE UPDATES AVAILABLE:</strong> {len(fixable)} vulnerable packages have security patches available. Update these packages to their fixed versions to resolve known vulnerabilities and reduce attack surface.
                </div>
            """)
        
        # Security best practices
        recommendations.append("""
            <div class="remediation-box">
                <strong>🔒 SECURITY HARDENING RECOMMENDATIONS:</strong>
                <ul style="margin-top: 15px; margin-left: 20px; line-height: 1.8;">
                    <li>Implement multi-stage Docker builds to minimize final image size and attack surface</li>
                    <li>Remove unnecessary packages, development tools, and build dependencies from production images</li>
                    <li>Integrate automated security scanning into CI/CD pipeline for continuous monitoring</li>
                    <li>Establish regular update cycles for base images and application dependencies</li>
                    <li>Apply principle of least privilege for container runtime permissions and capabilities</li>
                    <li>Use container image signing and verification to ensure supply chain integrity</li>
                    <li>Implement runtime security monitoring and anomaly detection</li>
                </ul>
            </div>
        """)
        
        return ''.join(recommendations)