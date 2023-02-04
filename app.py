import time

import psycopg2
from psycopg2 import DatabaseError
from flask import Flask, render_template

app = Flask(__name__)
conn = psycopg2.connect(host="postgres", user="postgres", password="admin", database="flask_api")
cursor = conn.cursor()

# Funcion auxiliar para el endpoint del metodo GET
def get_counter_value():
    retries = 5
    while True:
        try:
            cursor.execute('SELECT count FROM Contador;')
            rows = cursor.fetchall()
            res = None
            for row in rows:
                res = row[0]
            return res
        except conn.Error as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# Funcion auxiliar para el endpoint del metodo DELETE
def delete_counter_value():
    retries = 5
    while True:
        try:
            cursor.execute('UPDATE Contador SET count = 0 WHERE id = 1;')
            cursor.execute('SELECT count FROM Contador;')
            rows = cursor.fetchall()
            res = None
            for row in rows:
                res = row[0]
            return res
        except conn.Error as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# Funcion auxiliar para el endpoint del metodo PUT y POST
def update_counter_value(value):
    retries = 5
    while True:
        try:
            cursor.execute('UPDATE Contador SET count = {} WHERE id = 1;'.format(value))
            cursor.execute('SELECT count FROM Contador;')
            rows = cursor.fetchall()
            res = None
            for row in rows:
                res = row[0]
            return res
        except conn.Error as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# curl -i -X GET http://localhost:7000/counter
@app.route('/counter', methods=['GET'])
def get_method():
    counter = get_counter_value()
    return 'El valor del contador es de {} unidades.\n'.format(counter)

# curl -i -X DELETE http://localhost:7000/counter
@app.route('/counter', methods=['DELETE'])
def delete_method():
    counter = delete_counter_value()
    return 'Contador reiniciado exitosamente.\nEl valor del contador es de {} unidades.\n'.format(counter)

# curl -i -X PUT http://localhost:7000/counter/<int:value>
# curl -i -X POST http://localhost:7000/counter/<int:value>
@app.route('/counter/<int:value>', methods=['PUT', 'POST'])
def update_method(value):
    counter = update_counter_value(value)
    return 'Valor asignado exitosamente al contador.\nEl valor del contador es de {} unidades.\n'.format(counter)