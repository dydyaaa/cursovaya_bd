### Описание проекта

"Insurance Management System" – это веб-приложение для управления страховыми полисами и происшествиями. Пользователи могут зарегистрироваться, стать клиентами и оформлять страховые полисы или сообщать о происшествиях. Агент проверяет и принимает решения по заявкам пользователей.

---

### Основные компоненты

1. **inshurance** – Backend на Flask
2. **client** – Frontend на Flask с Bootstrap для интерфейса
3. **PostgreSQL** – База данных

---

### Основные роли

- **Пользователь**: Регистрация, ввод данных, запросы на полисы и происшествия.
- **Агент**: Проверка заявок на полисы и происшествия, одобрение/отклонение заявок.
- **Админ**: Управление базой данных, создание аккаунтов для Агентов

---

### Функциональные возможности

- **Регистрация** пользователей и вход в систему.
- **Оформление полисов** и **происшествий** после проверки агентом.
- **Админ-панель** для выполнения SQL-запросов и управления таблицами через GUI.

---

### Используемые технологии

- **Flask** – Backend и Frontend
- **PostgreSQL** – Реляционная база данных
- **JWT** – Аутентификация
- **Bootstrap 5** – UI

---

### Запуск проекта

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Настройте базу данных PostgreSQL в `settings.json`.

3. Запустите приложение (в разных консолях):
   ```bash
   python Inshurance/wsgi.py
   python client/main.py
   docker-compose start
   ```

---

### API Роуты

- **/api/register** – Регистрация 
- **/api/login** – Авторизация 
- **/api/profile** – Профиль пользователя
- **/api/become_client** – Стать клиентом 
- **/api/change_password** – Смена пароля

---

### Админ-панель

1. **SQL запросы** – Возможность выполнения произвольных SQL запросов через интерфейс на сайте.
2. **Управление таблицами через GUI** – Визуальная работа с таблицами базы данных, аналогичная "DataBase Client JDBC" в VSCode.

---

### Структура базы данных

#### Таблица `Users`

| Поле          | Тип данных     | Описание                       |
|---------------|----------------|--------------------------------|
| user_id       | SERIAL (PK)     | Уникальный идентификатор       |
| user_login    | VARCHAR(255)    | Логин пользователя             |
| password_hash | VARCHAR(255)    | Хэш пароля                     |
| user_role     | VARCHAR(255)    | Роль пользователя (по умолчанию 'guest') |

#### Таблица `Clients`

| Поле            | Тип данных     | Описание                     |
|-----------------|----------------|------------------------------|
| client_id       | SERIAL (PK)     | Уникальный идентификатор     |
| birth_day       | DATE            | Дата рождения                |
| client_name     | VARCHAR(255)    | Имя клиента                  |
| passport_series | INTEGER         | Серия паспорта               |
| passport_number | INTEGER         | Номер паспорта               |
| contact_number  | VARCHAR(20)     | Контактный телефон           |
| address         | VARCHAR(255)    | Адрес проживания             |
| user_id         | INTEGER (FK)    | Связь с пользователем        |

#### Таблица `Policies`

| Поле            | Тип данных     | Описание                     |
|-----------------|----------------|------------------------------|
| policy_id       | SERIAL (PK)     | Уникальный идентификатор     |
| policy_type     | VARCHAR(255)    | Тип полиса                   |
| agent_id        | INTEGER (FK)    | Агент, который оформил       |
| client_id       | INTEGER (FK)    | Клиент, которому оформлен    |
| date_start      | DATE            | Дата начала полиса           |
| date_stop       | DATE            | Дата окончания полиса        |
| sum_insurance   | INTEGER         | Сумма страхования            |
| status          | VARCHAR(255)    | Статус полиса                |

#### Таблица `Cases`

| Поле            | Тип данных     | Описание                     |
|-----------------|----------------|------------------------------|
| case_id         | SERIAL (PK)     | Уникальный идентификатор     |
| policy_id       | INTEGER (FK)    | Связь с полисом              |
| agent_id        | INTEGER (FK)    | Агент, проверяющий случай    |
| date            | DATE            | Дата происшествия            |
| description     | TEXT            | Описание происшествия        |
| status          | VARCHAR(255)    | Статус проверки              |
| sum             | INTEGER         | Сумма возмещения             |

--- 

### Настройка сервера

#### Установка git

```bash
sudo apt-get update
sudo apt-get install git
```

#### Установка nginx

```bash
sudo apt update
sudo apt install nginx
```

#### Установка docker

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Клонирование проекта

```bash
git clone git clone --branch prod --single-branch https://github.com/dydyaaa/cursovaya_bd.git
```

#### Первый запуск контейнеров

```bash
docker compose up --build
```

#### Последующая работа с контейнерами

```bash
docker compose stop
docker compose start
```

#### Настройка nginx

```bash
sudo nano /etc/nginx/sites-available/sogazik.ru
```

Добавить конфигурацию в файл

```nginx
server {
    listen 80;
    server_name sogazik.ru www.sogazik.ru;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/static/files; 
    }
}
```

#### Активация nginx

```bash
sudo ln -s /etc/nginx/sites-available/sogazik.ru /etc/nginx/sites-enabled/
```

#### Перезапуск nginx

```bash
sudo systemctl restart nginx
```

### Дополнительно

- Для тестирования API использовался Postman.
- В проекте реализована JWT аутентификация для защиты маршрутов. Токен передается в заголовке запроса (`Authorization: token`).