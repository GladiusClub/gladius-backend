import requests

# Replace with the URL of your deployed Google Cloud Function
function_url = "https://us-central1-wallet-login-45c1c.cloudfunctions.net/mumbai_token_transfer"

# Replace with your actual Firebase ID token
id_token = "YOUR_FIREBASE_ID_TOKEN"

# Replace with the JSON payload you want to send to the function
json_payload = {
    "to_address": "0xce912F29932994e60A7aEEa9F18F7C16E086CBAc",
    "amount": "0.01",
    "mint": False
}

# Set the headers for the request
headers = {
    "Authorization": f"Bearer {id_token}",
    "Content-Type": "application/json"
}

# Make the POST request to the Cloud Function
response = requests.post(function_url, json=json_payload, headers=headers)

# Print the response
print(response.status_code)
print(response.text)
