from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL del backend
BACKEND_URL = "http://localhost:5000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query = request.form.get('query')
    response = requests.post(f"{BACKEND_URL}/query", json={"query": query})
    products = response.json()
    return render_template('index.html', products=products)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        name = request.form.get('name')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        # Validar que el ID del producto esté presente
        if not product_id:
            message = "Error: Se requiere el ID del producto."
            return render_template('update.html', message=message)

        try:
            # Enviar solicitud al backend
            response = requests.post(f"{BACKEND_URL}/update", json={
                "id": int(product_id),
                "name": name,
                "category": category,
                "quantity": int(quantity) if quantity else None,
                "price": float(price) if price else None
            })
            message = response.json().get('message', 'rror al actualizar el producto')
        except ValueError:
            message = "Error: La cantidad y el precio deben ser números válidos."

        return render_template('update.html', message=message)

    return render_template('update.html')
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        
        # Validar que el ID no esté vacío
        if not product_id:
            message = "Error: Se requiere el ID del producto para eliminar un producto."
            return render_template('delete.html', message=message)
        
        try:
            # Enviar solicitud al backend
            response = requests.post(f"{BACKEND_URL}/delete", json={"id": int(product_id)})
            message = response.json().get('message', 'Error al eliminar el producto')
        except ValueError:
            message = "Error: El ID del producto debe ser un número válido."
        
        return render_template('delete.html', message=message)
    
    return render_template('delete.html')

@app.route('/products', methods=['GET'])
def products():
    response = requests.post(f"{BACKEND_URL}/query", json={"query": ""})  # Enviar una consulta vacía para obtener todos los productos
    products = response.json()
    return render_template('products.html', products=products)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        # Validar que todos los campos estén presentes
        if not all([name, category, quantity, price]):
            message = "Error: Todos los campos son obligatorios."
            return render_template('create.html', message=message)

        try:
            # Enviar solicitud al backend
            response = requests.post(f"{BACKEND_URL}/create", json={
                "name": name,
                "category": category,
                "quantity": int(quantity),
                "price": float(price)
            })
            message = response.json().get('message', 'Error al crear el producto')
        except ValueError:
            message = "Error: La cantidad y el precio deben ser números válidos."

        return render_template('create.html', message=message)

    return render_template('create.html')
if __name__ == '__main__':
    app.run(debug=True, port=5001)