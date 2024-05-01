curl -X POST https://europe-west1-wallet-login-45c1c.cloudfunctions.net/mintGladiusNFT \
-H "Authorization: Bearer $firebase_id_token" \
-H "Content-Type:application/json" \
-d '{
  "transactions": [
    {
      "to_address": "GAHY73P3VMI7GUJAD377JWXCZ6KKUOLJBAOTK5VJ4RKYYP23N75DR7AN",
      "img_uri" : "https://gateway.pinata.cloud/ipfs/QmPyaNC6gLuc21Jn5S3BGV26voBdC3QxbwHRETR3yARyDp"
    }
  ]
}'