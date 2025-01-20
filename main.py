from datetime import datetime
import os

class LicensePlate:
    def __init__(self, plate_id, number, price, status="available"):
        self.id = plate_id
        self.number = number
        self.price = price
        self.status = status

    def update_price(self, new_price):
        self.price = new_price

    def mark_as_sold(self):
        self.status = "sold"

    def is_available(self):
        return self.status == "available"
    
    def __str__(self):
        return f"ID: {self.id}, Number: {self.number}, Price: ${self.price}, Status: {self.status}"


class User:
    def __init__(self, user_id, name, address):
        self.id = user_id
        self.name = name
        self.address = address
        self.purchased_plates = []

    def add_purchase(self, license_plate):
        self.purchased_plates.append(license_plate)

    def get_purchase_history(self):
        return self.purchased_plates


class Sales:
    def __init__(self, sale_id, license_plate, user, date=None):
        self.id = sale_id
        self.license_plate = license_plate
        self.user = user
        self.date = date or datetime.now()

    def get_sale_details(self):
        return {
            "sale_id": self.id,
            "license_plate": self.license_plate.number,
            "user": self.user.name,
            "date": self.date
        }


class LicensePlateManager:
    def __init__(self):
        self.plates = []

    def add_plate(self, plate):
        self.plates.append(plate)

    def delete_plate(self, plate_id):
        self.plates = [p for p in self.plates if p.id != plate_id]

    def edit_plate(self, plate_id, **kwargs):
        for plate in self.plates:
            if plate.id == plate_id:
                plate.number = kwargs.get("number", plate.number)
                plate.price = kwargs.get("price", plate.price)
                plate.status = kwargs.get("status", plate.status)
                break

    def list_available_plates(self):
        return [plate for plate in self.plates if plate.is_available()]


class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def find_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def list_all_users(self):
        return self.users


class SalesManager:
    def __init__(self):
        self.sales_records = []

    def record_sale(self, license_plate, user):
        sale_id = len(self.sales_records) + 1
        sale = Sales(sale_id, license_plate, user)
        self.sales_records.append(sale)
        return sale

    def get_sales_statistics(self):
        total_sales = len(self.sales_records)
        total_revenue = sum(sale.license_plate.price for sale in self.sales_records)
        return {
            "total_sales": total_sales,
            "total_revenue": total_revenue
        }

    def get_sales_by_user(self, user_id):
        return [
            sale for sale in self.sales_records
            if sale.user.id == user_id
        ]
        

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    

def main_menu():
    while True:
        clear_screen()
        print("===== License Plate Sales System =====")
        print("1. My Profile")
        print("2. Register")
        print("3. Create New User")
        print("4. Users List")
        print("5. View all license plates")
        print("6. Add a new license plate")
        print("7. Edit a license plate")
        print("8. Delete a license plate")
        print("9. Record a sale")
        print("10. View sales statistics")
        print("11 or q. Exit")
        print("======================================")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            my_profile()
        elif choice == "2":
            register()
        elif choice == "3":
            create_new_user()
        elif choice == "4":
            users_list()
        elif choice == "5":
            view_license_plates()
        elif choice == "6":
            add_license_plate()
        elif choice == "7":
            edit_license_plate()
        elif choice == "8":
            delete_license_plate()
        elif choice == "9":
            record_sale()
        elif choice == "10":
            view_sales_statistics()
        elif choice == "11" or choice == "q":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")


plate_manager = LicensePlateManager()
user_manager = UserManager()
sales_manager = SalesManager()

current_user = None

def my_profile():
    global current_user
    clear_screen()
    if not current_user:
        print("You are not registered. Please register first.")
        input("\nPress Enter to return to the main menu...")
        return

    print("===== My Profile =====")
    print(f"User ID: {current_user.id}")
    print(f"Name: {current_user.name}")
    print(f"Address: {current_user.address}")
    print("======================")
    print("1. Update Profile")
    print("2. Back to Main Menu")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        name = input(f"Enter new name ({current_user.name}): ").strip() or current_user.name
        address = input(f"Enter new address ({current_user.address}): ").strip() or current_user.address
        current_user.name = name
        current_user.address = address
        print("Profile updated successfully!")
    input("\nPress Enter to return to the main menu...")

def register():
    global current_user
    clear_screen()
    if current_user:
        print("You are already registered!")
        input("\nPress Enter to return to the main menu...")
        return

    print("====== Register =====")
    user_id = input("Enter your User ID: ").strip()
    name = input("Enter your Name: ").strip()
    address = input("Enter your Address: ").strip()
    current_user = User(user_id, name, address)
    user_manager.add_user(current_user)
    print("Registration successful!")
    input("\nPress Enter to return to the main menu...")


