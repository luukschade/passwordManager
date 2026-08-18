accounts = {
}


def add_password(service, username, password):
    if not accounts:
        accounts[1] = {"Service": service, "Username": username, "Password": password}
    else:
        accounts[max(accounts) + 1] = {"Service": service, "Username": username, "Password": password}


def ask_password_data():
    service = input("Which service: ")
    username = input("What is your username: ")
    password = input("What is your password: ")
    return service, username, password

def delete_password(del_password_id):
    if del_password_id in accounts:
        del accounts[del_password_id]
    else:
        print("That is not a valid ID!")

def show_passwords():
    for account_id, info in accounts.items():
        print(f"Account ID: {account_id}")
        print(f"Service: {info['Service']}")
        print(f"Username: {info['Username']}")
        print(f"Password: {info['Password']}")

def edit_password(edit_password_id):
    while True:
        print("1. Service")
        print("2. Username")
        print("3. Password")
        print("4. Quit")
        edit_password_choice = input("What do you want to edit? ")
        if edit_password_choice == "1":
            value_after_edit = input("What do you want the service to change to: ")
            accounts[edit_password_id]["Service"] = value_after_edit
        elif edit_password_choice == "2":
            value_after_edit = input("What do you want the Username to change to: ")
            accounts[edit_password_id]["Username"] = value_after_edit
        elif edit_password_choice == "3":
            value_after_edit = input("What do you want the password to change to: ")
            accounts[edit_password_id]["Password"] = value_after_edit
        elif edit_password_choice == "4":
            return
        else:
            print("That is not a valid choice!")

while True:
    print("---( Password Manager )---")
    print("1. Add password")
    print("2. Show passwords")
    print("3. Delete Password")
    print("4. Edit password")
    print("5. Exit")
    choice = input("\nChoose an option: ")

    if choice == "1":
        service, username, password = ask_password_data()
        add_password(service, username, password)

    elif choice == "2":
        show_passwords()

    elif choice == "3":
        try:
            del_password_id = int(input("The ID of the password you want to delete: "))
            delete_password(del_password_id)
        except ValueError:
            print("That is not a valid ID!")

    elif choice == "4":
        try:
            edit_password_id = int(input("The ID of the password you want to edit: "))
            if edit_password_id in accounts:
                edit_password(edit_password_id)
            else:
                print("That is not a valid ID!")
        except ValueError:
            print("That is not a valid ID!")

    elif choice == "5":
        break
    else:
        print("That is a not a valid option!")