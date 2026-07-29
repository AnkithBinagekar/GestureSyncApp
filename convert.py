import tensorflow as tf

model = tf.keras.models.load_model('assets/expression_pointer_mobilenetv2.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('assets/expression_pointer.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model converted to TFLite")
