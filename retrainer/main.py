import tensorflow as tf
import numpy as np
from lib.StoreClient import StoreClient
from lib.ApiClient import ApiClient

tf.data.experimental.enable_debug_mode()

store = StoreClient()
model = store.fetch_model()
response = ApiClient.get_untrained_inputs_encoded()['data']

untrained_inputs = np.array([[row['input_encoded'] for row in response]])[0]
salaries = np.array([row['salary'] for row in response])
uuids = [row['uuid'] for row in response]

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
    history = model.fit(
        untrained_inputs,
        salaries,
        validation_split=0.2,
        verbose=0, epochs=maxEpochs,
        callbacks=[callback])

    print(f"Early stopping ran {len(history.history['loss'])} epochs out of the max of {maxEpochs}")
    print("Prediction after new inputs")

    store.save_model(model)
    ApiClient.mark_input_trained(uuids)
except BaseException as err:
    print("Failed to fit new inputs to existing model")
    print(f"Unexpected {err}, {type(err)}")