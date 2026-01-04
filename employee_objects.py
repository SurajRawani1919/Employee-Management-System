import json

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

# Load employees from the JSON file
employees = load_employees_from_json('employees.json')

# Display some information about the employees
print(f"Loaded {len(employees)} employees from JSON data")
print()

# Display information for the first few employees
for i, emp in enumerate(employees[:5]):  # Show first 5 employees
    print(f"Employee {i+1}:")
    print(f"  {emp}")
    print(f"  Yearly Salary: {emp.yearly_salary()}")
    print(f"  Promoted Salary: {emp.promotion():.2f}")
    print()

# Example of accessing specific employee
if employees:
    first_employee = employees[0]
    print(f"First employee: {first_employee.name}")
    print(f"Yearly salary: {first_employee.yearly_salary()}")
    print(f"Promoted salary: {first_employee.promotion():.2f}")