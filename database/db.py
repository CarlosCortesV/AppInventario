def read_data():
    import json
    with open('multi_level_architecture/database/data/sample_data.json', 'r') as file:
        return json.load(file)

def write_data(data):
    import json
    with open('multi_level_architecture/database/data/sample_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_item(item_id):
    data = read_data()
    return next((item for item in data if item['id'] == item_id), None)

def update_item(item_id, new_data):
    data = read_data()
    for index, item in enumerate(data):
        if item['id'] == item_id:
            data[index].update(new_data)
            write_data(data)
            return True
    return False

def get_all_items():
    return read_data()