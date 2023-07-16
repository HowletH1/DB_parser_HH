from database.db_creator import DBCreator
from database.db_manager import DBManager
from src.config import config
from utils.hh_parser import HHAPI


def main():
    hh = HHAPI()
    params = config()
    database_name = "vacancies_db"

    print("Программа предназначена для получения данных о компаниях и их вакансиях!\n")

    employers, vacancies = hh.get_list()

    db = DBCreator(employers, vacancies, database_name, params)
    db.db_creation()

    db.employers_saver()
    db.vacancies_saver()

    print(f"Сохранено!")

    manager = DBManager(database_name, params)

    while True:
        command = input('\nВыберете действие:\n'
                        '1: Вывод списка всех компаний и количество вакансий у каждой компании;\n'
                        '2: Вывод списка всех вакансий с указанием названий компании, '
                        'вакансий, зарплаты и ссылки на вакансию;\n'
                        '3: Вывод средней зарплаты;\n'
                        '4: Вывод списка всех вакансий, у которых зарплата выше средней;\n'
                        '5: Вывод списка всех вакансий по запросу;\n'
                        '6: Выход\n').strip()

        if command.lower() == "1":
            results = manager.get_companies_and_vacancies_count()
            for result in results:
                print(f"{result[0]}: {result[1]}")

        elif command.lower() == "2":
            results = manager.get_all_vacancies()
            for result in results:
                print(f'Компания: {result[0]}, Вакансия: {result[1]}, Зарплата от: {result[2]},'
                      f'Зарплата до: {result[3]}, url: {result[4]}\n')

        elif command.lower() == "3":
            results = manager.get_avg_salary()
            for result in results:
                print(f'Средняя зарплата по всем вакансиям: {result[0]}')

        elif command.lower() == "4":
            results = manager.get_vacancies_with_higher_salary()
            for result in results:
                print(result[0])

        elif command.lower() == "5":
            key_word = input("Введите название вакансии или ключевое слово для поиска\n")
            results = manager.get_vacancies_with_keyword(key_word)
            for result in results:
                print(f'{result[1]}, Зарплата от: {result[2]}, '
                      f'Зарплата до: {result[3]}, Валюта: {result[4]}, '
                      f'Компания: {result[5]}, url: {result[7]}\n'
                      )

        elif command.lower() == "6":
            print("Завершено.\n")
            break


if __name__ == '__main__':
    main()
