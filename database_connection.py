import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def connect_to_database():
    """
    Connect to MySQL database using credentials from .env file
    """
    try:
        # Get credentials from environment variables
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        
        # Default connection parameters (you can add these to .env if needed)
        host = os.getenv('HOST', 'localhost')  # defaults to localhost
        database = os.getenv('DATABASE', '')   # defaults to no specific database
        port = os.getenv('PORT', 3306)        # defaults to MySQL default port
        
        print(f"Attempting to connect to database with user: {user}")
        print(f"Host: {host}, Port: {port}, Database: {database}")
        
        # Create connection without specifying database first
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            
            # Get server info
            db_info = connection.get_server_info()
            print(f"MySQL Server version: {db_info}")
            
            return connection
            
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database_and_table(connection, db_name="employee_db"):
    """
    Create database and employees table
    """
    try:
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists")
        
        # Use the database
        cursor.execute(f"USE {db_name}")
        print(f"Using database '{db_name}'")
        
        # SQL to create employees table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary DECIMAL(10, 2) NOT NULL,
            age INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        print("Employees table created successfully")
        
        return db_name
        
    except mysql.connector.Error as e:
        print(f"Error creating database or table: {e}")
        return None

def insert_sample_data(connection, employees_data):
    """
    Insert sample employee data into the database
    """
    try:
        cursor = connection.cursor()
        
        # Prepare insert query
        insert_query = """
        INSERT INTO employees (name, salary, age) VALUES (%s, %s, %s)
        """
        
        # Insert each employee
        for emp in employees_data:
            cursor.execute(insert_query, (emp.name, emp.salary, emp.age))
        
        connection.commit()
        print(f"Successfully inserted {len(employees_data)} employees into database")
        
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")

def test_connection():
    """
    Test the database connection with sample operations
    """
    # Connect to the database
    db_connection = connect_to_database()
    
    if db_connection:
        # Create database and table
        db_name = create_database_and_table(db_connection)
        
        if db_name:
            # Switch to the new database
            db_connection.database = db_name
            print(f"Switched to database: {db_name}")
        
        # Close the connection
        db_connection.close()
        print("MySQL connection closed")
        
        return True
    else:
        print("Failed to connect to database. Please ensure:")
        print("1. MySQL server is running")
        print("2. Credentials in .env file are correct")
        print("3. Host and port are accessible")
        return False

if __name__ == "__main__":
    test_connection()