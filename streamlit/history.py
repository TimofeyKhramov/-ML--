import requests
import datetime
import streamlit as st


def format_date(date_str):
    dt = datetime.datetime.fromisoformat(date_str)
    formatted_date = dt.strftime("%d.%m.%Y %H:%M:%S")  
    return formatted_date

def show_prediction_history():
    """Отобразить историю предсказаний в виде таблицы"""
    st.title("📜 История ML-предсказаний")
    
    try:
        response = requests.get(
            "http://localhost:8080/history/",
            params={"user_id": st.session_state.user_id}
        )
        
        if response.status_code == 200:
            history = response.json()
            
            if not history:
                st.info("История предсказаний пуста")
            else:
                import pandas as pd
                
                # Создаём DataFrame
                
                df = pd.DataFrame([
                    {
                        "Дата и время": format_date(item['created_at'][:19]),
                        "Результат": item['result'],
                        "ID": item['id'],
                        "Тип задачи": item['type_of_mltask']
                    }
                    for item in history
                ])
                
                st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Ошибка: {e}")

    if st.button("🔙 Назад", use_container_width=True):
        st.session_state.show_prediction_history = False
        st.rerun()



def show_transaction_history():
    """Отобразить историю предсказаний в виде таблицы"""
    st.title("История транзакций")
    print(1)
    
    try:
        response = requests.get(
            "http://localhost:8080/api/users/get_user_all_transactions",
            params={"user_id": st.session_state.user_id}
        )
        
        if response.status_code == 200:
            history = response.json()
            print('HIS', history)
            
            if not history:
                st.info("История предсказаний пуста")
            else:
                import pandas as pd
                
                # Создаём DataFrame
                
                df = pd.DataFrame([
                    {
                        "Дата и время": format_date(item['created_at'][:19]),
                        "Тип": item['type_of'],
                        "Сумма": item['amount'],
                    }
                    for item in history
                ])
                
                unique_types = df['Тип'].unique().tolist()
                
                # Создаём мультивыбор для фильтрации
                selected_types = st.multiselect(
                    "Фильтр по типу транзакции:",
                    options=unique_types,
                    default=unique_types,  # по умолчанию показываем все
                    placeholder="Выберите типы транзакций"
                )
                
                # Применяем фильтр
                if selected_types:
                    filtered_df = df[df['Тип'].isin(selected_types)]
                else:
                    filtered_df = df
                
                # Отображаем отфильтрованную таблицу
                st.dataframe(
                    filtered_df, 
                    use_container_width=True, 
                    hide_index=True
                )
                
                # Дополнительно: показываем статистику по фильтру
                st.caption(f"Показано {len(filtered_df)} из {len(df)} транзакций")
    except Exception as e:
        st.error(f"Ошибка: {e}")
    
    if st.button("🔙 Назад", use_container_width=True):
        st.session_state.show_transaction_history = False
        st.rerun()