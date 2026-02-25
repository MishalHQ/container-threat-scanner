"""
Utility functions for environment validation and logging setup
"""

import subprocess
import logging
import sys
import os
from pathlib import Path


def setup_logging(verbose=False):
    """
    Configure logging for the application
    
    Args:
        verbose (bool): Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('scanner.log')
        ]
    )


def run_command(command, capture_output=True, check=True):
    """
    Execute shell command with proper error handling
    
    Args:
        command (list): Command and arguments as list
        capture_output (bool): Capture stdout/stderr
        check (bool): Raise exception on non-zero exit
        
    Returns:
        subprocess.CompletedProcess: Command result
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Executing command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.cmd}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        raise
    except FileNotFoundError:
        logger.error(f"Command not found: {command[0]}")
        raise


def check_tool_installed(tool_name, version_flag='--version'):
    """
    Check if a command-line tool is installed and accessible
    
    Args:
        tool_name (str): Name of the tool to check
        version_flag (str): Flag to get version info
        
    Returns:
        bool: True if tool is installed, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        result = run_command([tool_name, version_flag], check=False)
        if result.returncode == 0:
            logger.info(f"✓ {tool_name} is installed")
            return True
        else:
            logger.warning(f"✗ {tool_name} returned non-zero exit code")
            return False
    except FileNotFoundError:
        logger.error(f"✗ {tool_name} is not installed or not in PATH")
        return False
    except Exception as e:
        logger.error(f"✗ Error checking {tool_name}: {str(e)}")
        return False


def check_docker_running():
    """
    Check if Docker daemon is running
    
    Returns:
        bool: True if Docker is running, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        result = run_command(['docker', 'info'], check=False)
        if result.returncode == 0:
            logger.info("✓ Docker daemon is running")
            return True
        else:
            logger.error("✗ Docker daemon is not running")
            return False
    except Exception as e:
        logger.error(f"✗ Error checking Docker status: {str(e)}")
        return False


def validate_environment():
    """
    Validate that all required tools are installed and running
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Validating environment...")
    
    all_valid = True
    
    # Check Docker
    if not check_tool_installed('docker'):
        logger.error("Docker is not installed. Please install Docker Desktop.")
        logger.error("Download from: https://www.docker.com/products/docker-desktop")
        all_valid = False
    elif not check_docker_running():
        logger.error("Docker is installed but not running. Please start Docker Desktop.")
        all_valid = False
    
    # Check Syft
    if not check_tool_installed('syft'):
        logger.error("Syft is not installed.")
        logger.error("Install: https://github.com/anchore/syft#installation")
        all_valid = False
    
    # Check Trivy
    if not check_tool_installed('trivy'):
        logger.error("Trivy is not installed.")
        logger.error("Install: https://aquasecurity.github.io/trivy/latest/getting-started/installation/")
        all_valid = False
    
    if all_valid:
        logger.info("✓ All required tools are installed and ready")
    else:
        logger.error("✗ Environment validation failed")
    
    return all_valid


def ensure_reports_directory():
    """
    Create reports directory if it doesn't exist
    
    Returns:
        Path: Path to reports directory
    """
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    return reports_dir


def sanitize_image_name(image_name):
    """
    Sanitize image name for use in filenames
    
    Args:
        image_name (str): Docker image name
        
    Returns:
        str: Sanitized filename-safe string
    """
    return image_name.replace(':', '_').replace('/', '_')