from fastapi.testclient import TestClient
# from models.event import Event
from sqlmodel import Session 

def test_home_request(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_signup(client: TestClient):
    data = {
  "id": 1,
  "login": "test3@mail.ru",
  "password": "123456",
  "balance": 0,
  "created_at": "2026-05-05T19:46:40.993Z"
}
    
    response = client.post("/api/users/signup/", json=data)

    assert response.status_code == 201
    assert response.json() == {"message": "User successfully registered"}

def test_signin(client: TestClient):
    test_signup(client)
    data = {
  "id": 1,
  "login": "test3@mail.ru",
  "password": "123456",
  "balance": 0,
  "created_at": "2026-05-05T19:46:40.993Z"
}
    
    response = client.post("/api/users/signin/", json=data)

    assert response.status_code == 200
    assert response.json() == {"message": "User signed in successfully", "user_id": 1}

# Получить баланс пользователя
def test_get_user_balance(client: TestClient):
    test_signup(client)
    data = {
  "id": 1,
  "login": "test3@mail.ru",
  "password": "123456",
  "balance": 0,
  "created_at": "2026-05-05T19:46:40.993Z"
}
    
    response = client.get("/api/users/get_user_balance/?user_id=1")

    assert response.status_code == 200
    assert response.json() == {"Баланс пользователя с ID=1": 0}

# Пополнение баланса
def test_add_balance(client: TestClient):
    test_signup(client)
    
    response = client.post("/api/users/add_balance/?user_id=1&amount=100")

    assert response.status_code == 200
    response_data = response.json()
    # assert response_data["user_id"] == 1
    # assert response_data["added_amount"] == 100
    # assert response_data["new_balance"] == 100
    initial_response = client.get("/api/users/get_user_balance/?user_id=1")
    assert initial_response.status_code == 200
    initial_balance = initial_response.json().get("balance", 100)
    assert initial_balance == 100

#История_Транзакции
def test_get_user_all_transactions_success(client: TestClient, session: Session):
    """
    Тест успешного получения всех транзакций пользователя
    """

    test_signup(client)
  
    response = client.get(f"/api/users/get_user_all_transactions/?user_id={1}")
    assert response.status_code == 200
    transactions = response.json()

# История ML-задач
def test_get_user_history_success(client: TestClient, session: Session):
    """
    Тест успешного получения всех транзакций пользователя
    """

    test_signup(client)
  
    response = client.get(f"/history/?user_id={1}")
    assert response.status_code == 200
    
# Отправка ML-задачи
# def test_send_task_chat_with_llm(client: TestClient, session: Session):
#     """
#     Тест отправки задачи для чата с LLM
#     """
#     # 1. Создаём пользователя
#     user_data = {
#         "login": "llm_test@mail.ru",
#         "password": "123456"
#     }
#     signup_response = client.post("/api/users/signup/", json=user_data)
#     assert signup_response.status_code == 201
    
#     # 2. Получаем ID пользователя из БД
#     from src.user import User
#     user = session.query(User).filter(User.login == "llm_test@mail.ru").first()
#     user_id = user.id
    
#     # 3. Пополняем баланс (нужно для оплаты)
#     add_balance_response = client.post(f"/api/users/add_balance/?user_id={user_id}&amount=1000")
#     assert add_balance_response.status_code == 200
    
  
#     from src.mltask import MLTaskType
#     mltask = MLTaskType(id=1, name='Чат с LLM', cost=30, description='Пользователь может задавать любые вопросы LLM модели Qwen2.5:1.5b')
#     session.add(mltask)
#     session.commit()
    
#     # 5. Отправляем задачу
#     task_data = {
#         "mltask_id": 1,
#         "user_id": user_id,
#         "question": "Как дела?",
#         "features": None
#     }
    
#     response = client.post("/api/mltask/send_task/", json=task_data)
    
#     # 6. Проверяем ответ
#     assert response.status_code == 200
#     response_data = response.json()
#     assert "message" in response_data
#     assert response_data["message"] == "Task sent successfully!"
#     assert "task_id" in response_data
    
#     # 7. Проверяем, что баланс списался
#     session.refresh(user)
#     assert user.balance == 900  # 1000 - 100
    
    # 8. Проверяем, что задача создалась в истории
    # from src.ml_history import MLHistory
    # history = session.query(MLHistory).filter(MLHistory.user_id == user_id).first()
    # assert history is not None
    # assert history.task_id == mltask.id



