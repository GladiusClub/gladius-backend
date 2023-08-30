import firebase_admin
from firebase_admin import credentials, firestore


# Converts strings added to /messages/{pushId}/original to uppercase
def firestore_sync(data, context):

    try:
        # Initialize the Firebase Admin SDK with the temporary file
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-admin.json")
            default_app = firebase_admin.initialize_app(cred)
        # Get a reference to the firestore database
        db = firestore.client()

        print('Firebase connection is up')

    except Exception as e:
        print("Error initializing Firebase Admin SDK:", e)

    try:
        path_parts = context.resource.split("/documents/")[1].split("/")
        collection_path = path_parts[0]
        document_path = "/".join(path_parts[1:])

        affected_doc = db.collection(collection_path).document(document_path)

        # Get the document ID
        userId = affected_doc.id
        print(f"User UID {userId} triggered a change in club roles")

        club_roles = data["value"]["fields"]["clubs_roles"]["arrayValue"]
        print(club_roles)

        # Access the values directly from the dictionary
        values = club_roles.get('values', [])

        if values:
            # Extract club_id and role from the first element if it exists
            first_element = values[0].get('mapValue', {}).get('fields', {})
            club_id = first_element.get('club_id', {}).get('stringValue', '')
            role = first_element.get('role', {}).get('stringValue', '')

            if club_id and role:
                
                # /users collection
                users_collection = db.collection("users")

                # /clubs collection 
                clubs_collection = db.collection("clubs")
                # club ref
                club_ref = clubs_collection.document(club_id)        

                print(f"assign {userId} with role {role} to club {club_id} with the following data:")
                
                # members ref
                members_subcollection = club_ref.collection("members")
                # get user data from /users
                user_doc_ref = users_collection.document(userId)
                user_snapshot = user_doc_ref.get()
                user_data = user_snapshot.to_dict()

                # Set data in the "members" collection
                user_subcollection_data = {
                    "user": userId,
                    "role": role,
                    "name": user_data["name"],
                    "email": user_data["email"],
                }
                print(user_subcollection_data)
                # Add a document to the "members" collection
                members_subcollection.document(userId).set(user_subcollection_data)
                print(f"Added {userId} to {club_id} members as {role}")
                
            else:
                print("club_id or role not found in the data.")
        else:
            print("No values found in the data.")
    
    except Exception as e:
        print("Firebase Error:", e)