import streamlit as st
import requests

# Настройка страницы
st.set_page_config(
    page_title="Регистрация",
    layout="centered"
)

# API endpoint (ваш FastAPI эндпоинт)
API_URL = "http://localhost:8080/api/users/signup"

st.title("Регистрация")

# Форма регистрации
with st.form("registration_form"):
    login = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    
    submitted = st.form_submit_button("Зарегистрироваться")
    
    if submitted:
        try:
            payload = {
            "login": login,
            "password": password
        }

        # Отправляем POST-запрос с JSON
            response = requests.post(
               API_URL,
            json={"login": login, "password": password})
            
            if response.status_code == 201:
                st.success(" Регистрация успешна!")
            else:
                st.error(f" Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}")
                
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")