import requests
import json

# Replace with your Cloud Function URL
#CLOUD_FUNCTION_URL = "http://127.0.0.1:8080/register"
CLOUD_FUNCTION_URL = "https://us-central1-wallet-login-45c1c.cloudfunctions.net/register_user_no_auth"
# User information for registration
user_info = {
    "user": "Alexey",
    "email": "as.lexus@gmail.com",
    "password": "123456"
    
}

# Convert user_info dictionary to JSON
user_info_json = json.dumps(user_info)

# Set the headers for the request
headers = {
    "Content-Type": "application/json"
}

# Make the API call
response = requests.post(CLOUD_FUNCTION_URL, data=user_info_json, headers=headers)

# Print the response
print("Response status code:", response.status_code)
print("Response data:", response.text)
