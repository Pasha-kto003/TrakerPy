import datetime
import json
import os

from DateManager import DateConverter
from JsonLogic import JsonManager


class Tracker:
    def __init__(self, json_file = 'records.json'):
        self.json_manager = JsonManager(json_file)
        self.records = self.json_manager.load_records()
        self.income_categories = {'Зарплата', 'Подарочки', 'Вклады'}
        self.expense_categories = {'Еда', 'Транспорт', 'Развлечения'}

    def add_record(self, amount, category, date, description, record_type):
        if record_type == 'расход' and not self.can_afford(amount):
            print(f"Ошибка: недостаточно средств для расхода на сумму {amount:.2f}.")
            return

        record_date = DateConverter.convert_to_date(date)
        if not record_date:
            return

        record = {
            'amount': amount,
            'category': category,
            'date': record_date.strftime("%Y-%m-%d"),
            'description': description,
            'type': record_type
        }

        self.records.append(record)
        self.json_manager.save_records(self.records)
        print("Запись добавлена.")

    def can_afford(self, expense_amount):
        income = sum(r['amount'] for r in self.records if r['type'] == 'доход')
        expenses = sum(r['amount'] for r in self.records if r['type'] == 'расход')
        balance = income - expenses
        return balance >= expense_amount

    def show_balance(self):
        income = sum(r['amount'] for r in self.records if r['type'] == 'доход')
        expenses = sum(r['amount'] for r in self.records if r['type'] == 'расход')
        balance = income - expenses
        print(f"Баланс: {balance:.2f} (Доходы: {income:.2f}, Расходы: {expenses:.2f})")

    def view_period(self, start_date, end_date):
        start_date = DateConverter.convert_to_date(start_date)
        end_date = DateConverter.convert_to_date(end_date)
        if not start_date or not end_date:
            return
        if start_date and end_date:
            print(f"Записи с {start_date.date()} по {end_date.date()}:")
            for record in self.records:
                record_date = DateConverter.convert_to_date(record['date'])
                if start_date <= record_date <= end_date:
                    print(f"{record['date']} | {record['type']} | {record['category']} | {record['amount']} | {record['description']}")

    def view_period_category(self, start_date, end_date, selected_category):
        start_date = DateConverter.convert_to_date(start_date)
        end_date = DateConverter.convert_to_date(end_date)
        if start_date and end_date:
            print(f"Записи с {start_date.date()} по {end_date.date()}: с категорией {selected_category}")
            for record in self.records:
                record_date = DateConverter.convert_to_date(record['date'])
                if start_date <= record_date <= end_date and record['category'] == selected_category:
                    print(f"{record['date']} | {record['type']} | {record['category']} | {record['amount']} | {record['description']}")

    def analyze_expenses(self):
        categories_expenses = {}
        for record in self.records:
            if record['type'] == 'расход':
                category = record['category']
                categories_expenses[category] = categories_expenses.get(category, 0) + record['amount']

        show_top_3 = input("\nХотите увидеть топ-3 расходов по сумме? (Y/N): ").strip().upper()

        if show_top_3 == 'Y':
            sorted_expenses = sorted(categories_expenses.items(), key=lambda x: x[1], reverse=True)
            print("\nТоп-3 расходов:")

            for i, (category, total) in enumerate(sorted_expenses[:3], 1):
                print(f"Место {i}: Категория '{category}' с расходами {total:.2f}")
        else:
            print("Топ-3 расходов не будет отображён.")

        print("Анализ расходов по категориям:")
        for category, total in categories_expenses.items():
            print(f"{category}: {total:.2f}")

    def add_income_category(self):
        category = input("Введите новую категорию доходов: ").strip()
        if category and category not in self.income_categories:
            self.income_categories.add(category)
            print(f"Категория '{category}' добавлена в список доходов.")
        else:
            print(f"Категория '{category}' уже существует или не указана.")

    def show_income_expense_ratio(self):
        income = sum(r['amount'] for r in self.records if r['type'] == 'доход')
        expenses = sum(r['amount'] for r in self.records if r['type'] == 'расход')
        ratio = expenses / income if income != 0 else float('inf')

        print(f"Доходы: {income:.2f}, Расходы: {expenses:.2f}, Соотношение расходов к доходу: {ratio:.2f}")

        if ratio < 1:
            print("Доходы больше расходов.")
        elif ratio > 1:
            print("Расходы превышают доходы.")
        else:
            print("Доходы и расходы равны.")

    def add_expense_category(self):
        category = input("Введите новую категорию расходов: ").strip()
        if category and category not in self.expense_categories:
            self.expense_categories.add(category)
            print(f"Категория '{category}' добавлена в список расходов.")
        else:
            print(f"Категория '{category}' уже существует или не указана.")

    def show_categories(self):
        print("Доступные категории доходов:")
        print(self.income_categories if self.income_categories else "Нет категорий доходов.")

        print("\nДоступные категории расходов:")
        print(self.expense_categories if self.expense_categories else "Нет категорий расходов.")

    def read_records_from_json(self):
        records = self.json_manager.load_records()
        if records:
            print("\nВсе записи из JSON файла:")
            for record in records:
                print(
                    f"{record['date']} | {record['type']} | {record['category']} | {record['amount']} | {record['description']}")
        else:
            print("Нет данных в файле.")




