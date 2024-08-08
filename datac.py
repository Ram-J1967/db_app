import mysql.connector
import hashlib
from employee_treec import TreeNode

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="toor",  # Update with your actual password
            database="newname"  # Update with your actual database name
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
    
    def get_employees(self, username, role):
        if role == "Employee":
            query = "SELECT manager_id FROM employee WHERE username = %s"
            self.cursor.execute(query, (username,))
            manager_id = self.cursor.fetchone()
            
            query = "SELECT name FROM manager WHERE id = %s"
            self.cursor.execute(query, (manager_id,))
            manager_name = self.cursor.fetchone()
        elif role == "Manager":
            query = "SELECT name FROM manager WHERE username = %s"
            self.cursor.execute(query, (username,))
            manager_name = self.cursor.fetchone()
            
            query = "SELECT id FROM manager WHERE username = %s"
            self.cursor.execute(query, (username,))
            manager_id = self.cursor.fetchone()
            
        
        query = "SELECT * FROM employee where manager_id = %s"
        self.cursor.execute(query, (manager_id))
        results = self.cursor.fetchall()
        names = [result[1] for result in results]
        self.build_tree(manager_name, names)
        return names
    
    def build_tree(self, manager_name, names):
        root = TreeNode(manager_name)
        for name in names:
            emp = TreeNode(name)
            root.add_child(emp)

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
