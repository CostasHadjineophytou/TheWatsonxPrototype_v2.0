from backend.utils.service_utils import get_available_resources
from backend.config.config import Config
import json

def debug_resources_raw():
    """Debug script to print all available resources in IBM Cloud account in raw form"""
    try:
        # Get API key from config
        api_key = Config.IBM_CLOUD_API_KEY
        
        if not api_key:
            print("Error: API key not found in config")
            return
            
        # Get all resources
        resources = get_available_resources(api_key)
        
        print(f"Resource instances: {len(resources)}")
        
        # Create a file for output
        with open("resources_raw.txt", "w") as f:
            f.write("Raw resources from IBM Cloud:\n\n")
            for i, resource in enumerate(resources):
                f.write(f"Resource #{i+1}:\n")
                
                # Extract key fields
                name = resource.get('name', 'Unknown')
                crn = resource.get('id', 'Unknown')
                guid = resource.get('guid', 'Unknown')
                resource_id = resource.get('resource_id', 'Unknown')
                resource_plan_id = resource.get('resource_plan_id', 'Unknown')
                
                f.write(f"Name: {name}\n")
                f.write(f"CRN: {crn}\n")
                f.write(f"GUID: {guid}\n")
                f.write(f"Resource ID: {resource_id}\n")
                f.write(f"Resource Plan ID: {resource_plan_id}\n")
                
                # Check for all keys that might be related to service identifiers
                for key, value in resource.items():
                    if isinstance(value, str) and any(x in value.lower() for x in ['speech', 'text', 'natural', 'watson']):
                        f.write(f"Key '{key}': {value}\n")
                
                f.write("\n")
                
        print("Resource information written to resources_raw.txt")
            
    except Exception as e:
        print(f"Error debugging resources: {str(e)}")

if __name__ == "__main__":
    debug_resources_raw() 