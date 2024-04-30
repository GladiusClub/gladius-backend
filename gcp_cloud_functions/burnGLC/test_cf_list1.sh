curl -X POST https://europe-west1-wallet-login-45c1c.cloudfunctions.net/burnGLCauth \
-H "Authorization: Bearer $firebase_id_token" \
-H "Content-Type:application/json" \
-d '{
  "transactions": [
    {
      "amount": "1"
    }
  ]
}'