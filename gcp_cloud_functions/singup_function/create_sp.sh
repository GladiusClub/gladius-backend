gcloud functions deploy firebase_auth_sync \
  --runtime python310 \
  --trigger-event providers/firebase.auth/eventTypes/user.create \
  --source=./ \
  --entry-point=create_user_document