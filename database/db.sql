CREATE TABLE IF NOT EXISTS employers (
                                id_employer INT PRIMARY KEY,
                                company_name VARCHAR(100),
                                url TEXT);

CREATE TABLE IF NOT EXISTS vacancies (
                                vacancy_id INT PRIMARY KEY,
                                vacancy_name VARCHAR(200) NOT NULL,
                                salary_from INT,
                                salary_to INT,
                                currency VARCHAR(10),
                                name_employer VARCHAR(100),
                                id_employer INT REFERENCES employers(id_employer),
                                url TEXT)