import time
import requests
from google.cloud import storage
from dotenv import load_dotenv
from tensorflow.keras.models import load_model, save_model
from lib.ApiClient import ApiClient

class StoreClient:
    def __init__(self):
        # must set GOOGLE_APPLICATION_CREDENTIALS env var to 
        # path of google cloud store json credentials
        load_dotenv()
        self.client = storage.Client()
        self.latest_model_store = None

    def fetch_model(self):
        self.latest_model_store = self.fetch_latest_model_store()
        
        return load_model(f"gs://{self.latest_model_store['bucket']}/{self.latest_model_store['path']}")
    
    def save_model(self, model):
        if self.latest_model_store is None:
            self.latest_model_store = self.fetch_latest_model_store()
        
        filename = f'model_{int(time.time())}'
        filepath = f"gs://{self.latest_model_store['bucket']}/{filename}"
        
        save_model(model, filepath)
        ApiClient.add_model_store({"bucket": self.latest_model_store['bucket'], 
                                   "path": filename})
    
    def fetch_latest_model_store(self):
        return (requests.get(f'http://localhost:8000/api/latest-model-store')
                        .json()['latest_model_store'])