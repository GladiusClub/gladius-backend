gcloud functions deploy openai_image_generate  --runtime python310    --trigger-http      --source=./     --entry-point=generate_image  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY 