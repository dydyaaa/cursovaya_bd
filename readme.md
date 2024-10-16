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

![структура](/assets/image.png)

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
        proxy_pass http://127.0.0.1:3000/static/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Установка Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

#### Запуск Certbot

```bash
sudo certbot --nginx -d sogazik.ru -d www.sogazik.ru --email your-email@example.com
```

#### Активация nginx

```bash
sudo ln -s /etc/nginx/sites-available/sogazik.ru /etc/nginx/sites-enabled/
```

#### Перезапуск nginx

```bash
sudo systemctl restart nginx
```

#### Проверка синтаксиса 

```bash
sudo nginx -t
```

#### Удалить старый ssh

```bash
ssh-keygen -R <ip>
```

#### Удалить все образы и контейнеры

```bach
docker system prune -a
```

### Дополнительно

- Для тестирования API использовался Postman.
- В проекте реализована JWT аутентификация для защиты маршрутов. Токен передается в заголовке запроса (`Authorization: token`).

### Бизнес правила

1. Нельзя оформить 2 полиса одного типа на один автомобиль 
2. Нельзя стать клиентом, не будучи совершеннолетним
3. Нельзя оформить полис "задним числом"
