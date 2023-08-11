curl -X POST \
https://us-central1-wallet-login-45c1c.cloudfunctions.net/mumbai_token_transfer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $firebase_id_token" \
  -d '{
    "transactions": [
        {
            "to_address": "0x67c851F6805041ba34830F4479c4688e908FC26f",
            "amount": "0.01"
        },
        {
            "to_address": "0xFA8b27A0d9C5Bf7490ea03eDAB652c3a18cAc19b",
            "amount": "0.02"
        },
        {
            "to_address": "0x4093a8F669e227f5267FE4946F948eE981957BA2",
            "amount": "0.03"
        }
    ]
}'
