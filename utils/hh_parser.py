import requests

# 1740 Яндекс
# 2180 Ozon
# 23186 Русагро
# 15478 VK
# 78638 Тинькофф
# 4457416 Сириус


class HHAPI:
    """ Класс для получения и сохранения данных о работодателях и их вакансиях. """

    def __init__(self):
        self.__header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx 05)"}
        self.__params = {"page": 0, "per_page": 100, "only_with_salary": True}
        self.employers_id = ["1740", "2180", "15478", "23186", "78638", "4457416", "6189"]
        self.employers = []
        self.vacancies = []

    def get_employers(self, employer_id):
        """
        Запрос данных о компаниях по id
        """
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url, params=self.__params, headers=self.__header)

        if response.status_code != 200:
            raise f"Request failed with status code: {response.status_code}"
        return response.json()

    def get_vacancies(self, employer_id):
        """
        Запрос данных о вакансиях компаний по id работодателя
        """
        url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        response = requests.get(url, params=self.__params, headers=self.__header)

        if response.status_code != 200:
            raise f"Request failed with status code: {response.status_code}"
        return response.json()['items']

    def get_list(self):
        """
        Получение списка, для дальнейшего сохранения в БД
        """

        for emp in self.employers_id:
            employer = self.get_employers(emp)
            self.employers.append({'id_company': employer['id'],
                                   'name_company': employer['name'],
                                   'url': employer['alternate_url']})

            for self.__params['page'] in range(10):
                values = self.get_vacancies(emp)
                for val in values:
                    if val['salary']['currency'].lower() == 'rur':
                        salary_min, salary_max = self.get_salary(val['salary'])
                        self.vacancies.append({"id_vacancy": val['id'],
                                               "title": val['name'],
                                               "salary_min": salary_min,
                                               "salary_max": salary_max,
                                               "currency": val['salary']['currency'],
                                               "employer": val['employer']['name'],
                                               "id_employer": val['employer']['id'],
                                               "url": val['alternate_url']})
                    else:
                        continue
        return self.employers, self.vacancies

    @staticmethod
    def get_salary(salary):
        formatted_salary = [None, None]
        if salary['from'] is None:
            formatted_salary[0] = salary['to']
        else:
            formatted_salary[0] = salary['from']
        if salary['to'] is None:
            formatted_salary[1] = salary['from']
        else:
            formatted_salary[1] = salary['to']

        return formatted_salary
