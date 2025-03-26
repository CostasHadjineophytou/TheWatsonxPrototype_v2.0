"""
Utility functions for service operations
"""
from ..utils.token_utils import get_iam_token
from ..config.config import Config
import requests
import logging
from typing import List, Dict, Any
from ..utils.errors import ServiceError

def get_available_resources(api_key: str) -> List[Dict[str, Any]]:
    """
    Get all available resources from the user's IBM Cloud account
    
    This function centralizes the logic for retrieving IBM Cloud resources,
    making it reusable across both the ServiceCheckerService and validators.
    
    Args:
        api_key: IBM Cloud API key to use for authentication
        
    Returns:
        List of resource dictionaries
        
    Raises:
        ServiceError: If the request fails
    """
    try:
        # Get IAM token
        token = get_iam_token(api_key)
        
        # Set up request for resource list
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Use query parameters to get all resources
        # limit=100 ensures we get more resources in a single request
        # We include resource_instances and resource_aliases to make sure we get all types
        params = {
            "limit": 100,
            "resource_instance_id": "*",
            "include_related": "true"
        }
        
        resource_url = Config.IBM_CLOUD_RESOURCE_URL
        logging.debug(f"Making request to resource URL: {resource_url}")
        response = requests.get(resource_url, headers=headers, params=params)
        response.raise_for_status()
        
        # Extract resources
        data = response.json()
        resources = data.get('resources', [])
        
        # Debug the number of resources found
        logging.debug(f"Retrieved {len(resources)} resources from IBM Cloud API")
        
        # If no resources are found, try an alternative approach without params
        if not resources:
            logging.debug("No resources found with params, trying without params")
            response = requests.get(resource_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            resources = data.get('resources', [])
            logging.debug(f"Retrieved {len(resources)} resources from IBM Cloud API without params")
        
        return resources
        
    except requests.exceptions.RequestException as e:
        raise ServiceError(
            message=f"Failed to retrieve IBM Cloud resources: {str(e)}",
            code="RESOURCE_RETRIEVAL_FAILED"
        ) 