def create_new_user():
    clear_screen()
    print("====== Create New User =====")
    user_id = input("Enter User ID: ").strip()
    name = input("Enter Name: ").strip()
    address = input("Enter Address: ").strip()
    user = User(user_id, name, address)
    user_manager.add_user(user)
    print("User created successfully!")
    input("\nPress Enter to return to the main menu...")


def users_list():
    clear_screen()
    print("===== Users List ======")
    users = user_manager.list_all_users()
    if not users:
        print("No users available.")
    else:
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Address: {user.address}")
    input("\nPress Enter to return to the main menu...")


def view_license_plates():
    clear_screen()
    plates = plate_manager.plates
    if not plates:
        print("No license plates available yet.")
    else:
        print("Available License Plates:")
        for plate in plates:
            print(str(plate))
            
    input("\nPress Enter to return to the main menu...")
    

def add_license_plate():
    clear_screen()
    print("Add New License Plate")
    plate_id = input("Enter Plate ID: ").strip()
    number = input("Enter Plate Number: ").strip()
    price = float(input("Enter Price: ").strip())
    plate = LicensePlate(plate_id, number, price)
    plate_manager.add_plate(plate)
    print("License Plate added successfully!")
    input("\nPress Enter to return to the main menu...")

def edit_license_plate():
    clear_screen()
    print("Edit License Plate")
    plate_id = input("Enter Plate ID to edit: ").strip()
    plate = next((p for p in plate_manager.plates if p.id == plate_id), None)
    if plate:
        print(f"Editing Plate: {plate.number}")
        number = input(f"Enter new number ({plate.number}): ").strip() or plate.number
        price = input(f"Enter new price ({plate.price}): ").strip()
        status = input(f"Enter new status ({plate.status}): ").strip()
        plate_manager.edit_plate(
            plate_id, number=number, price=float(price or plate.price), status=status or plate.status
        )
        print("License Plate updated successfully!")
    else:
        print("Plate not found!")
    input("\nPress Enter to return to the main menu...")


def delete_license_plate():
    clear_screen()
    print("Delete License Plate")
    plate_id = input("Enter Plate ID to delete: ").strip()
    plate_manager.delete_plate(plate_id)
    print("License Plate deleted successfully!")
    input("\nPress Enter to return to the main menu...")


def record_sale():
    clear_screen()
    print("===== Record a Sale =====")
    plate_id = input("Enter Plate ID: ").strip()
    plate = next((p for p in plate_manager.plates if p.id == plate_id), None)

    if not plate:
        print("Plate does not exist!")
        input("\nPress Enter to return to the main menu...")
        return

    if not plate.is_available():
        print("Plate is not available!")
        input("\nPress Enter to return to the main menu...")
        return

    print("\nWho is buying this plate?")
    print("1. Buy for myself")
    print("2. Buy for an existing user")
    print("3. Create a new user and buy for them")
    choice = input("Enter your choice: ").strip()

    if choice == "1":  # Buy for the current user
        if not current_user:
            print("You must be registered to buy for yourself!")
            input("\nPress Enter to return to the main menu...")
            return
        buyer = current_user

    elif choice == "2":  # Buy for an existing user
        user_id = input("Enter the existing User ID: ").strip()
        buyer = user_manager.find_user_by_id(user_id)
        if not buyer:
            print("User not found!")
            input("\nPress Enter to return to the main menu...")
            return

    elif choice == "3":  # Create a new user and buy for them
        user_id = input("Enter new User ID: ").strip()
        name = input("Enter new User Name: ").strip()
        address = input("Enter new User Address: ").strip()
        buyer = User(user_id, name, address)
        user_manager.add_user(buyer)
        print("New user created successfully!")

    else:
        print("Invalid choice!")
        input("\nPress Enter to return to the main menu...")
        return

    # Record the sale
    sale = sales_manager.record_sale(plate, buyer)
    plate.mark_as_sold()
    buyer.add_purchase(plate)

    print(f"Sale recorded successfully! Sale ID: {sale.id}")
    input("\nPress Enter to return to the main menu...")


def view_sales_statistics():
    clear_screen()
    print("Sales Statistics")
    stats = sales_manager.get_sales_statistics()
    print(f"Total Sales: {stats['total_sales']}")
    print(f"Total Revenue: ${stats['total_revenue']}")
    input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main_menu()
