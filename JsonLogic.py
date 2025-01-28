import json
import os

#выносим работу с json как отдельный класс.
class JsonManager:
    def __init__(self, filename='records.json'):
        self.filename = filename

    def load_records(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print("Ошибка чтения файла JSON. Возможно, файл поврежден.")
                    return []
        else:
            print("Файл не найден, будут использоваться пустые записи.")
            return []

    def save_records(self, records):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(records, file, ensure_ascii=False, indent=4)
            print("Записи сохранены в файл JSON.")
