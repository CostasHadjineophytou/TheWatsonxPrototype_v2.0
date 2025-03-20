import requests
from backend.config.config import Config
from backend.utils.errors import ConfigurationError
from ..base_component import BaseComponent

class BaseClient(BaseComponent):
    """Base client for making HTTP requests to IBM Cloud services"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.IBM_CLOUD_API_KEY
        
        if not self.api_key:
            raise ConfigurationError(
                message="API key is missing or not configured",
                code="MISSING_API_KEY"
            )

    def _make_request(self, method, url, headers=None, data=None, params=None, is_form_data=False):
        """Make HTTP request with error handling and logging"""
        try:
            headers = headers or {}
            
            if is_form_data:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                    params=params
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data if method in ['POST', 'PUT'] else None,
                    params=params if method == 'GET' else None
                )
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise self.handle_error(e, f"Request failed: {method} {url}") 