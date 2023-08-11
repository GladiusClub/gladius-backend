import requests

# Replace with the URL of your deployed Google Cloud Function
function_url = "https://us-central1-wallet-login-45c1c.cloudfunctions.net/mumbai_token_transfer"
#function_url = "http://127.0.0.1:5000/transfer"

#with open('token.txt', 'r') as file:
#    firebase_id_token = file.read().strip()

firebase_id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmM2I1YWRhM2NhMzkxNTQ4ZDM1OTJiMzU5MjkyM2UzNjAxMmI5MTQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXVkIjoid2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXV0aF90aW1lIjoxNjkxNzU3NDExLCJ1c2VyX2lkIjoiNEVmZ0tLOUZzVVZMMzVvTktXU1EyMVZHNXB6MiIsInN1YiI6IjRFZmdLSzlGc1VWTDM1b05LV1NRMjFWRzVwejIiLCJpYXQiOjE2OTE3NTc0MTIsImV4cCI6MTY5MTc2MTAxMiwiZW1haWwiOiJib2JAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYm9iQGV4YW1wbGUuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.UFRiiFjAmTzl4FyMpj_h9QnQEklI9twgRMYbXeohfbDtXpQ-DQShv86iAPjJcOYnhBpCeQZW-fu-0qjcTJ3CIGL4iaKSDYv-2qZs4hwnpOrQsMdNUr60lB9Ycfgmm6_GRoJJ2fb6QysefgwdTJtfFjSLhm93DKn2iQSeSV0t-jsFM3k1hWZCBosgQaXcyu0WChnaHGLpQNQf54loWhDCxytmatMel4rsy64kZWLV3zXLUt8CSPz084wwKgGhgsd2Ehf5-bTR09b7IXaD7cywMJh8ioz1Z533zHNM8av_zP0znaUSBhReWyPIHlsl6tb7rc-Jx7hP-u06C6KeB-LZLQ"


# Replace with the transactions you want to send
transactions = [
    {
        "to_address": "0x67c851F6805041ba34830F4479c4688e908FC26f",
        "amount": "0.05"
    },
    {
        "to_address": "0xFA8b27A0d9C5Bf7490ea03eDAB652c3a18cAc19b",
        "amount": "0.06"
    },
    {
        "to_address": "0x4093a8F669e227f5267FE4946F948eE981957BA2",
        "amount": "0.07"
    }
]

# Set the headers for the request
headers = {
    'Authorization': f'Bearer {firebase_id_token}',
    "Content-Type": "application/json"
}

# Prepare the JSON payload
json_payload = {
    "transactions": transactions
}

# Make the POST request to the Flask app
response = requests.post(function_url, json=json_payload, headers=headers)

# Print the response
print(response.status_code)
print(response.text)
