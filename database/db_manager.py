import psycopg2


class DBManager:

    def __init__(self, db_name, params):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получение списка всех компаний и количества вакансий
        """

        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT name_employer, COUNT(name_employer)
                                FROM vacancies 
                                GROUP BY vacancies.name_employer""")
                result = cursor.fetchall()

        connection.close()
        return result

    def get_all_vacancies(self):
        """
        Получение списка всех вакансий с указанием названий, зарплаты и ссылки на нее.
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT name_employer, vacancy_name, salary_from, salary_to, url
                                FROM vacancies""")
                result = cursor.fetchall()

        connection.close()
        return result

    def get_avg_salary(self):
        """
        Средняя зарплата по вакансиям
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT AVG((salary_from+salary_to)/2) 
                                FROM vacancies""")
                result = cursor.fetchall()

        connection.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Список вакансий, у которых зарплата выше средней
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT vacancy_name FROM vacancies
                                WHERE ((salary_from+salary_to)/2) > (SELECT AVG((salary_from+salary_to)/2) 
                                FROM vacancies)""")
                result = cursor.fetchall()

        connection.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM vacancies 
                                WHERE vacancy_name LIKE '%{keyword}%'""")
                result = cursor.fetchall()

        connection.close()
        return result
