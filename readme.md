# Структура базы данных

Insurance policies

id
type - varchar
agent_id 
person_id
date start
date stop
sum insurance
status varchar

Clients

person_id SERIAL
birth_day
passport_seria
passport_number
number
adress
user_id


Agents

agent_id
agent_name
agent_role
user_id

Inshurance accidens

id
inshuranse_id
agent_id
date
decription
status
sum

users

user_id
login
password
role


Business rules

Полисы могут продавать только продавцы (Они смогут добавлять клиентов, и страховые полисы)
Регистрировать страховые случаи могут только плательзики??? (У них будет доступ к таблице случаи)
Если полис истек, страховая компания не несет ответственности за страховые случаи после окончания срока действия.
Сумма выплаты по страховому случаю не может превышать сумму страхового покрытия, указанную в полисе.

routes:

main GET

register GET / POST
login GET / POST

get my polis GET
get my insh GET

add polis
add user
