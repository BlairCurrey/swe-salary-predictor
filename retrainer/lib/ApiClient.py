import requests

class ApiClient:

    @staticmethod
    def add_model_store(model_store):
        return requests.post(f'http://localhost:8000/api/model-store', 
                             json=model_store)

    @staticmethod
    def get_untrained_inputs_encoded():
        return requests.get(
            f'http://localhost:8000/api/untrained-inputs-encoded').json()

    @staticmethod
    def mark_input_trained(uuids):
        return requests.put(
            f'http://localhost:8000/api/mark-input-trained', json=uuids)