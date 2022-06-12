import tensorflow as tf
import pandas as pd
import numpy as np
import random

tf.data.experimental.enable_debug_mode()

model = tf.keras.models.load_model('./dnn_model_keras')

# 10,000 inputs with 1 years exp and random salary between 20,000 and 30,000 
new_inputs_count = 10_000
new_inputs_labels = pd.Series([random.randint(20_000, 30_000)
                    for x in range(new_inputs_count)])
new_inputs_features = pd.DataFrame([{"YearsCode": 1, "YearsCodePro": 1} for x in range(new_inputs_count)])

def predict1YOE():
    return model.predict(np.array([1, 1]))[0][0]

print("Prediction before new inputs with low salaries")
print(predict1YOE())

model.fit(
    new_inputs_labels,
    new_inputs_features,
    validation_split=0.2,
    verbose=0, epochs=10)

print("Prediction after new inputs with low salaries")
print(predict1YOE())