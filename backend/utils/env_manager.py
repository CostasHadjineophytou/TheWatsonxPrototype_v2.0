import os
import re
from typing import Optional
from pathlib import Path

class EnvManager:
    """Manages environment variable changes in the .env file"""
    
    def __init__(self, env_path: str = ".env"):
        self.env_path = env_path
        self._ensure_env_file()
    
    def _ensure_env_file(self):
        """Ensure the .env file exists"""
        if not os.path.exists(self.env_path):
            raise FileNotFoundError(f"Environment file not found at {self.env_path}")
    
    def _read_env_file(self) -> str:
        """Read the entire .env file content"""
        with open(self.env_path, 'r') as f:
            return f.read()
    
    def _write_env_file(self, content: str):
        """Write content to the .env file"""
        with open(self.env_path, 'w') as f:
            f.write(content)
    
    def _update_env_value(self, key: str, value: str) -> bool:
        """Update a specific environment variable value"""
        content = self._read_env_file()
        
        # Pattern to match the key=value format
        pattern = f"^{key}=.*$"
        new_line = f"{key}={value}"
        
        # Check if the key exists
        if re.search(pattern, content, re.MULTILINE):
            # Replace the existing line
            new_content = re.sub(pattern, new_line, content, flags=re.MULTILINE)
        else:
            # Add new line if key doesn't exist
            new_content = content.rstrip() + f"\n{new_line}\n"
        
        self._write_env_file(new_content)
        return True
    
    def update_api_key(self, new_key: str) -> bool:
        """Update the IBM Cloud API key"""
        return self._update_env_value("IBM_CLOUD_API_KEY", new_key)
    
    def update_region(self, new_region: str) -> bool:
        """Update the region in URLs"""
        content = self._read_env_file()
        
        # Update region in all relevant URLs
        urls_to_update = {
            "IBM_CLOUD_MODELS_URL": f"https://{new_region}.ml.cloud.ibm.com",
            "IBM_CLOUD_PROJECTS_URL": f"https://api.{new_region}.dataplatform.cloud.ibm.com"
        }
        
        for key, value in urls_to_update.items():
            self._update_env_value(key, value)
        
        return True
    
    def get_current_region(self) -> Optional[str]:
        """Get the current region from the models URL"""
        content = self._read_env_file()
        match = re.search(r"IBM_CLOUD_MODELS_URL=https://([^.]+)\.ml\.cloud\.ibm\.com", content)
        return match.group(1) if match else None
    
    def get_current_api_key(self) -> Optional[str]:
        """Get the current API key from the .env file"""
        try:
            content = self._read_env_file()
            # Look for uncommented API key line
            match = re.search(r"^IBM_CLOUD_API_KEY=([^#\n]+)", content, re.MULTILINE)
            if match:
                return match.group(1).strip()
            return None
        except Exception:
            return None
    
    def reload_env(self):
        """Reload environment variables from .env file"""
        from dotenv import load_dotenv
        load_dotenv(override=True) 