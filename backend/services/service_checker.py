from typing import Dict, List, Any
from .base_client import BaseClient
from .iam_token import IAMTokenService
from ..utils.errors import ServiceError, ValidationError
from ..config.config import Config

class ServiceCheckerService(BaseClient):
    """Service for checking IBM Cloud service availability"""
    
    def __init__(self, iam_service: IAMTokenService = None):
        super().__init__()
        self.iam_service = iam_service or IAMTokenService()
        self.resource_url = Config.IBM_CLOUD_RESOURCE_URL
        
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
            response = self._make_request('GET', self.resource_url, headers=headers)
            
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
            service_url = f"{self.resource_url}/{service_id}"
            response = self._make_request('GET', service_url, headers=headers)
            
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
            
            # Get base URL for resource keys
            base_url = self.resource_url.replace('/resource_instances', '/resource_keys')
            
            # Add service ID filter if provided
            params = {}
            if service_id:
                params = {"resource_instance_id": service_id}
                
            response = self._make_request('GET', base_url, headers=headers, params=params)
            
            # Extract resources
            keys = response.get('resources', [])
            
            return keys
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to list resource keys") 