gcloud functions deploy SignupGladiusParent --gen2 \
--runtime nodejs18 \
--trigger-http \
--entry-point=SignupGladiusParent \
--region=europe-west1 \
--allow-unauthenticated 