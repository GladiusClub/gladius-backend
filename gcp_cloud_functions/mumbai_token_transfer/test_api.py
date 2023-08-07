import requests

# Replace with the URL of your deployed Google Cloud Function
function_url = "https://us-central1-wallet-login-45c1c.cloudfunctions.net/mumbai_token_transfer"
#function_url = "http://127.0.0.1:5000/transfer"

#with open('token.txt', 'r') as file:
#    firebase_id_token = file.read().strip()

firebase_id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjYyM2YzNmM4MTZlZTNkZWQ2YzU0NTkyZTM4ZGFlZjcyZjE1YTBmMTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXVkIjoid2FsbGV0LWxvZ2luLTQ1YzFjIiwiYXV0aF90aW1lIjoxNjkxNDI3NzM3LCJ1c2VyX2lkIjoiNEVmZ0tLOUZzVVZMMzVvTktXU1EyMVZHNXB6MiIsInN1YiI6IjRFZmdLSzlGc1VWTDM1b05LV1NRMjFWRzVwejIiLCJpYXQiOjE2OTE0Mjc3MzgsImV4cCI6MTY5MTQzMTMzOCwiZW1haWwiOiJib2JAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYm9iQGV4YW1wbGUuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.gh0ZOeJKJrjxOR-I8Wk8QQBqMfv_Ck9kW4UCvAVqY5stPg1rNF7lN7GYH-QCk4Nzg9gA3eNSpsdWvd1pCczE_uVHw6FILxeQol4agVBbA45VrIIciqkMhjk-mYwXYEGbtCBBzlfalOn1tUz-GuyTnjNZT7p8X2JfgIlS52Qmh0gyX5_eh790JF8VdVwy0D0LASFc43gzUkRcOdqRfRwRJb0ujdFfTEx8nxivDvI44NVgBrw_jCTDP5YVcXozgHqL2i_TxxZrhaJtkvIaF0lWDsgiEFadYMzCeqwlwDwCq0PhS6Slnh2b-7DjUK7gtaz2WwiLbrdN3wTEdNGwZILhzw"

# Replace with the JSON payload you want to send to the function
json_payload = {
    "to_address": "0xce912F29932994e60A7aEEa9F18F7C16E086CBAc",
    "amount": "0.01",
    "mint": False
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
