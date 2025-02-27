import sys
import os
# Go up three levels: unitScripts -> tests -> backend -> root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.services.credentials_manager import CredentialsManager

def test_credentials():
    credentials_manager = CredentialsManager()
    credentials = credentials_manager.get_service_credentials("Natural Language Understanding")
    print(credentials['apikey'])
    print(credentials['url'])

test_credentials()


