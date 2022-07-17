import requests
from dotenv import load_dotenv
import os

class ApiClient:
    load_dotenv()
    url = os.environ.get("API_URL")
    if url is None: raise ValueError('API_URL env var not set')

    @staticmethod
    def add_model_store(model_store):
        return requests.post(f'{ApiClient.url}/model-store', 
                             json=model_store)

    @staticmethod
    def get_untrained_inputs_encoded():
        return requests.get(
            f'{ApiClient.url}/untrained-inputs-encoded').json()

    @staticmethod
    def mark_input_trained(uuids):
        return requests.put(
            f'{ApiClient.url}/mark-input-trained', json=uuids)

    @staticmethod
    def fetch_latest_model_store():
        return (requests.get(f'{ApiClient.url}/latest-model-store')
                        .json()['latest_model_store'])