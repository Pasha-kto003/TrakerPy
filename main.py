print('@MyTraker all rights protected')


def add_expenses(selected_Category, sum):
    if selected_Category != "":
        new_pay = input(f"Введите новый расход в категории {selected_Category}")
        sum += new_pay
        print(sum)
        return sum
    else:
        print('Error!')


categories = ['Еда', 'Транспорт', 'Развлечения']
print("Категория расходов:", categories)
input_data = input('Выберите категорию расходов: ')
if input_data == 'Еда':
    print('Категория расходов еда:')

if input_data == 'Развлечения':
    print('Категория расходов развлечения:')
    add_expenses('Развлечения', 0)

if input_data == 'Транспорт':
    print('Категория расходов еда:')

    categories = ['Еда', 'Транспорт', 'Развлечения']
    print("Категория расходов:", categories)
    input_data = input('Выберите категорию расходов: ')
    if input_data == 'Еда':
        print('Категория расходов еда: ')

    if input_data == 'Развлечения':
        print('Категория расходов развлечения: ')

    if input_data == 'Транспорт':
        print('Категория расходов транспорт: ')

    money_categories = ['Зарплата', 'Вклад']


