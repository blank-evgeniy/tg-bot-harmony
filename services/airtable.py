import logging
from config import AIRTABLE_TOKEN, BASE_ID
from pyairtable import Api

class AirtableManager:
    def __init__(self):
        self.api = Api(AIRTABLE_TOKEN)
        self.base_id = BASE_ID

        # Таблицы из БД
        self.clients_table = self.api.table(self.base_id, "Клиенты")
        self.categories_table = self.api.table(self.base_id, "Категории")
        self.procedures_table = self.api.table(self.base_id, "Процедуры")
        self.masters_table = self.api.table(self.base_id, "Мастера")
        self.slots_table = self.api.table(self.base_id, "Слоты")
    
    async def check_user_exists(self, telegram_id: int):
        """Проверяет, существует ли пользователь в базе данных"""
        formula = f"{{TelegramID}} = '{telegram_id}'"
        record = self.clients_table.first(formula=formula)
        
        return record is not None
    
    async def get_client_id(self, telegram_id: int):
        """Получает ID клиента по его Telegram ID"""
        formula = f"{{TelegramID}} = '{telegram_id}'"
        record = self.clients_table.first(formula=formula)
        return record["id"]

    async def create_client(self, telegram_id: int, name: str, phone: str) -> bool:
        """Создает нового клиента в базе данных"""
        client_data = {
            "TelegramID": telegram_id,
            "Имя": name,
            "Телефон": phone,
        }

        try:
            record = self.clients_table.create(client_data)

            logging.info(f"Создан клиент: {record['id']}")
            return True
        
        except Exception as e:
            logging.error(f"Ошибка создания клиента: {e}")
            return False
        
    async def get_categories(self):
        """Получает все категории"""
        records = self.categories_table.all()
        return records
    
    async def get_masters_by_category(self, category):
        """Получает всех мастеров по категории"""
        formula = f"FIND('{category}', {{Тип услуг}})"
        all_masters = self.masters_table.all(formula=formula)
        
        # Фильтруем мастеров, у которых есть свободные слоты
        available_masters = []
        
        for master in all_masters:
            master_name = master["fields"]["Имя"]
            
            # Проверяем наличие свободных слотов для этого мастера
            slots_formula = f"AND(FIND('{category}', {{Категория}}), NOT({{Занято}}), TODAY() <= {{Дата}}, {{Мастер}} = '{master_name}')"
            available_slots = self.slots_table.first(formula=slots_formula)
            
            # Если есть хотя бы один свободный слот, добавляем мастера в список
            if available_slots:
                available_masters.append(master)
        
        return available_masters
    
    async def get_master_name(self, id):
        """Получает имя мастера по его ID"""
        record = self.masters_table.get(id)
        return record["fields"]["Имя"]
    
    async def get_procedures_by_category(self, category):
        """Получает все процедуры по категории"""
        formula = f"FIND('{category}', {{Вид}})"
        records = self.procedures_table.all(formula=formula)
        return records
    
    async def get_category_days(self, category, master_name):
        """Получает все слоты по категории и мастеру"""
        formula = f"AND(FIND('{category}', {{Категория}}), NOT({{Занято}}), TODAY() <= {{Дата}}, {{Мастер}} = '{master_name}')"
        records = self.slots_table.all(formula=formula, fields=["Дата", "Время начала", "Время окончания", "id"])
        return records
    
    async def get_category_name(self, id) -> str:
        """Получает название категории по ее ID"""
        record = self.categories_table.get(id)
        return record["fields"]["Название"] 
    
    async def get_procedure_data(self, id):
        """Получает данные процедуры по ее ID"""
        record = self.procedures_table.get(id)
        return record
    
    async def book_slot(self, slot_id: str, client_id: str, procedure_id: str) -> bool:
        """Записывает клиента на слот"""
        try:
            update_data = {
                "Занято": True,
                "Клиент": [client_id],
                "Процедура": [procedure_id]
            }

            slot_data = self.slots_table.first(formula=f"{{id}} = '{slot_id}'")
  
            # Проверяем, занят ли слот
            if not slot_data or slot_data["fields"].get("Занято", False):
                return False
            
            self.slots_table.update(slot_data["id"], update_data)
            logging.info(f"Успешная запись: клиент {client_id} на слот {slot_id}")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка записи на слот {slot_id}: {e}")
            return False

    
airtable = AirtableManager()