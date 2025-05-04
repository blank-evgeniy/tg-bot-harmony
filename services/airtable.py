from config import AIRTABLE_TOKEN, BASE_ID
from pyairtable import Api

class AirtableManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AirtableManager, cls).__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def __init__(self):
        self.api = Api(AIRTABLE_TOKEN)
        self.base_id = BASE_ID
        
    def get_table(self, table_name):
        """Возвращает объект таблицы"""
        return self.api.table(self.base_id, table_name)
    
    def get_all_records(self, table_name):
        """Получает все записи из таблицы"""
        table = self.get_table(table_name)
        return table.all()
    
    def get_free_slots(self):
        """Пример специализированного метода для услуг"""
        table = self.get_table("Слоты")
        records = table.all()
        return [record['fields'] for record in records if 'fields' in record]