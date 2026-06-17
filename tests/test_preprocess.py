import pytest
import numpy as np
from PIL import Image
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import preprocess_image 

def test_preprocess_dimensions():
    """Тест перевіряє, чи функція повертає правильну розмірність (1, 28, 28, 1)"""
    # створюємо чорне зображення 100x100 з білим квадратом (щоб знайти контур)
    data = np.zeros((100, 100), dtype=np.uint8)
    data[30:70, 30:70] = 255
    img = Image.fromarray(data)
    
    processed = preprocess_image(img)
    
    # перевірка форми тензора
    assert processed.shape == (1, 28, 28, 1), f"Очікували (1, 28, 28, 1), отримали {processed.shape}"

def test_preprocess_normalization():
    """Тест перевіряє, чи дані нормалізовані в діапазон [0, 1]"""
    data = np.zeros((100, 100), dtype=np.uint8)
    data[30:70, 30:70] = 255
    img = Image.fromarray(data)
    
    processed = preprocess_image(img)
    
    # перевірка діапазону значень
    assert processed.max() <= 1.0, "Значення пікселів перевищують 1.0"
    assert processed.min() >= 0.0, "Значення пікселів менші за 0.0"
    assert processed.dtype == np.float32, "Тип даних має бути float32"

def test_preprocess_empty_image():
    """Тест на стійкість до порожнього зображення (без цифри)"""
    data = np.zeros((100, 100), dtype=np.uint8)
    img = Image.fromarray(data)
    
    processed = preprocess_image(img)
    assert processed.shape == (1, 28, 28, 1)