from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json

def main():
    advanced_collectible = AdvancedCollectible[-1]
    total_tokens = advanced_collectible.tokenCounter()

    # Iterate through the tokenIdToBreed mapping using the tokenCounter
    for token_id in range(total_tokens):
        breed = advanced_collectible.tokenIdToBreed(token_id)
        print(f"Token ID: {token_id}, Breed: {breed}")

    pass
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"

        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists")
        else:
            print(f"Creating metadata {metadata_file_name}")
            collectible_metadata['name'] = breed
            collectible_metadata['description'] = f"It's a {breed} or something"
            image_file_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_file_path)
            collectible_metadata['image'] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)

def upload_to_ipfs(filepath):
    with Path(filepath).open('rb') as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        responce = requests.post(ipfs_url + end_point, files={"file":image_binary})
        ipfs_hash = responce.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"ipfs://{ipfs_hash}?filename={filename}"
        print(image_uri)
    return image_uri
