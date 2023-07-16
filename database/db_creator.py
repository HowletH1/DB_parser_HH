import psycopg2


class DBCreator:

    def __init__(self, employers, vacancies, db_name, params):
        self.employers = employers
        self.vacancies = vacancies
        self.db_name = db_name
        self.params = params

    def db_creation(self):
        """
        Создание баз данных и таблиц.
        """
        connection = psycopg2.connect(dbname='postgres', **self.params)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        cursor.execute(f"CREATE DATABASE {self.db_name}")
        connection.close()

        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS employers (
                                id_employer INT PRIMARY KEY, 
                                company_name VARCHAR(100),
                                url TEXT) """)

            with connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS vacancies (
                                vacancy_id INT PRIMARY KEY,
                                vacancy_name VARCHAR(200) NOT NULL,
                                salary_from INT,
                                salary_to INT,
                                currency VARCHAR(10),
                                name_employer VARCHAR(100),
                                id_employer INT REFERENCES employers(id_employer),
                                url TEXT)""")
        connection.close()

    def employers_saver(self):
        """
        Сохранение данных о компаниях.
        """

        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                for employer in self.employers:
                    cursor.execute("""INSERT INTO employers (id_employer, company_name, url) 
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (id_employer) DO NOTHING""",

                                   (employer['id_company'], employer['name_company'], employer['url']))

        connection.close()

    def vacancies_saver(self):
        """
        Сохранение данных о вакансиях
        """

        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                for vacancy in self.vacancies:
                    cursor.execute("""INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to,
                                    currency, name_employer, id_employer, url) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (vacancy_id) DO NOTHING""",

                                   (vacancy['id_vacancy'], vacancy['title'], vacancy['salary_min'],
                                    vacancy['salary_max'], vacancy['currency'], vacancy['employer'],
                                    vacancy['id_employer'], vacancy['url']))

        connection.close()
