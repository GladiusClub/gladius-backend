from openai import OpenAI
#import os
#from dotenv import load_dotenv
from flask import escape, jsonify

# Load the .env file
#load_dotenv()

def generate_image(request):
    
    try:
        # init OpenAI client
        client = OpenAI()

    except Exception as e:
        print('Cannot load OPENAI_API_KEY: ', str(e))
        return jsonify(error=str(e)), 500

    # Ensure the request is JSON
    request_json = request.get_json(silent=True)

    # Check if prompt is provided
    if request_json and 'prompt' in request_json:
        prompt = request_json['prompt']
    else:
        return jsonify(error="Please provide a prompt."), 400

    # Call OpenAI's image generation API
    try:
        response =  client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        )

        # Extract the image URL
        image_url = response.data[0].url
        print('image_url: ' , image_url)
        revised_prompt = response.data[0].revised_prompt
        print("revised_prompt: ", revised_prompt)

        return jsonify(url=image_url)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return jsonify(error=str(e)), 500