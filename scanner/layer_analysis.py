"""
Docker image layer analysis module
Extracts and analyzes container image layers
"""

import logging
import re
import json
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
            
            # Identify base image using docker inspect (more reliable)
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
        Identify the base image using docker inspect (more reliable than parsing history)
        """
        self.logger.debug("Identifying base image using docker inspect...")
        
        try:
            # Method 1: Use docker inspect to get Config.Image
            result = run_command([
                'docker', 'inspect',
                '--format', '{{json .Config}}',
                self.image_name
            ])
            
            config = json.loads(result.stdout.strip())
            
            # Try to get base image from labels or config
            if 'Image' in config and config['Image']:
                # This contains the parent image SHA or name
                parent_image = config['Image']
                
                # If it's a SHA, try to resolve it to a name
                if parent_image.startswith('sha256:'):
                    self.base_image = self._resolve_base_from_history()
                else:
                    self.base_image = parent_image
            else:
                # Fallback to history parsing
                self.base_image = self._resolve_base_from_history()
            
            # Validate the base image string
            if self.base_image and self._is_valid_base_image(self.base_image):
                self.logger.debug(f"Base image identified: {self.base_image}")
            else:
                self.logger.warning("Could not reliably identify base image")
                self.base_image = "Unknown (Parsing Issue)"
                
        except Exception as e:
            self.logger.warning(f"Error identifying base image: {str(e)}")
            self.base_image = "Unknown (Parsing Issue)"
    
    def _resolve_base_from_history(self):
        """
        Fallback method: Extract base image from docker history
        
        Returns:
            str: Base image name or None
        """
        for layer in reversed(self.layers):
            if layer['type'] == 'base':
                created_by = layer['created_by']
                
                # Try multiple patterns to extract base image
                patterns = [
                    r'FROM\s+([^\s]+)',  # Standard FROM instruction
                    r'#\(nop\)\s+FROM\s+([^\s]+)',  # Nop FROM
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, created_by, re.IGNORECASE)
                    if match:
                        base_name = match.group(1)
                        # Clean up the base name
                        base_name = base_name.strip('"\'')
                        if base_name and base_name != 'scratch':
                            return base_name
        
        # If no FROM found, try to infer from image name
        # For official images like nginx:latest, the base might be debian/alpine
        if ':' in self.image_name:
            image_base = self.image_name.split(':')[0]
            # Common base images
            if any(base in image_base.lower() for base in ['alpine', 'debian', 'ubuntu', 'centos', 'fedora']):
                return self.image_name
        
        return None
    
    def _is_valid_base_image(self, base_image):
        """
        Validate that base image string is clean and usable
        
        Args:
            base_image (str): Base image string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not base_image:
            return False
        
        # Check for broken artifacts
        invalid_patterns = [
            r'\$\w+',  # Shell variables like $server
            r'[{}]',   # Curly braces
            r'\\[nrt]',  # Escape sequences
            r'^\s*$',  # Empty or whitespace only
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, base_image):
                self.logger.warning(f"Invalid base image pattern detected: {base_image}")
                return False
        
        return True
    
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