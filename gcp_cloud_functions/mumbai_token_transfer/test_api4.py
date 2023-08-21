import requests

# Replace with the URL of your deployed Google Cloud Function
function_url = "https://us-central1-wallet-login-45c1c.cloudfunctions.net/mumbai_token_transfer"
#function_url = "http://127.0.0.1:5000/transfer"

#with open('token.txt', 'r') as file:
#    firebase_id_token = file.read().strip()

firebase_id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjYzODBlZjEyZjk1ZjkxNmNhZDdhNGNlMzg4ZDJjMmMzYzIzMDJmZGUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXVkIjoid2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXV0aF90aW1lIjoxNjkyNjM1MjUyLCJ1c2VyX2lkIjoiNEVmZ0tLOUZzVVZMMzVvTktXU1EyMVZHNXB6MiIsInN1YiI6IjRFZmdLSzlGc1VWTDM1b05LV1NRMjFWRzVwejIiLCJpYXQiOjE2OTI2MzUyNTMsImV4cCI6MTY5MjYzODg1MywiZW1haWwiOiJib2JAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYm9iQGV4YW1wbGUuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.ZsJqZqYzqZSyIgAGb0KGm_qAgqAkWOSyQonpJQ_vRG3PCK7fd9CB1Afn5LPdknrXWPTK0X7Fzg84qEfHx2kSqviV5_yr_Suq14wnt__EDKnXjcOaefkb5HpEpwgBRoJqqhapmv8Z0U_knuejdzBiTiJKhO_5fOQSJH3313qqyilI_Z3vrHGSzW3hrWBoEIuF8PRRrhR4ZFgxwjsilWJK-A68pZeJGMC4fgSDC12ZAoDUXiRfhxvpmJM7vX1-ta-QLPFSgRj9q6pJwbxRSX4_UnFRQw8YwNsL-VWSU0Zv-9FeyhjQDIJ_uIbTMHW4ctv87UXgSt4mMUq6ApELc6AlQg"




# Replace with the transactions you want to send
transactions = [
    {
        "to_address": "0x6A15f64d6546418acd9bAe4cc4Bb9e5737386006",
        "amount": "0.02"
    },      
    {
        "to_address": "0xFA8b27A0d9C5Bf7490ea03eDAB652c3a18cAc19b",
        "amount": "0.03"
    },
    {
        "to_address": "0x4093a8F669e227f5267FE4946F948eE981957BA2",
        "amount": "0.04"
    }
]

# Set the headers for the request
headers = {
    'Authorization': f'Bearer {firebase_id_token}',
    "Content-Type": "application/json"
}


for tx in transactions:
    json_payload = {
        "transactions": [tx]
    }

    headers = {
        'Authorization': f'Bearer {firebase_id_token}',
        "Content-Type": "application/json"
    }

    response = requests.post(function_url, json=json_payload, headers=headers)

    print(response.status_code)
    print(response.text)
