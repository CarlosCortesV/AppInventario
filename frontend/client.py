import requests

class Client:
    def __init__(self, server_url):
        self.server_url = server_url

    def send_query(self, query):
        response = requests.post(f"{self.server_url}/query", json={"query": query})
        return response.json()

    def send_update(self, product_id, quantity):
        response = requests.post(f"{self.server_url}/update", json={"id": product_id, "quantity": quantity})
        return response.json()

    def run(self):
        while True:
            operation = input("Choose operation (query/update/exit): ").strip().lower()
            if operation == "query":
                query = input("Enter product name or category: ")
                result = self.send_query(query)
                print("Query Result:", result)
            elif operation == "update":
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter new quantity: "))
                result = self.send_update(product_id, quantity)
                print("Update Result:", result)
            elif operation == "exit":
                print("Exiting the client.")
                break
            else:
                print("Invalid operation. Please choose 'query', 'update', or 'exit'.")

if __name__ == "__main__":
    client = Client("http://localhost:5000")
    client.run()