curl -X POST "https://europe-west1-wallet-login-45c1c.cloudfunctions.net/SignupGladiusClubCourse" \
-H "Content-Type: application/json" \
-d '{
  "ClubOwnerUID": "MmNNhkPnhXfluJ0HMpwCFFImpLt2",
  "ClubUID" : "4",
  "CourseName" : "My awesome course",
  "CoursePrice" : 200,
  "Courseincentive" : 15
}'
