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
        host = os.getenv('HOST', 'localhost')
        database = os.getenv('DATABASE', 'employee_db')
        port = os.getenv('PORT', 3306)
        
        print(f"Connecting to database: {database}")
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
            
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def update_table_structure():
    """
    Drop the old employees table and create a new one with the correct structure
    """
    connection = connect_to_database()
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Drop the old table if it exists
            cursor.execute("DROP TABLE IF EXISTS employees;")
            print("Dropped old employees table if it existed")
            
            # Create the new employees table with the specified structure
            create_table_query = """
            CREATE TABLE employees (
                emp_id INT AUTO_INCREMENT PRIMARY KEY,
                name TEXT NOT NULL,
                monthly_salary DECIMAL(10, 2) NOT NULL,
                age INT NOT NULL,
                yearly_salary DECIMAL(10, 2) NOT NULL
            )
            """
            
            cursor.execute(create_table_query)
            connection.commit()
            print("Created new employees table with correct structure:")
            print("  - emp_id: integer primary key")
            print("  - name: text")
            print("  - monthly_salary: REAL")
            print("  - age: integer")
            print("  - yearly_salary: REAL")
            
            # Insert sample data
            sample_employees = [
                ("Tiger Nixon", 320800.00, 61, 320800.00 * 12),
                ("Garrett Winters", 170750.00, 63, 170750.00 * 12),
                ("Ashton Cox", 86000.00, 66, 86000.00 * 12),
                ("Cedric Kelly", 433060.00, 22, 433060.00 * 12),
                ("Airi Satou", 162700.00, 33, 162700.00 * 12)
            ]
            
            # Insert sample data
            insert_query = """
            INSERT INTO employees (name, monthly_salary, age, yearly_salary) 
            VALUES (%s, %s, %s, %s)
            """
            
            for emp in sample_employees:
                cursor.execute(insert_query, emp)
            
            connection.commit()
            print(f"Successfully inserted {len(sample_employees)} employees into the new table")
            
            # Verify the data
            cursor.execute("SELECT COUNT(*) FROM employees;")
            count = cursor.fetchone()[0]
            print(f"Total records in the new employees table: {count}")
            
        except mysql.connector.Error as e:
            print(f"Error updating table structure: {e}")
        
        connection.close()

if __name__ == "__main__":
    update_table_structure()