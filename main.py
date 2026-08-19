import sqlite3 as sql

connection = sql.connect("data.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ACCOUNTS (
ID INTEGER NOT NULL PRIMARY KEY,
SERVICE TEXT NOT NULL,
USERNAME TEXT NOT NULL,
PASSWORD TEXT NOT NULL)
''')

connection.commit()


def add_password(service, username, password):
    cursor.execute("""
        INSERT INTO ACCOUNTS (SERVICE, USERNAME, PASSWORD)
        VALUES (?, ?, ?)
    """, (service, username, password))
    connection.commit()

def ask_password_data():
    service = input("Which service: ")
    username = input("What is your username: ")
    password = input("What is your password: ")
    return service, username, password

def delete_password(del_password_id):
    cursor.execute("""
            DELETE FROM ACCOUNTS WHERE ID = ?
        """, (del_password_id,))
    connection.commit()

def show_passwords():
    result = cursor.execute('''
    SELECT * FROM ACCOUNTS
    ''').fetchall()

    for account in result:
        account_id, service, username, password = account
        print(f"ID: {account_id}, Service: {service}, Username: {username}, Password: {password}")

def edit_password(edit_password_id):
    while True:
        print("1. Service")
        print("2. Username")
        print("3. Password")
        print("4. Quit")

        choice = input("What do you want to edit? ")

        if choice == "1":
            column = "SERVICE"
        elif choice == "3":
            column = "PASSWORD"
        elif choice == "4":
            return
        else:
            print("That is not a valid choice!")
            continue

        value = input("What do you want to change it to: ")

        cursor.execute(
            f"UPDATE ACCOUNTS SET {column} = ? WHERE ID = ?",
            (value, edit_password_id)
        )
        connection.commit()

def account_exists(account_id):
    result = cursor.execute(
        "SELECT ID FROM ACCOUNTS WHERE ID = ?",
        (account_id,)
    ).fetchone()
    return result is not None

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
            if account_exists(del_password_id):
                delete_password(del_password_id)
            else:
                print("That is not a valid ID!")
        except ValueError:
            print("That is not a valid ID!")

    elif choice == "4":
        try:
            edit_password_id = int(input("The ID of the password you want to edit: "))
            if account_exists(edit_password_id):
                edit_password(edit_password_id)
            else:
                print("That is not a valid ID!")
        except ValueError:
            print("That is not a valid ID!")

    elif choice == "5":
        break
    else:
        print("That is a not a valid option!")