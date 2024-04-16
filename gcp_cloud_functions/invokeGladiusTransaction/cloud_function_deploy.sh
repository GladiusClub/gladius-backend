gcloud functions deploy invokeGladiusTransaction --gen2 --runtime nodejs18 \
--trigger-http \
--entry-point=invokeGladiusTransaction \
--region=europe-west1 \
--allow-unauthenticated 