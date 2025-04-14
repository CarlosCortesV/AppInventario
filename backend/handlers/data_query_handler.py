class DataQueryHandler:
    def __init__(self, database):
        self.database = database

    def handle_query(self, query):
        if query.get("type") == "get_data":
            return self.database.get_data(query.get("id"))
        elif query.get("type") == "get_all_data":
            return self.database.get_all_data()
        else:
            return {"error": "Invalid query type"}