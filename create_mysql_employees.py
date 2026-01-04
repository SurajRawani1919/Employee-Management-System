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
        
        # Default connection parameters
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

def create_employee_database_and_table(connection, db_name="employee_db"):
    """
    Create database and employees table with the specified structure
    """
    try:
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists")
        
        # Use the database
        cursor.execute(f"USE {db_name}")
        print(f"Using database '{db_name}'")
        
        # SQL to create employees table with the specified structure
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INT AUTO_INCREMENT PRIMARY KEY,
            name TEXT NOT NULL,
            monthly_salary DECIMAL(10, 2) NOT NULL,
            age INT NOT NULL,
            yearly_salary DECIMAL(10, 2) NOT NULL
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        print("Employees table created successfully with the specified structure:")
        print("  - emp_id: integer primary key")
        print("  - name: text")
        print("  - monthly_salary: REAL")
        print("  - age: integer")
        print("  - yearly_salary: REAL")
        
        return db_name
        
    except mysql.connector.Error as e:
        print(f"Error creating database or table: {e}")
        return None

def insert_sample_data(connection):
    """
    Insert sample employee data into the database
    """
    try:
        cursor = connection.cursor()
        
        # Calculate yearly salary as monthly salary * 12
        sample_employees = [
            ("Tiger Nixon", 320800.00, 61, 320800.00 * 12),
            ("Garrett Winters", 170750.00, 63, 170750.00 * 12),
            ("Ashton Cox", 86000.00, 66, 86000.00 * 12),
            ("Cedric Kelly", 433060.00, 22, 433060.00 * 12),
            ("Airi Satou", 162700.00, 33, 162700.00 * 12)
        ]
        
        # Prepare insert query
        insert_query = """
        INSERT INTO employees (name, monthly_salary, age, yearly_salary) 
        VALUES (%s, %s, %s, %s)
        """
        
        # Insert each employee
        for emp in sample_employees:
            cursor.execute(insert_query, emp)
        
        connection.commit()
        print(f"Successfully inserted {len(sample_employees)} employees into database")
        
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")

def view_employees(connection):
    """
    View all employees in the database
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        
        print("\nCurrent employees in the database:")
        print("ID | Name | Monthly Salary | Age | Yearly Salary")
        print("-" * 50)
        for emp in employees:
            print(f"{emp[0]} | {emp[1]} | {emp[2]} | {emp[3]} | {emp[4]}")
        
    except mysql.connector.Error as e:
        print(f"Error viewing data: {e}")

def main():
    """
    Main function to create database and table
    """
    # Connect to the database
    db_connection = connect_to_database()
    
    if db_connection:
        # Create database and table with specified structure
        db_name = create_employee_database_and_table(db_connection)
        
        if db_name:
            # Switch to the new database
            db_connection.database = db_name
            print(f"Switched to database: {db_name}")
            
            # Insert sample data
            insert_sample_data(db_connection)
            
            # View the inserted data
            view_employees(db_connection)
        
        # Close the connection
        db_connection.close()
        print("\nMySQL connection closed")
        
        return True
    else:
        print("\nFailed to connect to database. Please ensure:")
        print("1. MySQL server is running")
        print("2. Credentials in .env file are correct")
        print("3. Host and port are accessible")
        return False

if __name__ == "__main__":
    main()