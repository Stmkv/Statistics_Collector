# Сравниваем вакансии программистов

Скрипт позволяет узнать какие среднии зарплаты у языка программирования в данный момент.

## Как установить

Python3 должен быть уже установлен. Затем воспользуйтесь pip (или pip3, есть конфликт с Python2) для установки зависимостей:

`pip install -r requirements.txt`

Необходимо также получить [Secret_key](https://api.superjob.ru/)

После чего создать папку .env, содержимео которой будет выглядеть так:

`SUPER_JOB_SECRET_KEY=# Ваш Secret key`

Пример запуска:

`python main.py`

![Вывод в консоль](https://github.com/Stmkv/Statistics_Collector/assets/169255952/96a0741d-6984-497c-bb69-707064b120d6)


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/) .
