from google.auth.transport import requests
from google.oauth2 import id_token
import requests as http_requests  # Renamed to avoid naming conflict

target_audience = "https://europe-west1-wallet-login-45c1c.cloudfunctions.net/StellarGladiusContracts"

auth_req = requests.Request()
id_token_credentials = id_token.fetch_id_token(auth_req, target_audience)


headers = {
        "Authorization": f"Bearer {id_token_credentials}",
        "Content-Type": "application/json"
    }

data = {
    "contract_func": "mint",
    'to_address': 'GALT6V5AXC56AS6XY6XIKET25I3GRII2EIMSXFBVKGGSQT3AKQNLCETY',
    'amount': '222'
}

def call_soroban(request):
   
    response = http_requests.post(target_audience, headers=headers, json=data)
    #print(response.text)
    if response.status_code == 200:
        return 'Function call was successful: ' + response.text
    else:
        return f'Function call failed with status code {response.status_code}'

