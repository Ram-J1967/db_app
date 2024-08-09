import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from datac import Database, hash_password, check_password

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ORGANIZATION LOG IN SYSTEM")
        self.geometry("800x500")

        self.db = Database()  # Initialize the database
        self.db.create_tables()  # Create tables when the app starts

        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.role_var = ctk.StringVar(value="Employee")  # Default to Employee
        self.create_main_frame()

    def create_main_frame(self):
        if hasattr(self, "success_frame"):
            self.success_frame.destroy()
            
        self.main_frame = ctk.CTkFrame(self, width=600, height=400)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label = ctk.CTkLabel(self.main_frame, text="WELCOME", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=1, columnspan=2, pady=100, padx=300)

        self.employee_button = ctk.CTkButton(self.main_frame, text="Employee Login", command=self.show_employee_login)
        self.employee_button.grid(row=0, column=0, padx=20, pady=10)

        self.manager_button = ctk.CTkButton(self.main_frame, text="Manager Login", command=self.show_manager_login)
        self.manager_button.grid(row=1, column=0, padx=20, pady=10)

        self.signup_button = ctk.CTkButton(self.main_frame, text="Sign Up", command=self.show_signup_form)
        self.signup_button.grid(row=2, column=0, padx=20, pady=10)

    def create_login_frame(self, login_type):
        if hasattr(self, 'login_frame'):
            self.login_frame.destroy()

        self.login_frame = ctk.CTkFrame(self, width=600, height=400)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        self.label = ctk.CTkLabel(self.login_frame, text=f"{login_type} Login", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.username_label = ctk.CTkLabel(self.login_frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=20, pady=10)
        self.username_entry = ctk.CTkEntry(self.login_frame, textvariable=self.username_var)
        self.username_entry.grid(row=1, column=1, padx=20, pady=10)

        self.password_label = ctk.CTkLabel(self.login_frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=20, pady=10)
        self.password_entry = ctk.CTkEntry(self.login_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=2, column=1, padx=20, pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.back_button = ctk.CTkButton(self.login_frame, text="Back", command=self.show_main_frame)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_signup_frame(self):
        if hasattr(self, 'signup_frame'):
            self.signup_frame.destroy()

        self.signup_frame = ctk.CTkFrame(self, width=600, height=400)
        self.signup_frame.grid(row=0, column=0, sticky="nsew")

        self.label = ctk.CTkLabel(self.signup_frame, text="Sign Up", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.id_label = ctk.CTkLabel(self.signup_frame, text="ID:")
        self.id_label.grid(row=1, column=0, padx=20, pady=10)
        self.id_entry = ctk.CTkEntry(self.signup_frame)
        self.id_entry.grid(row=1, column=1, padx=20, pady=10)

        self.first_name_label = ctk.CTkLabel(self.signup_frame, text="First Name:")
        self.first_name_label.grid(row=2, column=0, padx=20, pady=10)
        self.first_name_entry = ctk.CTkEntry(self.signup_frame)
        self.first_name_entry.grid(row=2, column=1, padx=20, pady=10)

        self.last_name_label = ctk.CTkLabel(self.signup_frame, text="Last Name:")
        self.last_name_label.grid(row=3, column=0, padx=20, pady=10)
        self.last_name_entry = ctk.CTkEntry(self.signup_frame)
        self.last_name_entry.grid(row=3, column=1, padx=20, pady=10)

        self.username_label = ctk.CTkLabel(self.signup_frame, text="Username:")
        self.username_label.grid(row=4, column=0, padx=20, pady=10)
        self.username_entry = ctk.CTkEntry(self.signup_frame)
        self.username_entry.grid(row=4, column=1, padx=20, pady=10)

        self.password_label = ctk.CTkLabel(self.signup_frame, text="Password:")
        self.password_label.grid(row=5, column=0, padx=20, pady=10)
        self.password_entry = ctk.CTkEntry(self.signup_frame, show="*")
        self.password_entry.grid(row=5, column=1, padx=20, pady=10)

        self.role_label = ctk.CTkLabel(self.signup_frame, text="Role (Employee/Manager):")
        self.role_label.grid(row=6, column=0, padx=20, pady=10)
        self.role_menu = ctk.CTkOptionMenu(self.signup_frame, values=["Manager", "Employee"], command=self.role_selected)
        self.role_menu.grid(row=6, column=1, padx=20, pady=10)

        self.company_label = ctk.CTkLabel(self.signup_frame, text="Company:")
        self.company_entry = ctk.CTkEntry(self.signup_frame)

        self.manager_id_label = ctk.CTkLabel(self.signup_frame, text="Manager ID:")
        self.manager_id_entry = ctk.CTkEntry(self.signup_frame)

        self.signup_button = ctk.CTkButton(self.signup_frame, text="Sign Up", command=self.signup)
        self.signup_button.grid(row=9, column=0, pady=10)

        self.back_button = ctk.CTkButton(self.signup_frame, text="Back", command=self.show_main_frame)
        self.back_button.grid(row=9, column=1, pady=10)

        self.role_selected(self.role_menu.get())  # To initialize the form based on default role selection

    def role_selected(self, role):
        # Clear existing fields in the signup frame
        self.company_label.grid_forget()
        self.company_entry.grid_forget()
        self.manager_id_label.grid_forget()
        self.manager_id_entry.grid_forget()

        if role == "Manager":
            self.company_label.grid(row=7, column=0, padx=20, pady=10)
            self.company_entry.grid(row=7, column=1, padx=20, pady=10)
        elif role == "Employee":
            self.manager_id_label.grid(row=7, column=0, padx=20, pady=10)
            self.manager_id_entry.grid(row=7, column=1, padx=20, pady=10)
            self.company_label.grid(row=8, column=0, padx=20, pady=10)
            self.company_entry.grid(row=8, column=1, padx=20, pady=10)

    def show_success_page(self, role, username):
        if hasattr(self, 'success_frame'):
            self.success_frame.destroy()
            
        if not hasattr(self, 'success_frame'):
            self.success_frame = self.success_frame = ctk.CTkFrame(self, width=600, height=400)
            self.success_frame.grid(row=0, column=0, sticky="nsew")

        self.success_frame = ctk.CTkFrame(self, width=600, height=400)
        self.success_frame.grid(row=0, column=0, sticky="nsew")
        
        if not hasattr(self, 'dashboard_frame'):
            self.dashboard_frame = ctk.CTkFrame(self, width=600, height=400)

        success_label = ctk.CTkLabel(self.success_frame, text=f"Successfully logged in as {role}", font=ctk.CTkFont(size=20, weight="bold"))
        success_label.pack(pady=10)

        self.dashboard_button = ctk.CTkButton(self.success_frame, text="Go to Dashboard", command=lambda: self.show_dashboard(role, username))
        self.dashboard_button.pack(pady=10)
        
        self.logout_button = ctk.CTkButton(self.success_frame, text="Logout", command=self.create_main_frame)
        self.logout_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.dashboard_frame, text="Back", command=lambda: self.show_success_page(role, username))
        self.back_button.pack(pady=10)

    def show_dashboard(self, role, username):
        if hasattr(self, 'success_frame'):
            self.success_frame.destroy()

        self.dashboard_frame = ctk.CTkFrame(self, width=600, height=400)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        
        company = self.db.get_company(username, role)
        self.label = ctk.CTkLabel(self.dashboard_frame, text=f"{role.capitalize()} Dashboard\n{company[0]}", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=10)

        self.mngr_tree = tk.Listbox(self.dashboard_frame)
        
        self.emp_tree = tk.Listbox(self.dashboard_frame)

        self.load_users(username, role)

        self.back_button = ctk.CTkButton(self.dashboard_frame, text="Back", command=lambda: self.show_success_page(role, username))
        self.back_button.pack(pady=10)
    
    def load_users(self, username, role):
        results = self.db.get_emp_mngrs(username, role)
        
        if role == "Employee" and results:
            self.emp_tree.pack(pady=10, fill="both", expand=True)
            self.emp_tree.insert(tk.END, "EMPLOYEES:")
            for employee in results[0]:
                self.emp_tree.insert(tk.END, employee)
        
        elif role == "Manager" and len(results) == 2:
            self.mngr_tree.pack(pady=10, fill="both", expand=True)
            self.emp_tree.pack(pady=10, fill="both", expand=True)
            
            employees, managers = results
            self.mngr_tree.insert(tk.END, "MANAGERS:")
            for manager in managers:
                self.mngr_tree.insert(tk.END, manager)
            
            self.emp_tree.insert(tk.END, "EMPLOYEES:")
            for employee in employees:
                self.emp_tree.insert(tk.END, employee)

    def show_main_frame(self):
        if hasattr(self, 'login_frame'):
            self.login_frame.destroy()
        if hasattr(self, 'signup_frame'):
            self.signup_frame.destroy()
        if hasattr(self, 'success_frame'):
            self.success_frame.destroy()
        if hasattr(self, 'dashboard_frame'):
            self.dashboard_frame.destroy()
        self.create_main_frame()

    def show_employee_login(self):
        self.create_login_frame("Employee")

    def show_manager_login(self):
        self.create_login_frame("Manager")

    def show_signup_form(self):
        self.create_signup_frame()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        login_type = "manager" if "Manager" in self.login_frame.winfo_children()[0].cget("text") else "employee"

        if login_type == "manager":
            self.manager_login(username, password)
        else:
            self.employee_login(username, password)

    def employee_login(self, username, password):
        if self.db.authenticate_user(username, password, "employee"):
            self.show_success_page("Employee", username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def manager_login(self, username, password):
        if self.db.authenticate_user(username, password, "manager"):
            self.show_success_page("Manager", username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        user_id = self.id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        company = self.company_entry.get()
        role = self.role_menu.get().lower()
        manager_id = None  # Initialize manager_id to None

        if not user_id or not first_name or not last_name or not username or not password or not company or not role:
            messagebox.showerror("Sign Up Failed", "All fields are required")
            return

        if role not in ["employee", "manager"]:
            messagebox.showerror("Sign Up Failed", "Invalid role. Please enter 'employee' or 'manager'")
            return

        if (role == "employee" and self.db.employee_id_exists(user_id)) or (role == "manager" and self.db.manager_id_exists(user_id)):
            messagebox.showerror("Sign Up Failed", "ID already exists")
            return

        if role == "employee":
            manager_id = self.manager_id_entry.get()
            if not manager_id or not self.db.manager_id_exists(manager_id):
                messagebox.showerror("Sign Up Failed", "Manager ID does not exist")
                return

            if not self.db.company_exists(company):
                messagebox.showerror("Sign Up Failed", "Company name does not exist")
                return

        full_name = f"{first_name} {last_name}"
        if self.db.add_user(user_id, full_name, username, password, company, role, manager_id):
            messagebox.showinfo("Success", f"Successfully signed up as {role.capitalize()}")
            self.show_main_frame()
        else:
            messagebox.showerror("Sign Up Failed", "Username already exists")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
