import os
import logging
import random
import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import cv2
from dotenv import load_dotenv

# імпорт логіки обробки
from utils import preprocess_image

# завантаження конфігурацій з .env
load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "model/mnist_model.h5")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# налаштування логування
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# фіксація seed
np.random.seed(42)
tf.random.set_seed(42)
random.seed(42)

# завантаження моделі з кешуванням
@st.cache_resource
def load_my_model():
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Модель не знайдено за шляхом: {MODEL_PATH}")
        return None
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        logger.info("Модель завантажена успішно")
        return model
    except Exception as e:
        logger.error(f"Помилка завантаження моделі: {e}")
        return None

def main():
    st.set_page_config(page_title="MNIST Digit System", layout="centered")
    st.title("Digit Recognition System")
    
    model = load_my_model()
    if model is None:
        st.error(f"Помилка: не вдалося знайти файл моделі в `{MODEL_PATH}`")
        return

    # стан сесії
    if 'prediction_data' not in st.session_state:
        st.session_state.prediction_data = None

    # UI вводу
    option = st.radio("Оберіть метод:", ("Малювання на панелі", "Завантаження фото"))

    if option == "Завантаження фото":
        file = st.file_uploader("Оберіть файл (цифра має бути чіткою)", type=["jpg", "png", "jpeg"])
        if file:
            img = Image.open(file)
            st.image(img, width=150, caption="Ваш файл")
            if st.button("Розпізнати фото"):
                processed = preprocess_image(img)
                st.session_state.prediction_data = model.predict(processed)[0]

    else:
        st.write("Намалюйте цифру в квадраті:")
        canvas_result = st_canvas(
            stroke_width=18, stroke_color="#FFFFFF", background_color="#000000",
            height=280, width=280, drawing_mode="freedraw", key="canvas"
        )
        if canvas_result.image_data is not None:
            if st.button("Розпізнати малюнок"):
                # конвертуємо RGBA в Gray
                img_raw = cv2.cvtColor(canvas_result.image_data.astype('uint8'), cv2.COLOR_RGBA2GRAY)
                if np.max(img_raw) > 0:
                    processed = preprocess_image(img_raw)
                    logger.info(f"Max pixel value in input: {np.max(processed)}")
                    st.session_state.prediction_data = model.predict(processed)[0]
                else:
                    st.warning("Канвас порожній!")

    # результати прогнозу
    if st.session_state.prediction_data is not None:
        probs = st.session_state.prediction_data
        label = np.argmax(probs)
        conf = np.max(probs)
        
        st.write("---")
        st.header(f"Прогноз: {label}")
        
        # візуалізація впевненості
        if conf < 0.7:
            st.warning(f"Впевненість низька: {conf:.2%}")
            logger.warning(f"Low confidence: {label} ({conf:.2f})")
        else:
            st.success(f"Впевненість: {conf:.2%}")
            logger.info(f"Prediction success: {label} ({conf:.2f})")

        # гістограма ймовірностей
        st.subheader("Розподіл ймовірностей по класах:")
        chart_df = pd.DataFrame(probs, index=[str(i) for i in range(10)], columns=["Ймовірність"])
        st.bar_chart(chart_df)

        if st.button("Очистити результат"):
            st.session_state.prediction_data = None
            st.rerun()

if __name__ == "__main__":
    main()