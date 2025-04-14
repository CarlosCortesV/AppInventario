class DataUpdateHandler:
    def __init__(self, database):
        self.database = database

    def handle_update(self, update_request):
        item_id = update_request.get('id')
        new_data = update_request.get('data')

        if not item_id or not new_data:
            return {"status": "error", "message": "Invalid request"}

        success = self.database.update_data(item_id, new_data)

        if success:
            return {"status": "success", "message": "Data updated successfully"}
        else:
            return {"status": "error", "message": "Data update failed"}