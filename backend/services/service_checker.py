import requests
import logging
from typing import Dict, List, Any
from .base_service import BaseService
from .iam_token import IAMTokenService
from ..utils.errors import ServiceError, ValidationError
from ..config.config import Config

class ServiceCheckerService(BaseService):
    """Service for checking IBM Cloud service availability"""
    
    def __init__(self, iam_service: IAMTokenService = None):
        super().__init__()
        self.iam_service = iam_service or IAMTokenService()
        self.resource_controller_url = Config.IBM_CLOUD_RESOURCE_CONTROLLER_URL
        
    def list_services(self) -> List[Dict[str, Any]]:
        """
        List all services available in the user's IBM Cloud account
        
        Returns:
            List of service instances with their details
        """
        try:
            self.validator.validate_resource()
            
            token = self.iam_service.get_iam_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Get resource instances
            endpoint = f"{self.resource_controller_url}/v2/resource_instances"
            response = self._make_request('GET', endpoint, headers=headers)
            
            # Extract resources
            resources = response.get('resources', [])
            
            # Return formatted resources
            return resources
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to list services")
            
    def get_service_details(self, service_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific service
        
        Args:
            service_id: The ID of the service to retrieve
            
        Returns:
            Dictionary containing service details
        """
        try:
            self.validator.validate_resource()
            
            token = self.iam_service.get_iam_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Get resource instance details
            endpoint = f"{self.resource_controller_url}/v2/resource_instances/{service_id}"
            response = self._make_request('GET', endpoint, headers=headers)
            
            return response
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to get service details")
            
    def list_resource_keys(self, service_id: str = None) -> List[Dict[str, Any]]:
        """
        List resource keys (credentials) for services
        
        Args:
            service_id: Optional service ID to filter keys
            
        Returns:
            List of resource keys
        """
        try:
            self.validator.validate_resource()
            
            token = self.iam_service.get_iam_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Build endpoint with optional filter
            endpoint = f"{self.resource_controller_url}/v2/resource_keys"
            if service_id:
                endpoint += f"?resource_instance_id={service_id}"
                
            response = self._make_request('GET', endpoint, headers=headers)
            
            # Extract resources
            keys = response.get('resources', [])
            
            return keys
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to list resource keys")
    
    def _make_request(self, method: str, url: str, headers: Dict = None, data: Dict = None) -> Dict:
        """Make HTTP request with error handling"""
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Return JSON response
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_msg = f"HTTP Error: {status_code}"
            
            try:
                error_data = e.response.json()
                if 'errors' in error_data and error_data['errors']:
                    error_msg = error_data['errors'][0].get('message', error_msg)
            except:
                pass
                
            raise ServiceError(
                message=error_msg,
                code=f"HTTP_{status_code}",
                details={"url": url}
            )
            
        except requests.exceptions.RequestException as e:
            raise ServiceError(
                message=f"Request failed: {str(e)}",
                code="REQUEST_FAILED",
                details={"url": url}
            ) 