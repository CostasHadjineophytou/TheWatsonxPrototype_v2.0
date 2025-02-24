import logging
from backend.services.base_client import BaseClient
from .iam_token import IAMTokenService
from ..utils.errors import AuthenticationError

class CredentialsManager(BaseClient):
    """Manages service credentials for IBM Cloud services."""
    
    def __init__(self):
        super().__init__()
        self.iam_service = IAMTokenService()
        self.resource_url = "https://resource-controller.cloud.ibm.com/v2/resource_instances"

    def get_service_credentials(self, service_name: str):
        """Get credentials for a specific service by name."""
        try:
            # Optional additional validation beyond "just have an API key"
            self.validator.validate_credentials({"api_key": self.api_key})
            
            # Acquire an IAM token for further calls
            token = self.iam_service.get_iam_token()
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json',
            }

            # Example: get the resource instances to find the relevant service
            response_json = self._make_request(
                method='GET',
                url=self.resource_url,
                headers=headers
            )
            resources = response_json.get('resources', [])

            # Look for any resource whose name matches 'service_name'
            for resource in resources:
                if service_name.lower() in resource['name'].lower():
                    instance_id = resource['guid']
                    return self._get_or_create_credentials(instance_id, headers)

            raise AuthenticationError(
                message=f"No instance found for service: {service_name}",
                code="RESOURCE_NOT_FOUND",
                details={"service_name": service_name}
            )

        except AuthenticationError as auth_err:
            logging.error(f"Service credentials error: {auth_err}")
            raise auth_err
        except Exception as e:
            raise self.handle_error(e, "Failed to get service credentials")

    def _get_or_create_credentials(self, instance_id: str, headers: dict):
        """Get existing credentials or create new ones if none exist."""
        keys_url = f"{self.resource_url}/{instance_id}/resource_keys"

        try:
            # 1. Try to get existing credentials
            key_response = self._make_request(
                method='GET',
                url=keys_url,
                headers=headers
            )
            keys = key_response.get('resources', [])
            if keys:
                return keys[0].get('credentials')

            # 2. Create new credentials if none exist
            data = {
                'name': 'auto-generated-credentials',
                'source': instance_id,
                'role': 'Writer'
            }
            create_response = self._make_request(
                method='POST',
                url=keys_url,
                headers=headers,
                data=data
            )
            return create_response.get('credentials')

        except Exception as e:
            raise self.handle_error(e, "Failed to retrieve or create resource keys") 