import streamlit as st
import requests
import time

# Настройка страницы
st.set_page_config(
    page_title="Личный кабинет",
    layout="centered",
    initial_sidebar_state="collapsed"
)

API_URL = "http://localhost:8080/api/users"
ML_API_URL = "http://localhost:8080/"
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

# Личный кабинет
def profile():

    st.title(f"👋 Добро пожаловать, {st.session_state.user_login}!")
    
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
                st.metric("📅 Дата регистрации", profile_data['created_at'][:10])
            
            st.divider()
            
            # Кнопки действий
            col1, col2, col3 = st.columns(3)
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
                    st.session_state.show_ml_tasks = st.session_state.show_ml_tasks
            if st.session_state.show_ml_tasks:
                with st.container():
                    st.markdown("### 🤖 Доступные ML задачи")
                    
                    try:
                        response = requests.get(f"{ML_API_URL}/get_all_mltasks")
                        
                        if response.status_code == 200:
                            tasks = response.json()
                            
                            if tasks:
                                for task in tasks:
                                    st.markdown(f"**{task['name']}** - {task['cost']} ₽")
                                    st.caption(f"{task['description']}")
                                    st.divider()
                            else:
                                st.info("Список ML задач пуст")
                        else:
                            st.error("❌ Не удалось загрузить список ML задач")
                            
                    except Exception as e:
                        st.error(f"❌ Ошибка: {e}")
                    
                    if st.button("🔙 Назад"):
                        st.session_state.show_ml_tasks = False
                        st.rerun()
            with col3:
                if st.button("📜 История", use_container_width=True):
                    st.info("Функция в разработке")
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