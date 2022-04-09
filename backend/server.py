from flask import Flask, request, jsonify
import products_dao
from mysql_connection import get_sql_connection

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route('/removeProducts', methods=['POST'])
def get_products():
    products = products_dao.delete_product(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response
    
if __name__ == "__main__":
    print("Start running")
    app.run(port=5000)