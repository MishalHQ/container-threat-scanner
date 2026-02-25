"""
Container Image Threat Scanner
A layer-aware forensic security analysis tool for container images
"""

__version__ = "1.0.0"
__author__ = "DevSecOps Team"

from .layer_analysis import LayerAnalyzer
from .sbom import SBOMGenerator
from .vulnerability import VulnerabilityScanner
from .remediation import RemediationEngine
from .utils import validate_environment, setup_logging

__all__ = [
    'LayerAnalyzer',
    'SBOMGenerator',
    'VulnerabilityScanner',
    'RemediationEngine',
    'validate_environment',
    'setup_logging'
]