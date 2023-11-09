curl -m 70 -X POST https://us-central1-wallet-login-45c1c.cloudfunctions.net/openai_image_generate \
-H "Authorization: bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json" \
-d '{"prompt":"a drammatic siamese cat with sword"}'