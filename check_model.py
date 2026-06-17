import os
import tensorflow as tf

def validate_model():
    model_path = 'model/mnist_model.h5'
    print(f"Checking model at {model_path}...")
    
    if not os.path.exists(model_path):
        print("Error: Model file not found!")
        exit(1)
        
    try:
        model = tf.keras.models.load_model(model_path)
        print("Success: Model loaded into RAM.")
        # перевірка вхідного шару (Розділ 15 звіту)
        expected_input = (None, 28, 28, 1)

        if model.input_shape != expected_input:
            print(f"Error: Wrong input shape {model.input_shape}")
            exit(1)
    except Exception as e:
        print(f"Error: Model is corrupted. {e}")
        exit(1)

if __name__ == "__main__":
    validate_model()