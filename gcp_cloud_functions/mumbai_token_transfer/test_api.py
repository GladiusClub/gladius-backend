import requests

# Replace with the URL of your deployed Google Cloud Function
function_url = "https://us-central1-wallet-login-45c1c.cloudfunctions.net/mumbai_token_transfer"
#function_url = "http://127.0.0.1:5000/transfer"

#with open('token.txt', 'r') as file:
#    firebase_id_token = file.read().strip()

firebase_id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmM2I1YWRhM2NhMzkxNTQ4ZDM1OTJiMzU5MjkyM2UzNjAxMmI5MTQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXVkIjoid2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXV0aF90aW1lIjoxNjkxNDc2NzY4LCJ1c2VyX2lkIjoiNEVmZ0tLOUZzVVZMMzVvTktXU1EyMVZHNXB6MiIsInN1YiI6IjRFZmdLSzlGc1VWTDM1b05LV1NRMjFWRzVwejIiLCJpYXQiOjE2OTE0NzY3NjgsImV4cCI6MTY5MTQ4MDM2OCwiZW1haWwiOiJib2JAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYm9iQGV4YW1wbGUuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.brtT2O8D5MVE_9W-vUC1auUZ-ve6ai7i4ORVONfNfcneWK755Wz95Sk0QQTQyaMLKXj81lgdsK1N-M1tYpZxm9I2QkKMWPXa4Of6NTk9mmP09J0fxCtBD5JKwdlvI4SpZzC1LBWULbAQH63E5fyGXoagTtl7_WMjqg9aiBsO18v2bYqoNCsShpzFgd1FeF3lzoSBPxJ0LBadVKgsDYxqVX3mKUCl_aq6jrVUR3RSodfVuqmvYl6VG5uvcm71z7BqR6scpLVIgux82iCzQLW7s1lNxBPUvcaigmo27v2TFff9ID3El4lihmTrNxncVGTVcHyewOlGHNIggtyZExsuWA"

# Replace with the JSON payload you want to send to the function
json_payload = {
    "to_address": "0xce912F29932994e60A7aEEa9F18F7C16E086CBAc",
    "amount": "0.6"
}

# Set the headers for the request
headers = {
    'Authorization': f'Bearer {firebase_id_token}',
    "Content-Type": "application/json"
}

# Make the POST request to the Cloud Function
response = requests.post(function_url, json=json_payload, headers=headers)

# Print the response
print(response.status_code)
print(response.text)
