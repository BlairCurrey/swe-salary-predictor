from google.cloud import storage
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from lib.Encodings import Encodings
from lib.models import ModelsStore, EncodingsStore
from lib.database import get_db

class StoreClient:
    def __init__(self):
        # must set GOOGLE_APPLICATION_CREDENTIALS env var to 
        # path of google cloud store json credentials
        load_dotenv()
        self.db = next(get_db())
        self.client = storage.Client()

    def fetch_encodings(self):
        latest_encodings = (self.db.query(EncodingsStore)
                            .order_by(EncodingsStore.created_at.desc())
                            .first())
        bucket = self.client.get_bucket(latest_encodings.bucket)
        blob_str = bucket.blob(latest_encodings.path).download_as_string()
        return Encodings(blob_str)

    def fetch_model(self):
        latest_model = (self.db.query(ModelsStore)
                        .order_by(ModelsStore.created_at.desc())
                        .first())
        print(f'Retrieved ref to latest model in db: {latest_model.path}')
        return load_model(f'gs://{latest_model.bucket}/{latest_model.path}')