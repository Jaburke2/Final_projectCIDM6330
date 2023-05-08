import sys
from SocialService.domain import commands
from SocialService.services import handlers, unit_of_work
from SocialService.adapters.database import create_session_factory, get_session

# Create a session factory for the SQLite database
session_factory = create_session_factory()

# Create a unit of work that uses the SQLAlchemy session
uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)

def main():
    while True:
        action = input("Enter the action (create, allocate, change_qty, quit): ").lower()
        if action == 'create':
            service_name = input("Enter the service name: ")
            social_service_type = input("Enter the social service type: ")
            qty = int(input("Enter the quantity: "))
            cmd = commands.CreateService(service_name, social_service_type, qty)
            handlers.add_service(cmd, uow)
            print("Service created successfully.")
        elif action == 'allocate':
            client_id = int(input("Enter the client ID: "))
            service_name = input("Enter the service name: ")
            social_service_type = input("Enter the social service type: ")
            cmd = commands.AllocateService(client_id, service_name, social_service_type)
            handlers.allocate(cmd, uow)
            print("Service allocated successfully.")
        elif action == 'change_qty':
            service_name = input("Enter the service name: ")
            qty = int(input("Enter the new quantity: "))
            cmd = commands.ChangeBatchQuantity(service_name, qty)
            handlers.change_batch_quantity(cmd, uow)
            print("Batch quantity changed successfully.")
        elif action == 'quit':
            print("Exiting the application.")
            sys.exit()
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()
