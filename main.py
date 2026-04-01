from datetime import datetime

class User:
    def __init__(self, id: int, username: str, login: str, password: str, balance: int):
        self.id = id
        self.username = username
        self.login = login
        self.password = password
        self.balance = balance

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError(f"ID должен быть целым числом")
        if value < 0:
            raise ValueError("ID не должен быть отрицательным")
        self._id = value

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Имя пользователя должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Необходимо заполнить имя пользователя")
        if len(value) < 5:
            raise ValueError("Имя пользователя должно содержать не менее 5 символов")
        if len(value) > 30:
            raise ValueError("Имя пользователя должно содержать не более 30 символов")
        self._username = value

    @property
    def login(self):
        return self._login
    @login.setter
    def login(self, value):
        if not isinstance(value, str):
            raise TypeError(f"login must be str, got {type(value).__name__}")
        value = value.strip()
        if not value:
            raise ValueError("login cannot be empty")
        if len(value) < 3:
            raise ValueError("login must be at least 3 characters")
        if len(value) > 50:
            raise ValueError("login cannot exceed 50 characters")
        if ' ' in value:
            raise ValueError("login cannot contain spaces")
        self._login = value

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError(f"password must be str, got {type(value).__name__}")
        if len(value) < 6:
            raise ValueError("password must be at least 6 characters")
        if len(value) > 128:
            raise ValueError("password cannot exceed 128 characters")
        self._password = value

    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, value):
        if not isinstance(value, int):
            raise TypeError(f"balance must be int, got {type(value).__name__}")
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

    def can_afford_add(self, amount):
        if not isinstance(amount, int):
            raise TypeError(f"amount must be int, got {type(amount).__name__}")
        if amount < 0:
            raise ValueError("amount cannot be negative")
        return self._balance 
    
    def can_afford_debit(self, amount):
        if not isinstance(amount, int):
            raise TypeError(f"amount must be int, got {type(amount).__name__}")
        if amount < 0:
            raise ValueError("amount cannot be negative")
        return self._balance >= amount

    


class MLModel:
    def __init__(self, id: int, price: int):
        self._id = id
        self._price = price 
   
        """Модель позволяет создавать финансовую отчётность на основе кассовых чеков.
        На вход модель принимает фото кассового чека. Поддерживаемые форматы: jpg, jpeg, png. 
        Далее осуществляется перевод изображения в текст (image-to-text).
        На выходе модель возвращает json-файл  со следующими ключами: 
        1. Дата
        2. Наименование расхода
        3. Сумма
        4. Поставщик
        5. ИНН
        Далее планируется перевод в csv-файл и отправка конечного ответа пользователю
        Возможные модели: FRED-T5-large-ods-ner-2023 (вес около 3.3Гб), 
        LightOnOCR-1B-1025 (вес около 3Гб, можно применить квантизацию)
        """

class MLTask:
    def __init(self, path: str, user: User, mlmodel: MLModel):
        self._path = path # Путь к исходному чеку
        self._user = user # Ссылка на пользователя
        self._mlmodel = mlmodel # Ссылка на ml-модель
    
    def status():
        """
        Функция возвращает следующие статусы:
            Выполнено, если файл сгенерирован и отправлен пользователю.
            В процессе обработки, если файл загружен пользователем и находится в процессе обработки
            Файл готов к обработке, если файл загружен пользователем
            Загрузите файл, если не указан путь (path) к файлу
        """
        pass

    def process():
        """
        Функция осуществляет проверку статуса задачи и запускает обработку, если статус Файл готов к обработке
        """
        pass

class Transaction:
    def __init__(self, user: User, mltask: MLTask):
        self._user = user # Ссылка на пользователя
        self._mltask = mltask # Ссылка на ml-задачу
        self.created_at: datetime = datetime.now()
    
    def apply(self):
        raise NotImplementedError('Функция должна быть переопределена')

class DebitTransaction(Transaction):
    def __init__(self,  user, mltask):
        super().__init__( user, mltask)

    def apply(self, amount):
        if  not self._user.can_afford_debit(amount):
            print('Недостаточно средств')
            return False
        self._user._balance -= amount
        return True
    

class AddTransaction(Transaction):
    def __init__(self, user: User, mltask: MLTask):
        super().__init__(user, mltask)
    
    def apply(self, amount):
        if not self._user.can_afford_add(amount):
            return False
        self._user._balance += amount
        return True
    
user1 = User(1, 'tkhth', 'khtjtt', '12mymy3', 8)
trans1 = DebitTransaction(user1, 'rec')
trans1.apply(1)
print(trans1.created_at)



