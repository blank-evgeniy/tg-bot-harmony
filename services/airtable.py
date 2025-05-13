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
        formula = f"{{TelegramID}} = '{telegram_id}'"
        record = self.clients_table.first(formula=formula)
        
        return record is not None

    async def create_client(self, telegram_id: int, name: str, phone: str) -> bool:
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
        records = self.categories_table.all()
        return records
    
    async def get_procedures_by_category(self, category):
        formula = f"FIND('{category}', {{Вид}})"
        records = self.procedures_table.all(formula=formula)
        return records
    
    async def get_category_days(self, category):
        formula = f"AND(FIND('{category}', {{Категория}}), NOT({{Занято}}), TODAY() <= {{Дата}})"
        records = self.slots_table.all(formula=formula, fields=["Дата", "Время начала", "Время окончания"])
        return records
    
    async def get_category_name(self, id) -> str:
        record = self.categories_table.get(id)
        return record["fields"]["Название"] 
    
    async def get_procedure_data(self, id) -> str:
        record = self.procedures_table.get(id)
        return record
    
airtable = AirtableManager()