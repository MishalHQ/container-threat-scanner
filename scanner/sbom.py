"""
Software Bill of Materials (SBOM) generation using Syft
"""

import logging
import json
from pathlib import Path
from .utils import run_command, ensure_reports_directory, sanitize_image_name


class SBOMGenerator:
    """
    Generates SBOM for container images using Syft
    """
    
    def __init__(self, image_name):
        """
        Initialize SBOM generator
        
        Args:
            image_name (str): Docker image name/tag
        """
        self.image_name = image_name
        self.logger = logging.getLogger(__name__)
        self.sbom_data = None
        self.sbom_path = None
    
    def generate(self):
        """
        Generate SBOM using Syft
        
        Returns:
            dict: SBOM data
        """
        self.logger.info(f"Generating SBOM for: {self.image_name}")
        
        try:
            # Ensure reports directory exists
            reports_dir = ensure_reports_directory()
            
            # Generate output filename
            safe_name = sanitize_image_name(self.image_name)
            self.sbom_path = reports_dir / f"sbom_{safe_name}.json"
            
            # Run Syft
            result = run_command([
                'syft',
                self.image_name,
                '-o', 'json'
            ])
            
            # Parse and save SBOM
            self.sbom_data = json.loads(result.stdout)
            
            with open(self.sbom_path, 'w') as f:
                json.dump(self.sbom_data, f, indent=2)
            
            self.logger.info(f"✓ SBOM saved to: {self.sbom_path}")
            
            return self.sbom_data
            
        except Exception as e:
            self.logger.error(f"Failed to generate SBOM: {str(e)}")
            raise
    
    def get_package_count(self):
        """
        Get total number of packages in SBOM
        
        Returns:
            int: Package count
        """
        if not self.sbom_data:
            return 0
        
        artifacts = self.sbom_data.get('artifacts', [])
        return len(artifacts)
    
    def get_packages(self):
        """
        Get list of packages from SBOM
        
        Returns:
            list: Package information
        """
        if not self.sbom_data:
            return []
        
        artifacts = self.sbom_data.get('artifacts', [])
        packages = []
        
        for artifact in artifacts:
            packages.append({
                'name': artifact.get('name'),
                'version': artifact.get('version'),
                'type': artifact.get('type'),
                'locations': artifact.get('locations', [])
            })
        
        return packages
    
    def get_package_by_name(self, package_name):
        """
        Find package by name in SBOM
        
        Args:
            package_name (str): Package name to search
            
        Returns:
            dict: Package information or None
        """
        packages = self.get_packages()
        for pkg in packages:
            if pkg['name'] == package_name:
                return pkg
        return None