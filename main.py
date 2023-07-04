from firebase_admin import firestore
from google.cloud import kms
from google.oauth2 import service_account
from firebase_functions import event_handler


SERVICE_ACCOUNT_FILE = '../kms-admin.json'

project_id = 'wallet-login-45c1c'

# Create the credentials object from the service account file.
credentials = service_account.Credentials.from_service_account_file("../kms-admin.json")

# Initialize the app with the credentials and the project ID.
app = firestore.initialize_app(credentials, project_id="your-project-id")

# Get a reference to the Firestore service.
db = firestore.client()

# Build the key name.
key_name = f"projects/{project_id}/locations/global/keyRings/my-key-ring/cryptoKeys/my-key"

# Create a client for Google KMS.
client = kms.KeyManagementServiceClient(credentials=credentials)

# Define a function that encrypts the user private key when a new user document is created in Firestore.
@event_handler.on_document_created(reference="/users/{user_id}")
def encrypt_user_private_key(event):
  # Get the user ID from the event parameters.
  user_id = event.params.get("user_id")

  # Get the user private key from the event data.
  user_private_key = event.data.data().get("private_key")

  # Encrypt the user private key with Google KMS.
  response = client.encrypt(request={"name": key_name, "plaintext": user_private_key})
  encrypted_user_private_key = response.ciphertext

  # Update the user document with the encrypted user private key.
  db.collection("users").document(user_id).update({"private_key": encrypted_user_private_key})
