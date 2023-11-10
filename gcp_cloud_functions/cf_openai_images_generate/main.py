import firebase_admin
from firebase_admin import credentials, auth, firestore
from google.cloud import storage

from openai import OpenAI
#import os
#from dotenv import load_dotenv
from flask import escape, jsonify

# Load the .env file
#load_dotenv()

def generate_image(request):

    ### CORS headers ###
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST",  # Allow both GET and POST methods
            "Access-Control-Allow-Headers": "Content-Type, Authorization",  # Added 'Authorization'
            "Access-Control-Max-Age": "3600",
        }


        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type, Authorization"}

    # Get the Firebase ID token from the Authorization header
    bearer_token = request.headers.get("Authorization")
    if not bearer_token:
        return jsonify({"error": "Authorization token not found"}), 401

    id_token = bearer_token.split(" ")[1]       
    # Call this function to initialize the Firebase Admin SDK in your Cloud Function
    
    ### Firebase initialize_app ###
    try:
        # Replace with your Cloud Storage bucket and the path to the service account credentials JSON file
        bucket_name = "gladius-backend"
        credentials_file_path = "firebase-admi-sdk-d55dc53a0acc.json"

        # Download the service account credentials JSON file from Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(credentials_file_path)
        credentials_file_content = blob.download_as_text()
        print(credentials_file_path + ' was downloaded from ' + bucket_name)

        # Initialize the Firebase Admin SDK with the downloaded service account credentials
               # Create a temporary file to write the credentials content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(credentials_file_content.encode())
            temp_file_path = temp_file.name 

        # Initialize the Firebase Admin SDK with the temporary file
        if not firebase_admin._apps:
            cred = credentials.Certificate(temp_file_path)
            firebase_admin.initialize_app(cred)
        db = firestore.client()

        #cred = credentials.Certificate(credentials_file_content)
        # firebase_admin.initialize_app(cred)

        print('Firebase connection is up')

    except Exception as e:
        print("Error initializing Firebase Admin SDK:", e)


    try:

        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)

        # Access user information from the decoded token
        uid = decoded_token["uid"]
        email = decoded_token["email"]

        print(email + ' is authenticated with uid ' + uid)

        # Retrieve the user's document from the Firestore
        user_doc_ref = db.collection('users').document(uid)
        user_doc = user_doc_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            private_key = user_data.get('privateKey')
            wallet_address = user_data.get('address')
            username = user_data.get('name')
            print(username +'`s wallet is ' +wallet_address ) 

            if private_key:
                # Use the private_key
                #print(f"Private Key {private_key} is loaded from Firebase")
                print(f"private_key was loaded from Firebase")
            else:
                print("private_key not found in user document")
        else:
            print("User document not found")

    except auth.ExpiredIdTokenError as e:
        return jsonify({"error": "Token expired"}), 401, headers

    except Exception as e:
        print("Firebase Error:", e)

    ### OPEN AI API ###
    try:
        print ("initiate OpenAI client")
        # init OpenAI client
        client = OpenAI()

    except Exception as e:
        print('Cannot load OPENAI_API_KEY: ', str(e))
        return jsonify(error=str(e)), 500

    # Ensure the request is JSON
    request_json = request.get_json(silent=True)

    # Check if prompt is provided
    if request_json and 'prompt' in request_json:
        prompt = request_json['prompt']
    else:
        return jsonify(error="Please provide a prompt."), 400

    # Call OpenAI's image generation API
    try:
        response =  client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        )

        # Extract the image URL
        image_url = response.data[0].url
        print('image_url: ' , image_url)
        revised_prompt = response.data[0].revised_prompt
        print("revised_prompt: ", revised_prompt)

        return jsonify(url=image_url)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return jsonify(error=str(e)), 500