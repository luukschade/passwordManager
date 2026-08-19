import sqlite3 as sql
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

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

cursor.execute('''
CREATE TABLE IF NOT EXISTS SETTINGS (
SALT BLOB NOT NULL,
CHECK_VALUE BLOB)
''')
connection.commit()

# Get saved salt
salt_result = cursor.execute("""
SELECT SALT FROM SETTINGS
""").fetchone()

if salt_result is None:
    # Generate salt on first startup
    salt = os.urandom(16)

    cursor.execute("""
        INSERT INTO SETTINGS (SALT)
        VALUES (?)
    """, (salt,))

    connection.commit()

# Load saved salt
salt = cursor.execute("""
    SELECT SALT FROM SETTINGS
""").fetchone()[0]

# Turn master password into bytes
password = input("Master password: ").encode()

# Derive encryption key from password
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=600_000
)

# Generate key
key = kdf.derive(password)

# Convert key to Fernet format
fernet_key = base64.urlsafe_b64encode(key)

# Create encryption/decryption object
cipher = Fernet(fernet_key)

# Get saved password check
check_result = cursor.execute("""
    SELECT CHECK_VALUE FROM SETTINGS
""").fetchone()

if check_result[0] is None:
    # Create check on first startup
    check_value = cipher.encrypt(b"CHECK")

    cursor.execute("""
        UPDATE SETTINGS
        SET CHECK_VALUE = ?
    """, (check_value,))
    connection.commit()
else:
    try:
        # Verify master password
        cipher.decrypt(check_result[0])
    except InvalidToken:
        print("Wrong master password!")
        exit()

def add_password(service, username, password):
    encrypted_password = cipher.encrypt(password.encode())
    cursor.execute("""
        INSERT INTO ACCOUNTS (SERVICE, USERNAME, PASSWORD)
        VALUES (?, ?, ?)
    """, (service, username, encrypted_password))
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
        try:
            decrypted_password = cipher.decrypt(password).decode()
            print(f"ID: {account_id}, Service: {service}, Username: {username}, Password: {decrypted_password}")
        except InvalidToken:
            print("Wrong master password!")

def edit_password(edit_password_id):
    while True:
        print("1. Service")
        print("2. Username")
        print("3. Password")
        print("4. Quit")

        choice = input("What do you want to edit? ")

        if choice == "1":
            column = "SERVICE"
        elif choice == "2":
            column = "USERNAME"
        elif choice == "3":
            column = "PASSWORD"
        elif choice == "4":
            return
        else:
            print("That is not a valid choice!")
            continue

        value = input("What do you want to change it to: ")

        if column == "PASSWORD":
            value = cipher.encrypt(value.encode())

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