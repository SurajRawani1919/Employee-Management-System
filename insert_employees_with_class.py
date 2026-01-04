import mysql.connector
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

class Employee:
    """
    Employee class to represent employee data with methods for calculations
    """
    def __init__(self, emp_id, name, salary, age):
        self.id = emp_id
        self.name = name
        self.salary = int(salary)  # Convert to int for calculations
        self.age = int(age)        # Convert to int
        
    def yearly_salary(self):
        """Calculate yearly salary (monthly salary * 12)"""
        return self.salary * 12
        
    def promotion(self):
        """Calculate promoted salary (current salary * 1.10)"""
        return self.salary * 1.10
    
    def __str__(self):
        return f"Employee(id={self.id}, name='{self.name}', salary={self.salary}, age={self.age})"

def load_employees_from_json(json_file):
    """
    Load employee data from JSON file and convert to Employee objects
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract the employee list from the 'data' key
    employees_json = data.get('data', [])
    
    # Convert JSON data to Employee objects
    employees = []
    for emp_data in employees_json:
        employee = Employee(
            emp_id=emp_data['id'],
            name=emp_data['employee_name'],
            salary=emp_data['employee_salary'],
            age=emp_data['employee_age']
        )
        employees.append(employee)
    
    return employees

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

def insert_employees_to_db(employees):
    """
    Insert employee data into the database using computed yearly salary from class method
    """
    connection = connect_to_database()
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Prepare insert query
            insert_query = """
            INSERT INTO employees (name, monthly_salary, age, yearly_salary) 
            VALUES (%s, %s, %s, %s)
            """
            
            successful_inserts = 0
            
            for emp in employees:
                # Compute yearly salary using the class method
                yearly_sal = emp.yearly_salary()
                
                # Insert the employee data
                cursor.execute(insert_query, (emp.name, emp.salary, emp.age, yearly_sal))
                successful_inserts += 1
            
            connection.commit()
            print(f"Successfully inserted {successful_inserts} employees into the database")
            print(f"Yearly salaries computed using the Employee.yearly_salary() method")
            
        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
        
        connection.close()
        return True
    else:
        return False

def clear_employees_table():
    """
    Clear all records from the employees table
    """
    connection = connect_to_database()
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Clear the table
            cursor.execute("DELETE FROM employees;")
            connection.commit()
            print("Cleared all records from employees table")
            
        except mysql.connector.Error as e:
            print(f"Error clearing table: {e}")
        
        connection.close()

def main():
    """
    Main function to load employees from JSON, compute yearly salary using class method, and insert to DB
    """
    print("Loading employees from JSON file...")
    employees = load_employees_from_json('employees.json')
    
    print(f"Loaded {len(employees)} employees")
    print(f"Sample employee: {employees[0] if employees else 'No employees'}")
    print(f"Sample yearly salary (computed using class method): {employees[0].yearly_salary() if employees else 'N/A'}")
    
    # Clear the existing data in the table
    print("\nClearing existing data from employees table...")
    clear_employees_table()
    
    # Insert the employee data into the database
    print("\nInserting employee data into database...")
    success = insert_employees_to_db(employees)
    
    if success:
        print("\nSuccessfully inserted all employees with computed yearly salaries!")
        
        # Verify by checking the count
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees;")
            count = cursor.fetchone()[0]
            print(f"Total employees in database after insertion: {count}")
            connection.close()
    else:
        print("\nFailed to insert employees into database")

if __name__ == "__main__":
    main()