import logging
from backend.utils.base_client import BaseClient
from backend.services.iam_token import IAMTokenService

class CredentialsManager(BaseClient):
    """Manages service credentials for IBM Cloud services"""
    
    def __init__(self):
        super().__init__()
        self.iam_service = IAMTokenService()

    def get_service_credentials(self, service_name):
        """Get credentials for a specific service"""
        try:
            token = self.iam_service.get_iam_token()
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json',
            }
            
            # First get the service instance
            resource_url = "https://resource-controller.cloud.ibm.com/v2/resource_instances"
            instances = self._make_request('GET', resource_url, headers=headers)
            
            for instance in instances.get('resources', []):
                if service_name.lower() in instance['name'].lower():
                    instance_id = instance['guid']
                    
                    # Get or create credentials for the instance
                    return self._get_or_create_credentials(instance_id, headers)
                    
            raise ValueError(f"No instance found for service: {service_name}")
            
        except Exception as e:
            logging.error(f"Failed to get service credentials: {str(e)}")
            raise RuntimeError(f"Failed to get service credentials: {str(e)}")

    def _get_or_create_credentials(self, instance_id, headers):
        """Get existing credentials or create new ones"""
        keys_url = f"https://resource-controller.cloud.ibm.com/v2/resource_instances/{instance_id}/resource_keys"
        
        # Try to get existing credentials
        existing_keys = self._make_request('GET', keys_url, headers=headers)
        if existing_keys.get('resources'):
            return existing_keys['resources'][0]['credentials']
            
        # Create new credentials if none exist
        data = {
            'name': f'auto-generated-credentials',
            'source': instance_id,
            'role': 'Writer'
        }
        new_key = self._make_request('POST', keys_url, headers=headers, data=data)
        return new_key['credentials'] 