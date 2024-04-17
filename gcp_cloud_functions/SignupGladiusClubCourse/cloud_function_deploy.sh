gcloud functions deploy SignupGladiusClubCourse --gen2 \
--runtime nodejs18 \
--trigger-http \
--entry-point=SignupGladiusClubCourse \
--region=europe-west1 \
--allow-unauthenticated 