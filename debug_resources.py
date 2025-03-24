from backend.utils.service_utils import get_available_resources
from backend.config.config import Config
import json

def debug_resources():
    """Debug script to print all available resources in IBM Cloud account"""
    try:
        # Get API key from config
        api_key = Config.IBM_CLOUD_API_KEY
        
        if not api_key:
            print("Error: API key not found in config")
            return
            
        # Get all resources
        resources = get_available_resources(api_key)
        
        # Create a file for output
        with open("resource_debug.txt", "w") as f:
            f.write("Resources CRN check (direct from API):\n")
            for resource in resources:
                id_str = resource.get('id', '').lower()
                name = resource.get('name', '').lower()
                f.write(f"Resource name: {name}\n")
                f.write(f"Resource CRN: {id_str}\n")
                
                # Check for keywords that would identify the service
                f.write(f"  Has 'natural-language-understanding': {'natural-language-understanding' in id_str}\n")
                f.write(f"  Has 'speech-to-text': {'speech-to-text' in id_str}\n")
                f.write(f"  Has 'text-to-speech': {'text-to-speech' in id_str}\n")
                f.write(f"  Has 'pm-20': {'pm-20' in id_str}\n")
                f.write(f"  Has 'data-science-experience': {'data-science-experience' in id_str}\n")
                f.write(f"  Has 'cloud-object-storage': {'cloud-object-storage' in id_str}\n")
                f.write("\n")
                
        print("Resource information written to resource_debug.txt")
            
    except Exception as e:
        print(f"Error debugging resources: {str(e)}")

if __name__ == "__main__":
    debug_resources() 