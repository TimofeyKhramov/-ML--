import streamlit as st
import requests
import time
import datetime
import json
from show_screen import show_ml_tasks, show_task_input_screen, show_medical_prediction_input
from history import show_prediction_history, format_date, show_transaction_history

# Настройка страницы
st.set_page_config(
    page_title="Личный кабинет",
    layout="centered",
    initial_sidebar_state="collapsed"
)
def _max_width_(prcnt_width:int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f""" 
                <style> 
                .reportview-container .main .block-container{{{max_width_str}}}
                </style>    
                """, 
                unsafe_allow_html=True,
    )
API_URL = "http://localhost:8080/api/users"

# Инициализация состояния сессии
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "show_ml_tasks" not in st.session_state:
    st.session_state.show_ml_tasks = False
# Функция для входа
def login():
    st.subheader("\U0001F4B0 Вход в аккаунт")
    
    with st.form("login_form"):
        login = st.text_input("Логин (Email)")
        password = st.text_input("Пароль", type="password")
        
        if st.form_submit_button("Войти"):
            try:
                response = requests.post(
                    f"{API_URL}/signin",
                    json={"login": login, "password": password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.logged_in = True
                    print(data)
                    st.session_state.user_id = data.get("user_id")
                    st.session_state.user_login = login
                    st.rerun()
                else:
                    error = response.json().get("detail", "Ошибка входа")
                    st.error(f"❌ {error}")
                    
            except Exception as e:
                st.error(f"❌ Ошибка подключения: {e}")

# Функция для регистрации
def register():
    st.subheader("📝 Регистрация")
    
    with st.form("register_form"):
        login = st.text_input("Email")
        password = st.text_input("Пароль", type="password")
        confirm = st.text_input("Подтвердите пароль", type="password")
        
        if st.form_submit_button("Зарегистрироваться"):
            if password != confirm:
                st.error("❌ Пароли не совпадают")
            elif len(password) < 5:
                st.error("❌ Пароль должен быть минимум 5 символов")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/signup",
                        json={"login": login, "password": password}
                    )
                    
                    if response.status_code == 201:
                        st.success("✅ Регистрация успешна! Теперь войдите в аккаунт.")
                    else:
                        error = response.json().get("detail", "Ошибка регистрации")
                        st.error(f"❌ {error}")
                        
                except Exception as e:
                    st.error(f"❌ Ошибка подключения: {e}")

def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
            return "Доброе утро, "
    elif 12 <= hour < 18:
        return "Добрый день, "
    elif 18 <= hour < 23:
        return "Добрый вечер, "
    else:
        return "Доброй ночи, "
    
def profile():
    st.markdown("""
<style>
    /* Ограничиваем ширину основного контейнера */
    .main .block-container {
        max-width: 100px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Ограничиваем ширину колонок */
    .stHorizontalBlock {
        max-width: 600px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    /* Центрирование текста меток (названий полей) */
    .stNumberInput label {
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }
    /* Центрирование заголовков */
    h1 {
        text-align: center !important;
    }
    
    .stCaption {
        text-align: center !important;
    }
    
    
    /* Поля ввода на всю ширину своей колонки */
    .stNumberInput input {
        width: 80% !important;
    }
    
                /* Отключаем ограничения у block-container */
    .block-container {
        max-width: none !important;
    }
                
    .stNumberInput label {
        font-size: 18px !important;
        font-weight: 500 !important;
        text-align: center !important;
        width: 100% !important;
    }

    
    /* Увеличенный шрифт в полях ввода */
    .stNumberInput input {
        font-size: 20px !important;
        padding: 10px !important;
    }
    /* Глобально убираем все отступы у полей ввода */
    .stNumberInput {
        margin-top: -20px !important;
    }
    /* Центрирование кнопок */
    .stButton {
        display: flex;
        justify-content: center;
    }
    .stButton button {
        max-width: 700px;
    }
    </style>            
""", unsafe_allow_html=True)

    # Инициализация состояния для приветствия
    if "show_welcome" not in st.session_state:
        st.session_state.show_welcome = True
    if "welcome_start_time" not in st.session_state:
        st.session_state.welcome_start_time = None
    if st.session_state.get("show_ml_tasks", False):
        show_ml_tasks()
        return
    if "show_task_input" not in st.session_state:
        st.session_state.show_task_input = False
    if st.session_state.get("show_prediction_history", False):
        show_prediction_history()
        return
    if st.session_state.get("show_transaction_history", False):
        show_transaction_history()
        return
    
    # Если показываем ввод вопроса
    if st.session_state.get("show_task_input", False):
        show_task_input_screen()
        return
    
    # Отображение приветствия на 7 секунд (скрываем всё остальное)
    if st.session_state.show_welcome:
        if st.session_state.welcome_start_time is None:
            st.session_state.welcome_start_time = time.time()
        
        # Очищаем всё и показываем только приветствие
        st.empty()
        
        # Показываем большое приветствие на весь экран
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
            text-align: center;
        ">
            <div>
                <h1 style="font-size: 64px;">👋{get_greeting()}{st.session_state.user_login}!</h1>
                <p style="font-size: 24px; color: #888; margin-top: 20px;"></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Проверяем, прошло ли 7 секунд
        elapsed = time.time() - st.session_state.welcome_start_time
        if elapsed >= 1:
            st.session_state.show_welcome = False
            st.rerun()
        else:
            time.sleep(0.1)
            st.rerun()
    
    # Основной интерфейс (показывается после приветствия)
    st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <h1>🔮 Готовы к предсказаниям, {st.session_state.user_login}?</h1>
    </div>
    """,
    unsafe_allow_html=True
)
    # Загрузка данных профиля
    try:
        user_id = int(st.session_state.user_id)
        response = requests.get(f"{API_URL}/profile/{user_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            profile_data = response.json()
            print(profile_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💰 Баланс", f"{profile_data['balance']} ₽")
            with col2:
                current_date = datetime.datetime.now().strftime("%d-%m-%Y")
                st.metric("📅 Дата", current_date)
            
            st.divider()
            
            # Кнопки действий
            col1, col2= st.columns(2)
            with col1:
                if st.button("💸 Пополнить баланс", use_container_width=True):
                    st.session_state.show_balance_modal = True

            if st.session_state.get("show_balance_modal", False):
                with st.container():
                    st.markdown("### 💰 Пополнение баланса")
                    amount = st.number_input("Сумма", step=1, key="amount_modal")
              
                    col_ok, col_cancel = st.columns(2)
                    
                    with col_ok:
                        if st.button("✅ Подтвердить", key="confirm_modal"):
                            response = requests.post(
                                f"{API_URL}/add_balance",
                                params={"user_id": st.session_state.user_id, "amount": amount}
                            )
                            if response.status_code == 200:
                                st.success(f"✅ Пополнено на {amount} ₽")
                                time.sleep(3)
                                st.session_state.show_balance_modal = False
                                st.rerun()
                            else:
                                error_detail = response.json().get("detail", "Неизвестная ошибка")
                                st.error(f"❌ Ошибка пополнения: {error_detail}")
                                time.sleep(2)
                                st.rerun()
                    with col_cancel:
                        if st.button("❌ Отмена", key="cancel_modal"):
                            st.session_state.show_balance_modal = False
                            st.rerun()
                         
            with col2:
                if st.button("🤖 ML задачи", use_container_width=True):
                    st.session_state.show_ml_tasks = True
                    st.rerun()
                    
                    if st.button("🔙 Назад", key="back_from_ml"):
                        st.session_state.show_ml_tasks = False
                        st.rerun()
            col3, col4 = st.columns(2)            
    
            with col3:
                if st.button("История транзакций", use_container_width=True):
                    st.session_state.show_transaction_history = True
                    st.rerun()
            if st.session_state.get("show_transaction_history", False):
                show_transaction_history()
                return
           
            with col4:
                if st.button("История ML-предсказаний", use_container_width=True):
                    st.session_state.show_prediction_history = True
                    st.rerun()
            if st.session_state.get("show_prediction_history", False):
                show_prediction_history()
                return
            
        else:
            st.error("❌ Не удалось загрузить профиль")
            
    except Exception as e:
        st.error(f"❌ Ошибка: {e}")
    
    st.divider()
    
    # Кнопка выхода
    if st.button("🚪 Выйти из аккаунта", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_login = None
        st.session_state.show_welcome = True
        st.session_state.welcome_start_time = None
        st.session_state.show_ml_tasks = False
        st.session_state.show_balance_modal = False
        st.rerun()

# Главная логика
def main():
    if not st.session_state.logged_in:
        st.title("🏦 Event Planner")
        
        tab1, tab2 = st.tabs(["🔐 Вход", "📝 Регистрация"])
        
        with tab1:
            login()
        with tab2:
            register()
    else:
        profile()

if __name__ == "__main__":
    main()