from flask import Flask, request, jsonify, g
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configuración de la conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'carlos12',
    'database': 'inventory_db'
}

# Variables globales para métricas
request_count = 0
total_latency = 0
start_time_server = time.time()

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_request(response):
    global request_count, total_latency
    latency = (time.time() - g.start_time) * 1000
    request_count += 1
    total_latency += latency
    return response

@app.route('/stats')
def stats():
    uptime = time.time() - start_time_server
    avg_latency = total_latency / request_count if request_count else 0
    throughput = request_count / uptime if uptime > 0 else 0
    return jsonify({
        "total_requests": request_count,
        "avg_latency_ms": round(avg_latency, 2),
        "throughput_rps": round(throughput, 2)
    })

@app.route('/query', methods=['POST'])
def query_products():
    data = request.json
    query = data.get('query', '')
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE name LIKE %s OR category LIKE %s", (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
    connection.close()
    return jsonify(results)

@app.route('/update', methods=['POST'])
def update_product():
    data = request.json
    product_id = data.get('id')
    name = data.get('name')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    if not product:
        connection.close()
        return jsonify({"message": "Error: Producto NO Encontrado"}), 404

    try:
        if quantity is not None:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError("La cantidad debe ser un número positivo")
        if price is not None:
            price = float(price)
            if price < 0:
                raise ValueError("El precio debe ser un número positivo")
    except ValueError as e:
        connection.close()
        return jsonify({"message": f"Error: {str(e)}"}), 400

    name = name if name else product['name']
    category = category if category else product['category']
    quantity = quantity if quantity is not None else product['quantity']
    price = price if price is not None else product['price']

    cursor.execute(
        "UPDATE products SET name = %s, category = %s, quantity = %s, price = %s WHERE id = %s",
        (name, category, quantity, price, product_id)
    )
    connection.commit()
    connection.close()
    return jsonify({"message": "Producto actualizado exitosamente!"})

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    connection.close()
    if not product:
        return jsonify({"message": "Error: Producto NO Encontrado"}), 404
    return jsonify(product)

@app.route('/delete', methods=['POST'])
def delete_product():
    data = request.json
    product_id = data.get('id')
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    if not product:
        connection.close()
        return jsonify({"message": "Error: Producto NO Encontrado"}), 404

    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": "Producto eliminado exitosamente!"})

@app.route('/create', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    if not all([name, category, quantity, price]):
        return jsonify({"message": "Error: Todos los campos son obligatorios"}), 400

    try:
        quantity = int(quantity)
        price = float(price)
        if quantity < 0 or price < 0:
            return jsonify({"message": "Error: La cantidad y el precio deben ser números positivos"}), 400
    except ValueError:
        return jsonify({"message": "Error: La cantidad y el precio deben ser números válidos"}), 400

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, quantity, price) VALUES (%s, %s, %s, %s)",
        (name, category, quantity, price)
    )
    connection.commit()
    connection.close()
    return jsonify({"message": "Producto creado exitosamente"})

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"message": "Error: Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Error: Error Interno del Servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
