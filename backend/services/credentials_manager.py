import logging
from backend.utils.base_client import BaseClient
from backend.services.iam_token import IAMTokenService
from backend.utils.error_handling import handle_api_error
from backend.validators.service_validator import ServiceValidator
import requests

class CredentialsManager(BaseClient):
    """Manages service credentials for IBM Cloud services"""
    
    def __init__(self):
        super().__init__()
        self.iam_service = IAMTokenService()
        self.resource_url = "https://resource-controller.cloud.ibm.com/v2/resource_instances"
        self.validator = ServiceValidator()

    def get_service_credentials(self, service_name: str):
        """Get credentials for a specific service"""
        try:
            # Example: validate that we have an API key/ creds
            self.validator.validate_credentials({
                "api_key": self.api_key  # or any needed info
            })

            token = self.iam_service.get_iam_token()
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json',
            }
            
            # First get the service instance
            response = requests.get(self.resource_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get instances: {response.text}")

            resources = response.json()['resources']
            for resource in resources:
                if service_name.lower() in resource['name'].lower():
                    instance_id = resource['guid']
                    return self._get_or_create_credentials(instance_id, headers)
                    
            raise Exception(f"No instance found for service: {service_name}")
            
        except Exception as e:
            logging.error(f"Failed to get service credentials: {str(e)}")
            raise handle_api_error(e)

    def _get_or_create_credentials(self, instance_id: str, headers: dict):
        """Get existing credentials or create new ones"""
        keys_url = f"{self.resource_url}/{instance_id}/resource_keys"
        
        # Try to get existing credentials
        key_response = requests.get(keys_url, headers=headers)
        if key_response.status_code == 200:
            keys = key_response.json()['resources']
            if keys:
                return keys[0]['credentials']
        
        # Create new credentials if none exist
        data = {
            'name': 'auto-generated-credentials',
            'source': instance_id,
            'role': 'Writer'
        }
        create_response = requests.post(keys_url, headers=headers, json=data)
        if create_response.status_code == 201:
            return create_response.json()['credentials']
            
        raise Exception(f"Failed to create credentials: {create_response.text}") 