gcloud functions deploy SignupGladiusClub --gen2 \
--runtime nodejs18 \
--trigger-http \
--entry-point=SignupGladiusClub \
--region=europe-west1 \
--allow-unauthenticated 