import sys
import os
# Go up three levels: unitScripts -> tests -> backend -> root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.services.iam_token import IAMTokenService

def test_iam_token():
    iam_token_service = IAMTokenService()
    token = iam_token_service.get_iam_token()
    print(token[0:10])

test_iam_token()


