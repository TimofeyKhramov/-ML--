import streamlit as st
import requests
import time

def show_ml_tasks():
    ML_API_URL  = "http://localhost:8080/"
    """Отображение только ML задач (всё остальное скрыто)"""
    st.title("✨ Доступные ML задачи")
    
    try:
        response = requests.get(f"{ML_API_URL}/get_all_mltasks")
        
        if response.status_code == 200:
            tasks = response.json()
            
            if tasks:
                for task in tasks:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"**{task['name']}**")
                            st.caption(task.get('description', 'Нет описания'))
                        with col2:
                            st.metric("Стоимость", f"{task['cost']} ₽")
                        with col3:
                            if st.button("Выбрать", key=f"select_{task['id']}"):
                                st.session_state.selected_task = task
                                st.session_state.show_task_execution = True
                                st.session_state.show_task_input = True
                                st.session_state.show_ml_tasks = False
                                st.rerun()
                    st.divider()
            else:
                st.info("Список ML задач пуст")
        else:
            st.error("❌ Не удалось загрузить список ML задач")
            
    except Exception as e:
        st.error(f"❌ Ошибка: {e}")
    
    if st.button("🔙 Назад", use_container_width=True):
        st.session_state.show_ml_tasks = False
        st.rerun()

def show_medical_prediction_input():
    
    st.markdown("""
<style>
    /* Ограничиваем ширину основного контейнера */
    .main .block-container {
        max-width: 1000px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Ограничиваем ширину колонок */
    .stHorizontalBlock {
        max-width: 2000px !important;
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
        width: 100% !important;
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

    st.title("🏥 Медицинские предсказания")
    st.write("")
    st.write("")
    st.write("")
    

    col1, col2, col3, col4, col5, col6 = st.columns([5,5,5,5,5,5])
    
    with col1:
        st.markdown(
            '<p style="font-size: 17px; margin-bottom: 0; text-align: center;"> Полный гемоглобин</p>',
            unsafe_allow_html=True
        )
        hb = st.number_input('', key="hemoglobin", min_value=-10.0, max_value=50.0, value=0.0, label_visibility='hidden')

    with col2:
        st.markdown(
            '<p style="font-size: 17px; margin-bottom: 0; text-align: center;"> Оксигенация</p>',
            unsafe_allow_html=True
        )
        oxi = st.number_input('', key="oxygenation", min_value=-10.0, max_value=50.0, value=0.0, label_visibility='hidden')

    with col3:
        st.markdown(
            '<p style="font-size: 17px; margin-bottom: 0; text-align: center;"> Рассеяние</p>',
            unsafe_allow_html=True
        )
        scat = st.number_input('', key="scattering", min_value=-10.0, max_value=50.0, value=0.0, label_visibility='hidden')

    with col4:
        st.markdown(
            '<p style="font-size: 17px; margin-bottom: 0; text-align: center;"> Интенсивность 1</p>',
            unsafe_allow_html=True
        )
        i1 = st.number_input('', key="i1", min_value=0.0, max_value=1.0, value=0.0, step=0.01, format="%.2f", label_visibility='hidden')

    with col5:
        st.markdown(
            '<p style="font-size: 17px; margin-bottom: 0; text-align: center;"> Интенсивность 2</p>',
            unsafe_allow_html=True
        )
        i2 = st.number_input('', key="i2", min_value=0.0, max_value=1.0, value=0.0, step=0.01, format="%.2f", label_visibility='hidden')

    with col6:
        st.markdown(
            '<p style="font-size: 17px; margin-bottom: 0; text-align: center;"> Длина волны</p>',
            unsafe_allow_html=True
        )
        lam = st.number_input('', key="lambda", min_value=0.0, max_value=600.0, value=0.0, step=5.0, label_visibility='hidden')
    for i in range(10):
        st.write('')

    st.markdown(
    '<hr style="border: 0.5px solid #8888; width: 700px; margin: 0 auto;">',
    unsafe_allow_html=True
)
    if st.button("🚀 ПРЕДСКАЗАТЬ", use_container_width=True, type="primary"):
                medical_data = {
                    "hemoglobin": hb,
                    "oxygenation": oxi,
                    "scattering": scat,
                    "I1": i1,
                    "I2": i2,
                    "lambda": lam
                }
                cont_st = st.empty()
                # Здесь будет отправка данных в API
                placeholder = st.empty()
                waiting_msg = st.info("⏳ Данные отправлены на предсказание...")
                # st.json(medical_data)
                response = requests.post(
                    f"http://localhost:8080/send_task",
                    json={
                        "user_id": st.session_state.user_id,
                        "mltask_id": st.session_state.selected_task['id'],
                        "message": 'Message',
                        "features": medical_data}
                        
                )
                result = None
                print(response.status_code)
                if response.status_code == 500:
                    error_data = response.json()
                    error_msg = error_data.get("detail", "Недостаточно! средств для выполнения операции")
                    st.error(f"❌ {error_msg}")
                    
            
                else:
                    task_data = response.json()
                    task_id = task_data.get("task_id")
                    with st.spinner("⏳ Обработка предсказания..."):
                        result = None
                        for i in range(30):  # ждём до 30 секунд
                            time.sleep(1)
                            result_response = requests.get(f"http://localhost:8080/task_result/{task_id}")
                            if result_response.status_code == 200:
                                result_data = result_response.json()
                                if result_data.get("result"):
                                    result = result_data.get("result")
                                    break
                  
                    placeholder.success("✅ Результат получен!")
                    st.markdown(
            f'<p style="font-size: 30px; margin-bottom: 0; text-align: center;"> Результат анализа: {result}</p>',
            unsafe_allow_html=True
        )
                    waiting_msg.empty()
                
    if st.button("🔙 Назад к задачам", use_container_width=True):
        st.session_state.show_task_input = False
        st.session_state.show_ml_tasks = True
        st.rerun()


def show_task_input_screen():
    task_name = st.session_state.selected_task['name']
    
    # Проверяем, какая задача выбрана
    if "медицинск" in task_name.lower() or "medical" in task_name.lower():
        show_medical_prediction_input()
        return
    
    """Отображение поля для ввода вопроса"""
    st.title(f"✨ {st.session_state.selected_task['name']}")
    # st.caption(f"Стоимость: {st.session_state.selected_task['cost']} ₽")
    # st.caption(st.session_state.selected_task.get('description', ''))
    
    st.divider()
    
    # Поле для ввода вопроса
    question = st.text_area("💬 Введите, пожалуйста, Ваш вопрос:", height=150)
    if st.button("🚀 ОТПРАВИТЬ", use_container_width=True, type="primary"):
               
                cont_st = st.empty()
                # Здесь будет отправка данных в API
                placeholder = st.empty()
                waiting_msg = st.info("⏳ Данные отправлены на предсказание...")
                # st.json(medical_data)
                response = requests.post(
                    f"http://localhost:8080/send_task",
                    json={
                        "user_id": st.session_state.user_id,
                        "mltask_id": st.session_state.selected_task['id'],
                        "message": 'Message',
                        "question": question}
                )
                result = None
                print(response.status_code)
                if response.status_code == 500:
                    error_data = response.json()
                    error_msg = error_data.get("detail", "Недостаточно! средств для выполнения операции")
                    st.error(f"❌ {error_msg}")
                    
            
                else:
                    task_data = response.json()
                    task_id = task_data.get("task_id")
                    with st.spinner("⏳ Думаю над ответом..."):
                        result = None
                        for i in range(300):  # ждём до 30 секунд
                            time.sleep(1)
                            result_response = requests.get(f"http://localhost:8080/task_result/{task_id}")
                            if result_response.status_code == 200:
                                result_data = result_response.json()
                                print(result_data)
                                if result_data.get("result"):
                                    result = result_data.get("result")
                                    break
                  
                    placeholder.success("✅ Результат получен!")
                    st.markdown(
            f'<p style="font-size: 30px; margin-bottom: 0; text-align: center;"> {result}</p>',
            unsafe_allow_html=True
        )
                    st.balloons()
                    waiting_msg.empty()
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Назад к задачам", use_container_width=True):
            st.session_state.show_task_input = False
            st.session_state.show_ml_tasks = True
            st.rerun()