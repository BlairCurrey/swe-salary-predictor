from google.cloud import storage
from dotenv import load_dotenv
import pickle

class Store:
    def __init__(self):
        # must set GOOGLE_APPLICATION_CREDENTIALS env var to 
        # path of google cloud store json credentials
        load_dotenv()
        self.client = storage.Client()
        self.bucket = self.client.get_bucket('swe-salary-predictor-store')

    def get_blob_str(blob_path):
        blob = self.bucket.blob(blob_path)
        return blob.download_as_string()