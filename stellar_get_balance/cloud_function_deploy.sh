gcloud functions deploy getStudentBalance --gen2 --runtime nodejs18 \
--trigger-http \
--entry-point=getStudentBalance \
--region=europe-west1 \
--allow-unauthenticated \
--source ./