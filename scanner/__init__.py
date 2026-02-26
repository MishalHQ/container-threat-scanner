"""
LayerGuard - Layer-Aware Container Image Forensic Threat Scanner
A professional security analysis tool for container images
"""

__version__ = "2.0.0"
__author__ = "LayerGuard Security Team"

from .layer_analysis import LayerAnalyzer
from .sbom import SBOMGenerator
from .vulnerability import VulnerabilityScanner
from .remediation import RemediationEngine
from .report_generator import HTMLReportGenerator
from .utils import validate_environment, setup_logging

__all__ = [
    'LayerAnalyzer',
    'SBOMGenerator',
    'VulnerabilityScanner',
    'RemediationEngine',
    'HTMLReportGenerator',
    'validate_environment',
    'setup_logging'
]