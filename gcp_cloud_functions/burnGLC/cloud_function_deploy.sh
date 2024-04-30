gcloud functions deploy burnGLCauth --gen2 \
--runtime nodejs18 \
--trigger-http \
--entry-point=burnGLC \
--region=europe-west1 \
--allow-unauthenticated  
