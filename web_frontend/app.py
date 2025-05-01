from flask import Flask, render_template, request, redirect, url_for, g
import requests
import time

app = Flask(__name__)

# URL del backend
BACKEND_URL = "http://localhost:5000"

# Variables globales para estadísticas
request_count = 0
total_latency = 0.0
start_time_server = time.time()

# Middleware para medir latencia por solicitud
@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def record_metrics(response):
    global request_count, total_latency
    if hasattr(g, 'start_time'):
        latency = (time.time() - g.start_time) * 1000  # en milisegundos
        total_latency += latency
        request_count += 1
    return response

# Página de estadísticas
@app.route('/stats')
def stats():
    uptime_seconds = time.time() - start_time_server
    avg_latency = total_latency / request_count if request_count else 0
    throughput = request_count / uptime_seconds if uptime_seconds else 0

    return f'''
    <h2>Estadísticas del servidor</h2>
    <p>Total de peticiones: {request_count}</p>
    <p>Tiempo activo: {round(uptime_seconds, 2)} segundos</p>
    <p>Latencia promedio: {round(avg_latency, 2)} ms</p>
    <p>Throughput: {round(throughput, 2)} solicitudes/segundo</p>
    '''

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

        if not product_id:
            message = "Error: Se requiere el ID del producto."
            return render_template('update.html', message=message)

        try:
            response = requests.post(f"{BACKEND_URL}/update", json={
                "id": int(product_id),
                "name": name,
                "category": category,
                "quantity": int(quantity) if quantity else None,
                "price": float(price) if price else None
            })
            message = response.json().get('message', 'Error al actualizar el producto')
        except ValueError:
            message = "Error: La cantidad y el precio deben ser números válidos."

        return render_template('update.html', message=message)

    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        product_id = request.form.get('product_id')

        if not product_id:
            message = "Error: Se requiere el ID del producto para eliminar un producto."
            return render_template('delete.html', message=message)

        try:
            response = requests.post(f"{BACKEND_URL}/delete", json={"id": int(product_id)})
            message = response.json().get('message', 'Error al eliminar el producto')
        except ValueError:
            message = "Error: El ID del producto debe ser un número válido."

        return render_template('delete.html', message=message)

    return render_template('delete.html')

@app.route('/products', methods=['GET'])
def products():
    response = requests.post(f"{BACKEND_URL}/query", json={"query": ""})
    products = response.json()
    return render_template('products.html', products=products)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if not all([name, category, quantity, price]):
            message = "Error: Todos los campos son obligatorios."
            return render_template('create.html', message=message)

        try:
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
