curl -X POST https://europe-west1-wallet-login-45c1c.cloudfunctions.net/transferGLCauth \
-H "Authorization: Bearer $firebase_id_token" \
-H "Content-Type:application/json" \
-d '{
  "transactions": [
    {
      "to_address": "GC4C4SSPDOKW7BA7446B5TM6NHGJ3NAZ4HZEUXRO3NEJKZYQEK5AORFX",
      "amount": "2000"
    },
    {
      "to_address": "GC4C4SSPDOKW7BA7446B5TM6NHGJ3NAZ4HZEUXRO3NEJKZYQEK5AORFX",
      "amount": "3"
    }
  ]
}'