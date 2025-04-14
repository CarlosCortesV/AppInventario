# Multi-Level Architecture Simulation in Python

This project simulates a multi-level architecture application using Python. It consists of three main components: a frontend client, a backend server, and a database. The application allows users to send requests for data queries and updates, demonstrating a basic distributed application structure.

## Project Structure

```
multi_level_architecture
├── frontend
│   ├── client.py          # Frontend client implementation
├── backend
│   ├── server.py          # Backend server entry point
│   ├── handlers
│   │   ├── data_query_handler.py  # Handles data query requests
│   │   └── data_update_handler.py  # Handles data update requests
├── database
│   ├── db.py              # Database connection and interaction logic
│   └── data
│       └── sample_data.json  # Sample data for the application
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Components

### Frontend
The frontend is implemented in `client.py`, which handles user input and sends requests to the backend server. It displays responses from the server, allowing users to interact with the application.

### Backend
The backend is implemented in `server.py`, which sets up a web server to listen for incoming requests. It routes requests to the appropriate handler based on the request type. The handlers are located in the `handlers` directory:
- `data_query_handler.py`: Processes data query requests and retrieves information from the database.
- `data_update_handler.py`: Processes data update requests and modifies the database accordingly.

### Database
The database logic is contained in `db.py`, which manages connections and interactions with the data stored in `sample_data.json`. This file serves as the initial dataset for the application.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd multi_level_architecture
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```
   python backend/server.py
   ```

4. In a separate terminal, run the frontend client:
   ```
   python frontend/client.py
   ```

## Usage Examples

- To query data, follow the prompts in the frontend client to send a request to the backend.
- To update data, provide the necessary information as prompted by the frontend client.

## Overview of the Architecture
This project demonstrates a simple multi-level architecture where the frontend communicates with the backend, which in turn interacts with the database. This separation of concerns allows for better organization and scalability of the application.