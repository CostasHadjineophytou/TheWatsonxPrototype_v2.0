import requests
import json
import logging
from backend.config.config import Config
from backend.utils.token_utils import get_iam_token

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_resources_api():
    """Debug script to directly access the IBM Cloud resources API and analyze the response"""
    try:
        # Get API key from config
        api_key = Config.IBM_CLOUD_API_KEY
        
        if not api_key:
            logger.error("Error: API key not found in config")
            return
            
        # Get IAM token
        token = get_iam_token(api_key)
        logger.debug(f"Successfully retrieved IAM token")
        
        # Set up request for resource list
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Make the request to the IBM Cloud API
        resource_url = Config.IBM_CLOUD_RESOURCE_URL
        logger.debug(f"Making request to: {resource_url}")
        response = requests.get(resource_url, headers=headers)
        response.raise_for_status()
        
        # Get resources from response
        data = response.json()
        resources = data.get('resources', [])
        logger.debug(f"Received {len(resources)} resources from API")
        
        # Write raw response to file for analysis
        with open("api_response.json", "w") as f:
            json.dump(data, f, indent=2)
        logger.info("Raw API response written to api_response.json")
        
        # Define service identifiers to check for
        service_identifiers = {
            "natural-language-understanding": {
                "crn_identifiers": ["natural-language-understanding"],
                "name_identifiers": ["natural language understanding", "nlu"]
            },
            "speech-to-text": {
                "crn_identifiers": ["speech-to-text"],
                "name_identifiers": ["speech to text", "stt"]
            },
            "text-to-speech": {
                "crn_identifiers": ["text-to-speech"],
                "name_identifiers": ["text to speech", "tts"]
            },
            "watson-machine-learning": {
                "crn_identifiers": ["pm-20", "machine-learning"],
                "name_identifiers": ["watson machine learning", "wml", "machine learning"]
            },
            "watson-studio": {
                "crn_identifiers": ["data-science-experience"],
                "name_identifiers": ["watson studio", "studio"]
            },
            "cloud-object-storage": {
                "crn_identifiers": ["cloud-object-storage"],
                "name_identifiers": ["cloud object storage", "cos"]
            }
        }
        
        # Analyze resources with focus on all services
        with open("api_resources_detailed.txt", "w") as f:
            f.write("=== IBM Cloud Resources Detailed Analysis ===\n\n")
            f.write(f"Total resources found: {len(resources)}\n\n")
            
            # Track found resources
            found_resources = {service: [] for service in service_identifiers.keys()}
            
            # Examine each resource in detail
            for i, resource in enumerate(resources):
                res_name = resource.get('name', 'Unknown')
                res_crn = resource.get('id', 'Unknown')
                res_name_lower = res_name.lower()
                res_crn_lower = res_crn.lower()
                res_guid = resource.get('guid', 'Unknown')
                res_type = resource.get('type', 'Unknown')
                
                f.write(f"Resource #{i+1}:\n")
                f.write(f"  Name: {res_name}\n")
                f.write(f"  CRN: {res_crn}\n")
                f.write(f"  GUID: {res_guid}\n")
                f.write(f"  Type: {res_type}\n")
                f.write(f"  Resource Group ID: {resource.get('resource_group_id', 'Unknown')}\n")
                f.write(f"  Resource Plan ID: {resource.get('resource_plan_id', 'Unknown')}\n")
                f.write(f"  Region: {resource.get('region_id', 'Unknown')}\n")
                f.write(f"  State: {resource.get('state', 'Unknown')}\n")
                
                # Print all available fields for thorough analysis
                f.write("  All fields:\n")
                for key, value in resource.items():
                    if key not in ['name', 'id', 'guid', 'type', 'resource_group_id', 
                                  'resource_plan_id', 'region_id', 'state']:
                        f.write(f"    {key}: {value}\n")
                
                # Check for service matches
                f.write("  Service matching:\n")
                for service_name, identifiers in service_identifiers.items():
                    crn_matches = []
                    name_matches = []
                    
                    # Check CRN identifiers
                    for crn_id in identifiers['crn_identifiers']:
                        if crn_id in res_crn_lower:
                            crn_matches.append(crn_id)
                    
                    # Check name identifiers
                    for name_id in identifiers['name_identifiers']:
                        if name_id in res_name_lower:
                            name_matches.append(name_id)
                    
                    if crn_matches or name_matches:
                        f.write(f"    {service_name}: MATCH\n")
                        f.write(f"      CRN matches: {', '.join(crn_matches) if crn_matches else 'None'}\n")
                        f.write(f"      Name matches: {', '.join(name_matches) if name_matches else 'None'}\n")
                        
                        # Add to found resources
                        found_resources[service_name].append({
                            'name': res_name,
                            'crn': res_crn,
                            'matches': {
                                'crn': crn_matches,
                                'name': name_matches
                            }
                        })
                
                f.write("\n")
            
            # Summary of found services
            f.write("\n=== Service Detection Summary ===\n\n")
            for service_name, matches in found_resources.items():
                if matches:
                    f.write(f"{service_name}: FOUND ({len(matches)} resources)\n")
                    for match in matches:
                        f.write(f"  - {match['name']}\n")
                        f.write(f"    CRN: {match['crn']}\n")
                        f.write(f"    Matched by: CRN={match['matches']['crn']}, Name={match['matches']['name']}\n")
                else:
                    f.write(f"{service_name}: NOT FOUND\n")
            
            # Add debugging recommendations
            f.write("\n=== Recommendations ===\n")
            for service_name, matches in found_resources.items():
                if not matches:
                    f.write(f"- Add additional identifiers for {service_name} in the validator\n")
            
        logger.info("Detailed resource analysis written to api_resources_detailed.txt")
        
    except Exception as e:
        logger.error(f"Error debugging resources: {str(e)}")

if __name__ == "__main__":
    debug_resources_api() 