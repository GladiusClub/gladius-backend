ID_TOKEN=$(gcloud auth print-identity-token)
curl https://europe-west1-wallet-login-45c1c.cloudfunctions.net/StellarGladiusContracts \
  -H "Authorization: bearer ${ID_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
        "contract_func": "mint",
        "to_address": "GALT6V5AXC56AS6XY6XIKET25I3GRII2EIMSXFBVKGGSQT3AKQNLCETY",
        "amount": "555"
      }'