import mysql.connector
import hashlib
from db_tree import TreeNode

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="test",  # Update with your actual password
            database="dsa"  # Update with your actual database name
        )
        self.cursor = self.db.cursor()

    def drop_tables(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS employee")
            self.cursor.execute("DROP TABLE IF EXISTS manager")
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_tables(self):
        try:
            # Create the manager table first
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS manager (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    username VARCHAR(100) UNIQUE,
                    password VARCHAR(64),
                    company VARCHAR(64)
                )
            """)

            # Create the employee table with a foreign key reference to the manager table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    username VARCHAR(100) UNIQUE,
                    password VARCHAR(64),
                    company VARCHAR(64),
                    manager_id INT,
                    FOREIGN KEY (manager_id) REFERENCES manager(id)
                )
            """)
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def company_exists(self, company_name):
        query = "SELECT COUNT(*) FROM manager WHERE company = %s"
        self.cursor.execute(query, (company_name,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def employee_id_exists(self, user_id):
        query = "SELECT COUNT(*) FROM employee WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def manager_id_exists(self, user_id):
        query = "SELECT COUNT(*) FROM manager WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def add_user(self, user_id, full_name, username, password, company, role, manager_id=None):
        hashed_password = hash_password(password)
        try:
            if role == "manager":
                # Add manager to the database
                self.cursor.execute(
                    "INSERT INTO manager (id, name, username, password, company) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, full_name, username, hashed_password, company)
                )
            else:  # Assuming the role is "employee"
                # Add employee to the database
                self.cursor.execute(
                    "INSERT INTO employee (id, name, username, password, company, manager_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (user_id, full_name, username, hashed_password, company, manager_id)
                )
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def authenticate_user(self, username, password, role):
        query = f"SELECT password FROM {role} WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result and check_password(result[0], password):
            return True
        return False
    
    def get_company(self, username, role):
        if role == "Employee":
            self.cursor.execute("SELECT company FROM employee WHERE username = %s", (username,))
            company = self.cursor.fetchone()
            return company
        
        elif role == "Manager":
            self.cursor.execute("SELECT company FROM manager WHERE username = %s", (username,))
            company = self.cursor.fetchone()
            return company
            
    def get_emp_mngrs(self, username, role):
        if role == "Employee":
            # Get the manager ID for the given employee username
            self.cursor.execute("SELECT manager_id FROM employee WHERE username = %s", (username,))
            manager_id = self.cursor.fetchone()
            
            if manager_id:
                manager_id = manager_id[0]  # Extract the ID from the tuple
                
                # Get the manager's name
                self.cursor.execute("SELECT name FROM manager WHERE id = %s", (manager_id,))
                manager_name = self.cursor.fetchone()[0]  # Extract the name
                
                # Get all employees under this manager
                self.cursor.execute("SELECT * FROM employee WHERE manager_id = %s", (manager_id,))
                results = self.cursor.fetchall()
                
                # Extract employee names and build the employee tree
                employee_names = [result[1] for result in results]
                employees = self.build_emp_tree(manager_name, employee_names)
                return [employees]
        
        elif role == "Manager":
            # Get the manager's name and ID for the given username
            self.cursor.execute("SELECT name FROM manager WHERE username = %s", (username,))
            manager_name = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT id FROM manager WHERE username = %s", (username,))
            manager_id = self.cursor.fetchone()[0]
            
            # Get the company the manager belongs to
            self.cursor.execute("SELECT company FROM manager WHERE username = %s", (username,))
            company = self.cursor.fetchone()[0]
            
            # Get all managers in the same company
            self.cursor.execute("SELECT * FROM manager WHERE company=%s", (company,))
            mngrs = self.cursor.fetchall()
            
            # Extract manager names and build the manager tree
            mngr_names = [mngr[1] for mngr in mngrs]
            managers = self.build_mngr_tree(company, mngr_names)
            
            # Get all employees under this manager
            self.cursor.execute("SELECT * FROM employee WHERE manager_id = %s", (manager_id,))
            results = self.cursor.fetchall()
            
            # Extract employee names and build the employee tree
            emp_names = [result[1] for result in results]
            employees = self.build_emp_tree(manager_name, emp_names)
            
            return [employees, managers]

    def build_mngr_tree(self, company, mngr_names):
        root = TreeNode(company)
        for mngr_name in mngr_names:
            mngr = TreeNode(mngr_name)
            root.add_child(mngr)
        
        managers = []
        for child in root.children:
            managers.append(child.data)
            
        return managers
        
    def build_emp_tree(self, manager_name, names):
        root = TreeNode(manager_name)
        for name in names:
            emp = TreeNode(name)
            root.add_child(emp)
        
        employees = []
        for child in root.children:
            employees.append(child.data)
            
        return employees
            
    def get_managers(self):
        query = "SELECT * FROM manager"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        names = [result[1] for result in results]
        companies = [result[4] for result in results]
        return names, companies

def hash_password(password):
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return sha256_hash

def check_password(stored_password, provided_password):
    provided_hash = hash_password(provided_password)
    return stored_password == provided_hash
