import pymongo
import json
from pandas import DataFrame
import datetime

CONNECTION_STRING = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
DATABASE = 'coursework'


myclient = pymongo.MongoClient(CONNECTION_STRING)
mydb = myclient[DATABASE]
mycol = mydb["service"]

# mycol.drop()
# with open('Databases/MongoDB/configs/my_order.json') as f:
#     file_data = json.load(f)
#
# mycol.insert_one(file_data)
#

data1 = {
    "commissions": datetime.datetime.strptime("2021-05-01 14:25:10", "%Y-%m-%d %H:%M:%S"),
    "executions": datetime.datetime.strptime("2021-05-02 13:30:00", "%Y-%m-%d %H:%M:%S"),
    "stage_id": 1,
    "stage_title": "Выполняется",
    "stage_description": "Заказ в процессе выполнения.",
    "orders_service_id": 1,
    "orders_service_title": "Грузоперевозки",
    "orders_service_description": "Квартирные и дачные переезды, офисные переезды, доставка мебели, строительных материалов, перевозка крупногабаритных грузов.",
    "orders_service_cost_weight": 4,
    "orders_service_cost_radius": 6,
    "orders_service_quantity_weight": 10,
    "orders_service_quantity_radius": 10,
    "orders_service_total_cost": 100,
    "destinations_address": "ADDRESS1",
    "departures_address": "ADDRESS2",
    "orders_service_begin_city": "Гомель",
    "orders_service_end_city": "Гродно"
}

data2 = {
    "customer_id": 1,
    "employee_id": 1,
    "status_id": 4,
    "status_title": "Свободен",
    "status_description": "Сотрудник доступен и ему можно поручить задание.",
    "country": "Беларусь",
    "street": "ул. УЛИЦА1",
    "home_number": 20,
    "flat_number": 77,
    "last_name": "Прокопенко",
    "name": "Артур",
    "middle_name": "Романович",
    "login": "art",
    "password": "123",
    "email": "arturprokopenko01@gmail.com",
    "phone_number": "375333242810",
    "salary": 100000,
    "passport_data": "HB11111111",
    "requirements": "requirements1",
    "duties": "duties1",
    "roles": {
        "role_id": [1, 2, 3, 4],
        "role_title": ["Клиент", "Директор", "Оператор", "Курьер"],
        "role_description": ["Заказывает платные услуги.", "Ведет справочники, прейскурант, проверяет отчетность.",
                             "Распределяет оплаченные заказы между курьерами.", "Выполняет заказы."]
    }
}

data3 = {
    "city_title": "Гомель",
    "city_fleets": {
        "fleet_id": [1, 2],
        "fleet_title": ["ПА-1", "ПА-2"],
        "fleet_description": ["", ""],
        "fleet_address": ["ул. УЛИЦА1, д.10", "ул. УЛИЦА2, д.100"],
        "fleet_square": [300, 100],
        "fleet_stars_quantity": [4, 3],
        "fleet_transport": [
            {
                "transport_id": [1],
                "kind_id": [1],
                "kind_description": ["Подойдет для грузов, не требующих особых условий транспортировки. Обычно это стройматериалы."],
                "kind_title": ["Бортовой грузовик", "Рефрижератор"],
                "kind_lifting_capacity": [8000],
                "kind_volume": [12.5]
            },
            {
                "transport_id": [2],
                "kind_id": [3],
                "kind_description": ["Оборудованный холодильными установками фургон. В нем перевозят обычно продукты, цветы."],
                "kind_title": ["Рефрижератор"],
                "kind_lifting_capacity": [4000],
                "kind_volume": [24]
            }
        ]
    }
}

data = {
    "_id": 4,
    "service_title": "Специальные грузоперевозки",
    "service_description": "Перевозки продуктов, спецвеществ и прочее.",
    "cost_weight": 5,
    "cost_radius": 10
}
mycol.insert_one(data)

for x in mycol.find():
    print(x)
