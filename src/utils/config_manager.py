"""
Configuration Manager for Playwright Test Framework
Handles loading and managing configuration from YAML files
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration loading and environment-specific settings"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self._config: Optional[Dict[str, Any]] = None
        self._active_env: str = "dev"
        self._browser_override: Optional[str] = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file"""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
            
            # Set active environment from ENV variable or default to dev
            self._active_env = os.getenv('ENV', 'dev').lower()
            
            if self._active_env not in self._config.get('environments', {}):
                logger.warning(f"Environment '{self._active_env}' not found in config, using 'dev'")
                self._active_env = 'dev'
                
            logger.info(f"Configuration loaded successfully. Active environment: {self._active_env}")

            # Keep browser selection strictly from config.yaml (no env override)
            self._browser_override = None
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def get_config(self) -> Dict[str, Any]:
        """Get the complete configuration"""
        return self._config or {}
    
    def get_environment_config(self) -> Dict[str, Any]:
        """Get configuration for the active environment"""
        return self._config.get('environments', {}).get(self._active_env, {})
    
    def get_global_config(self) -> Dict[str, Any]:
        """Get global configuration settings"""
        return self._config.get('global', {})
    
    def get_browser_config(self, browser_name: str = None) -> Dict[str, Any]:
        """Get browser configuration"""
        if not browser_name:
            browser_name = self.get_browser()
        
        browsers = self._config.get('browsers', {})
        return browsers.get(browser_name, {})
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting from environment config"""
        env_config = self.get_environment_config()
        return env_config.get(key, default)
    
    def get_global_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting from global config"""
        global_config = self.get_global_config()
        return global_config.get(key, default)
    
    def get_base_url(self) -> str:
        """Get the base URL for the active environment"""
        return self.get_setting('base_url', 'http://localhost:3000')
    
    def get_browser(self) -> str:
        """Get the browser for the active environment"""
        if self._browser_override:
            return self._browser_override
        return self.get_setting('browser', 'chromium')
    
    def get_timeout(self) -> int:
        """Get the timeout value for the active environment"""
        return self.get_setting('timeout', self.get_global_setting('timeout', 30000))
    
    def get_headless(self) -> bool:
        """Get the headless setting for the active environment"""
        return self.get_setting('headless', self.get_global_setting('headless', True))
    
    def get_viewport(self) -> Dict[str, int]:
        """Get the viewport configuration"""
        return self.get_global_setting('viewport', {'width': 1920, 'height': 1080})
    
    def get_trace(self) -> str:
        """Get the trace setting"""
        return self.get_global_setting('trace', 'on-first-retry')
    
    def get_video(self) -> str:
        """Get the video setting"""
        return self.get_global_setting('video', 'retain-on-failure')
    
    def get_screenshot(self) -> str:
        """Get the screenshot setting"""
        return self.get_global_setting('screenshot', 'only-on-failure')
    
    def get_retries(self) -> int:
        """Get the retry count"""
        return self.get_setting('retries', self.get_global_setting('retries', 2))
    
    def get_db_config(self) -> Dict[str, Any]:
        """Get database configuration for the active environment"""
        return self.get_setting('db', {})
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration for the active environment"""
        return self.get_setting('api', {})
    
    def get_test_data(self) -> Dict[str, Any]:
        """Get test data configuration"""
        return self._config.get('test_data', {})
    
    def get_reporting_config(self) -> Dict[str, Any]:
        """Get reporting configuration"""
        return self._config.get('reporting', {})
    
    def get_parallel_config(self) -> Dict[str, Any]:
        """Get parallel execution configuration"""
        return self._config.get('parallel', {})
    
    def get_hooks_config(self) -> Dict[str, Any]:
        """Get hooks configuration"""
        return self._config.get('hooks', {})
    
    def override_browser(self, browser: str) -> None:
        """Override the browser setting for the current session"""
        if browser in self._config.get('browsers', {}):
            self._browser_override = browser
            logger.info(f"Browser overridden to: {browser}")
        else:
            logger.warning(f"Invalid browser '{browser}', using default")
    
    def get_active_environment(self) -> str:
        """Get the currently active environment"""
        return self._active_env
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        self._load_config()


# Global configuration instance
config_manager = ConfigManager()