def main():
    tracker = Tracker()

    while True:
        print("\nМеню:")
        print("1. Добавить доход")
        print("2. Добавить расход")
        print("3. Показать баланс")
        print("4. Просмотр за период")
        print("5. Анализ расходов по категориям")
        print("6. Добавить категорию доходов")
        print("7. Добавить категорию расходов")
        print("8. Показать категории")
        print("9. Просмотр с фильтром")
        print("10. Соотношение расходов и доходов")
        print("11. Чтение данных с JSON")
        print('12. Выход')

        choice = input("Выберите действие: ")

        if choice == '1':
            print("Доступные категории доходов:", tracker.income_categories)
            category = input("Выберите категорию дохода: ")
            if category not in tracker.income_categories:
                print("Такой категории нет. Пожалуйста, добавьте её сначала.")
                continue
            amount = float(input("Введите сумму дохода: "))
            date = input("Введите дату (ГГГГ-ММ-ДД): ")
            description = input("Введите описание: ")
            tracker.add_record(amount, category, date, description, 'доход')

        elif choice == '2':
            print("Доступные категории расходов:", tracker.expense_categories)
            category = input("Выберите категорию расхода: ")
            if category not in tracker.expense_categories:
                print("Такой категории нет. Пожалуйста, добавьте её сначала.")
                continue
            amount = float(input("Введите сумму расхода: "))
            date = input("Введите дату (ГГГГ-ММ-ДД): ")
            description = input("Введите описание: ")
            tracker.add_record(amount, category, date, description, 'расход')

        elif choice == '3':
            tracker.show_balance()

        elif choice == '4':
            start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
            end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")
            tracker.view_period(start_date, end_date)

        elif choice == '5':
            tracker.analyze_expenses()

        elif choice == '6':
            tracker.add_income_category()

        elif choice == '7':
            tracker.add_expense_category()

        elif choice == '8':
            tracker.show_categories()

        elif choice == '9':
            print('Фильтр по категории и датам')
            print("Доступные категории расходов:", tracker.expense_categories)
            print("Доступные категории доходов:", tracker.income_categories)
            start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
            end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")
            category = input('Выберите категорию расходов или доходов: ')
            tracker.view_period_category(start_date, end_date, category)

        elif choice == '10':
            print('Соотношение расходов и доходов:')
            tracker.show_income_expense_ratio()


        elif choice == '11':
            tracker.read_records_from_json()


        elif choice == '12':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
