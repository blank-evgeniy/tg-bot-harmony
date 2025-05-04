import logging
from config import AIRTABLE_TOKEN, BASE_ID
from pyairtable import Api

class AirtableManager:
    def __init__(self):
        self.api = Api(AIRTABLE_TOKEN)
        self.base_id = BASE_ID
        self.clients_table = self.api.table(self.base_id, "Клиенты")
    
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
    
airtable = AirtableManager()