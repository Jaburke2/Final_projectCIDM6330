CIDM 6330 Final Project.

This project is a rudimentary application that will allow Social work organizations to connect to their client base in a given geographic location. The goal of this application is to serve as a database for different organizations to submit what services they can provide at a given time, to whom, and how the client can get in contact with them. On the flip side however, it also serves a a portal for which clients in need can log in and see what services are available to them for a given need.

## Features

- **Service Creation**: Users can create new social service entries by specifying the service name, social service type, and quantity.
- **Service Allocation**: Users can allocate social services to specific clients by providing the client ID, service name, and social service type.
- **Batch Quantity Change**: Users can change the quantity of social services in a batch by specifying the service name and the new quantity.
- **Event Handling**: The application supports event-driven architecture, where events such as service allocation and deallocation trigger corresponding actions and updates.
- **Integration with External Systems**: The application integrates with external systems, allowing seamless communication with social work organizations and government agencies.
- **Message Bus**: The application utilizes a message bus to facilitate communication and coordination between components, enabling loose coupling and scalability.
- **Data Persistence**: The application uses an SQLite database to persist social service and client information.

## Technology used: 

- Python
- SQLAlchemy (Object-Relational Mapping)
- Redis (External Message Bus)
- SQLite (Database)
- Flask (Web Framework)

## Usage

1. Start the application: `python main.py`
2. Access the application through the provided command-line interface.
3. Use the available actions (`create`, `allocate`, `change_qty`, `quit`) to interact with the application.
4. Follow the prompts and provide the required information for each action.

## Testing

To run the unit tests for the application, execute the following command:


## Notes
- This application is not finished and is need of Unit tests, integration tests, and End to End tests. Also There is still considerable work to be done as far as making it useful for an everyday user and bugs to be flushed out as far as changing the quantiy of a service that an organization can provide. 
