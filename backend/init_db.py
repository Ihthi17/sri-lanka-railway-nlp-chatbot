import os
from sqlalchemy import text
from database import engine

def initialize_database():
    print("Starting database initialization...")
    
    # Read the schema file
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    if not os.path.exists(schema_path):
        print(f"Error: {schema_path} not found.")
        return

    with open(schema_path, "r") as f:
        sql_commands = f.read().split(";")

    with engine.connect() as connection:
        # Start a transaction
        trans = connection.begin()
        try:
            # Disable foreign key checks for clean re-initialization
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            
            for command in sql_commands:
                command = command.strip()
                if command:
                    print(f"Executing: {command[:50]}...")
                    connection.execute(text(command))
            
            # Re-enable foreign key checks
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            
            trans.commit()

            print("\nDatabase initialized successfully! All tables created and sample data inserted.")
        except Exception as e:
            trans.rollback()
            print(f"\nError during initialization: {e}")

if __name__ == "__main__":
    initialize_database()
