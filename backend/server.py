from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración de la conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Cambia esto si tienes un usuario diferente
    'password': 'carlos12',  # Cambia esto por tu contraseña
    'database': 'inventory_db'
}

# Ruta para consultar productos
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

# Ruta para actualizar productos
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

    # Validar que el producto exista
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    if not product:
        connection.close()
        return jsonify({"message": "Error: Producto NO Encontrado"}), 404

    # Validar que cantidad y precio sean números válidos si se proporcionan
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

    # Mantener los valores existentes si no se proporcionan nuevos
    name = name if name else product['name']
    category = category if category else product['category']
    quantity = quantity if quantity is not None else product['quantity']
    price = price if price is not None else product['price']

    # Actualizar el producto
    cursor.execute(
        "UPDATE products SET name = %s, category = %s, quantity = %s, price = %s WHERE id = %s",
        (name, category, quantity, price, product_id)
    )
    connection.commit()
    connection.close()
    return jsonify({"message": "Producto actualizado exitosamente!"})

# Ruta para obtener un producto específico
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

# Ruta para eliminar productos
@app.route('/delete', methods=['POST'])
def delete_product():
    data = request.json
    product_id = data.get('id')
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    # Validar que el producto exista
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    if not product:
        connection.close()
        return jsonify({"message": "Error: Producto NO Encontrado"}), 404

    # Eliminar el producto
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": "Producto eliminado exitosamente!"})

# Ruta para crear productos
@app.route('/create', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    # Validar que todos los campos estén presentes
    if not all([name, category, quantity, price]):
        return jsonify({"message": "Error: Todos los campos son obligatorios"}), 400

    # Validar que cantidad y precio sean números válidos
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
    return jsonify({"message": "Error: rror Interno del Servidor"}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)