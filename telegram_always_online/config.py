#!/usr/bin/env python3
"""
Configuration management for Telegram Always Online
"""

import os
import logging
import json
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(name)

# Default configuration values
DEFAULT_CONFIG = {
    'update_interval': 300,  # Update status every 5 minutes
    'session_dir': None,     # Will be set to user's home directory
    'log_level': 'INFO',
    'daemon_mode': True      # Run in background by default
}

def get_config_dir():
    """Get the configuration directory"""
    # For Linux and Termux, use ~/.config/telegram-always-online
    home_dir = str(Path.home())
    config_dir = os.path.join(home_dir, '.config', 'telegram-always-online')
    
    # Create directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)
    
    return config_dir

def load_config():
    """Load configuration from file"""
    config_dir = get_config_dir()
    config_file = os.path.join(config_dir, 'config.json')
    
    # Load environment variables
    load_dotenv(os.path.join(config_dir, '.env'))
    
    # Set default session directory if not specified
    DEFAULT_CONFIG['session_dir'] = os.path.join(config_dir, 'sessions')
    os.makedirs(DEFAULT_CONFIG['session_dir'], exist_ok=True)
    
    # Load config from file or create default
    config = DEFAULT_CONFIG.copy()
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        else:
            save_config(config)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
    
    return config

def save_config(config):
    """Save configuration to file"""
    config_dir = get_config_dir()
    config_file = os.path.join(config_dir, 'config.json')
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

def update_config(key, value):
    """Update a specific configuration value"""
    config = load_config()
    if key in config:
        config[key] = value
        return save_config(config)
    return False