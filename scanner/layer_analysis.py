"""
Docker image layer analysis module
Extracts and analyzes container image layers
"""

import logging
import re
from .utils import run_command


class LayerAnalyzer:
    """
    Analyzes Docker image layers and build history
    """
    
    def __init__(self, image_name):
        """
        Initialize layer analyzer
        
        Args:
            image_name (str): Docker image name/tag
        """
        self.image_name = image_name
        self.logger = logging.getLogger(__name__)
        self.layers = []
        self.base_image = None
    
    def pull_image(self):
        """
        Pull Docker image if not present locally
        """
        self.logger.info(f"Pulling image: {self.image_name}")
        try:
            run_command(['docker', 'pull', self.image_name])
            self.logger.info(f"✓ Image pulled successfully")
        except Exception as e:
            self.logger.error(f"Failed to pull image: {str(e)}")
            raise
    
    def analyze_layers(self):
        """
        Analyze image layers using docker history
        
        Returns:
            dict: Layer analysis results
        """
        self.logger.info(f"Analyzing layers for: {self.image_name}")
        
        try:
            # Get layer history
            result = run_command([
                'docker', 'history',
                '--no-trunc',
                '--format', '{{.ID}}|{{.CreatedBy}}|{{.Size}}',
                self.image_name
            ])
            
            layers_raw = result.stdout.strip().split('\n')
            self.layers = []
            
            for idx, layer in enumerate(layers_raw):
                if not layer.strip():
                    continue
                
                parts = layer.split('|', 2)
                if len(parts) >= 3:
                    layer_id, created_by, size = parts
                    
                    self.layers.append({
                        'index': idx,
                        'id': layer_id[:12],  # Short ID
                        'created_by': created_by.strip(),
                        'size': size.strip(),
                        'type': self._classify_layer(created_by)
                    })
            
            # Identify base image (usually the last FROM instruction)
            self._identify_base_image()
            
            self.logger.info(f"✓ Analyzed {len(self.layers)} layers")
            
            return {
                'total_layers': len(self.layers),
                'base_image': self.base_image,
                'layers': self.layers
            }
            
        except Exception as e:
            self.logger.error(f"Failed to analyze layers: {str(e)}")
            raise
    
    def _classify_layer(self, created_by):
        """
        Classify layer type based on creation command
        
        Args:
            created_by (str): Layer creation command
            
        Returns:
            str: Layer classification
        """
        created_by_lower = created_by.lower()
        
        if 'from' in created_by_lower or '/bin/sh -c #(nop)' in created_by_lower:
            return 'base'
        elif 'copy' in created_by_lower or 'add' in created_by_lower:
            return 'application'
        elif 'run' in created_by_lower:
            if any(pkg in created_by_lower for pkg in ['apt', 'yum', 'apk', 'pip', 'npm']):
                return 'dependency'
            return 'build'
        elif 'cmd' in created_by_lower or 'entrypoint' in created_by_lower:
            return 'runtime'
        else:
            return 'metadata'
    
    def _identify_base_image(self):
        """
        Identify the base image from layer history
        """
        for layer in reversed(self.layers):
            if layer['type'] == 'base':
                # Try to extract base image name from created_by
                match = re.search(r'FROM\s+([^\s]+)', layer['created_by'], re.IGNORECASE)
                if match:
                    self.base_image = match.group(1)
                    break
        
        if not self.base_image:
            self.base_image = "Unknown"
    
    def get_base_layers(self):
        """
        Get layers classified as base image layers
        
        Returns:
            list: Base image layers
        """
        return [l for l in self.layers if l['type'] == 'base']
    
    def get_application_layers(self):
        """
        Get layers classified as application layers
        
        Returns:
            list: Application layers
        """
        return [l for l in self.layers if l['type'] in ['application', 'dependency', 'build']]