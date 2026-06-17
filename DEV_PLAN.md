# План розробки «Digit Recognition System»

## Статус етапів розробки

| Пріоритет | Завдання | Статус |
| :--- | :--- | :--- |
| 🔴 High | Розробка архітектури CNN та навчання моделі | 🟢 Done |
| 🔴 High | Завантаження ваг та перевірка інференсу | 🟢 Done |
| 🔴 High | Інтерактивний веб-інтерфейс (Streamlit) | 🟢 Done |
| 🟡 Medium | Попередня обробка OpenCV (центрування, ресайзинг) | 🟢 Done |
| 🟡 Medium | Контейнеризація застосунку (Dockerfile) | 🟢 Done |
| 🟡 Medium | Налаштування CI/CD (GitHub Actions) | 🟢 Done |
| 🟢 Done | Додавання лінтерів (flake8, black) | 🟢 Done |
| 🟢 Done | Візуалізація ймовірностей (Explainable AI) | 🟢 Done |

## Розподіл ресурсів (Фази проєкту)
1. **ML Core & Data**: Навчання CNN, аугментація — 35 год.
2. **Application & UI**: Streamlit, логіка малювання — 30 год.
3. **Infra & CI/CD**: Docker, GitHub Actions, Dependabot — 30 год.
4. **Security & QA**: Валідація, тестування, рев'ю — 40 год.

---