import tensorflow as tf
import numpy as np
from lib.StoreClient import StoreClient
from lib.ApiClient import ApiClient
from dotenv import load_dotenv

load_dotenv()
tf.data.experimental.enable_debug_mode()

# 'retrainer' function name expected by gcloud function.
# 'data' and 'context' expected by gcloud function if triggered by pubsub
def retrainer(data, context):
    store = StoreClient()
    model = store.fetch_model()
    response = ApiClient.get_untrained_inputs_encoded()['data']

    untrained_inputs = np.array([[row['input_encoded'] for row in response]])[0]
    salaries = np.array([row['salary'] for row in response])
    uuids = [row['uuid'] for row in response]

    count = untrained_inputs.shape[0]
    print(f'retrieved {count} untrained inputs')
    min_inputs = 2
    
    if count < min_inputs:
        print(f'Need at least ${min_inputs} new inputs to retrain, exiting')
        return

    print('y shape: ', salaries.shape) # should be (n,)
    print('X shape: ', untrained_inputs.shape) # should be (n,115)

    callback = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        min_delta=0,
        patience=0,
        verbose=0,
        mode="auto",
        baseline=None,
        restore_best_weights=False,
    )
    maxEpochs = 10

    try:
        print("Starting training on untrained inputs")
        
        history = model.fit(
            untrained_inputs,
            salaries,
            validation_split=0.2,
            verbose=0, epochs=maxEpochs,
            callbacks=[callback])

        print(f"Early stopping ran {len(history.history['loss'])} epochs out of the max of {maxEpochs}")

        store.save_model(model)
        print('model saved')
        ApiClient.mark_input_trained(uuids)
        print('inputs marked as trained')
        ApiClient.trigger_refetch_latest_model()
        
    except BaseException as err:
        print("Failed to fit new inputs to existing model")
        print(f"Unexpected {err}, {type(err)}")