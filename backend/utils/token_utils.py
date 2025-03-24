"""
Utility functions for IBM Cloud IAM token operations
"""
import requests
from ..config.config import Config
from ..utils.errors import AuthenticationError

def get_iam_token(api_key: str) -> str:
    """
    Get an IAM token from IBM Cloud using the provided API key
    
    Args:
        api_key: The IBM Cloud API key to use for authentication
        
    Returns:
        The IAM access token as a string
        
    Raises:
        AuthenticationError: If authentication fails or token retrieval fails
    """
    if not api_key:
        raise AuthenticationError(
            message="No API key provided for token retrieval",
            code="NO_API_KEY_FOR_TOKEN"
        )
        
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }

        # Form data for IBM Cloud's IAM token endpoint
        data = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'apikey': api_key,
        }
        
        token_url = Config.IAM_TOKEN_URL
        response = requests.post(
            url=token_url,
            headers=headers,
            data=data
        )
        response.raise_for_status()
        
        response_json = response.json()
        token = response_json.get('access_token')
        
        if not token:
            raise AuthenticationError(
                message="No access token in response",
                code="NO_TOKEN",
                details={"response": response_json}
            )
            
        return token
        
    except requests.exceptions.RequestException as e:
        raise AuthenticationError(
            message=f"Failed to retrieve IAM token: {str(e)}",
            code="IAM_TOKEN_RETRIEVAL_FAILED"
        ) 