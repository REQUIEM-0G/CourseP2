import os
import logging
import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import cv2
from dotenv import load_dotenv
from utils import preprocess_image  # імпортуємо логіку

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "model/mnist_model.h5")

# завантаження моделі
@st.cache_resource
def load_my_model():
    if os.path.exists(MODEL_PATH):
        return tf.keras.models.load_model(MODEL_PATH)
    return None

def main():
    st.set_page_config(page_title="MNIST System")
    st.title("Digit Recognition System")

    model = load_my_model()
    if model is None:
        st.error(f"Модель не знайдено за шляхом: {MODEL_PATH}")
        return

if __name__ == "__main__":
    main()