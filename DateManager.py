import datetime

class DateConverter:
    @staticmethod
    def convert_to_date(date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print(f"Ошибка: Невалидная дата '{date_str}'. Ожидается формат ГГГГ-ММ-ДД.")
            return None
