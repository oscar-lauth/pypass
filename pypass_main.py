import os
import sqlite3
import secrets
from pypass_functions import *

db_path = 'passwords.db' # path where db is stored, defaults to inside project folder

# generates master.key and salt.key to store hashed and salted master password and unique salt
if not os.path.exists('master.key') or not os.path.exists('salt.key'):
    master_file = open('master.key', 'wb')
    salt_file = open('salt.key', 'wb')
    hash_pass, salt = hash_salt_pass(input("Create a master password for your vault\n:"))
    master_file.write(hash_pass)
    salt_file.write(salt)
    master_file.close()
    salt_file.close()
# if master password is reset (i.e. master.key or salt.key are deleted) then passwords.db is deleted 
    if os.path.exists(db_path):
        os.remove(db_path)

# validates master_pass, if invalid quits
master_pass = input("Enter master password\n:")
if not check_hash_pass(open('master.key', 'rb').readline(), open('salt.key', 'rb').readline(), master_pass):
    print("Invalid master password\nQuitting PyPass")
    quit()

# setup sqlite3 db
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS vault (service TEXT PRIMARY KEY, user TEXT, password TEXT, salt BLOB, iv BLOB)")
conn.close()

print("""
  {PyPass Vault} 
 ----------------
 ap|Add password
 gp|Get password
 up|Update info
 ls|List services
 ds|Del services
 ev|Erase vault
 qp|Quit PyPass
 ----------------""")
while True:  # menu loop
    menu_choice = input("\nEnter a menu option\n:")

    if menu_choice == 'ap': # add password
        new_service = input("Enter service to add (ex: amazon)\n:")
        if in_vault(new_service, db_path):
            print("Error, service already in vault")
        else:
            new_user = input("Enter user/email\n:")
            new_pass = input("Enter password or leave blank to generate random password\n:")
            if new_pass == '':
                new_pass = pass_gen()
                print("Password is " + new_pass)
            # encrypts new_pass and gets adds service, user, encrypted pass, salt, and iv to db
            new_salt = secrets.token_bytes(16)
            new_info_enc = enc(new_pass, new_salt)
            new_info_all = new_service, new_user, new_info_enc[0], new_salt, new_info_enc[1]
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("INSERT INTO vault VALUES (?, ?, ?, ?, ?)", new_info_all)
            conn.commit()
            conn.close()
            print("New password added")

    elif menu_choice == 'gp': # get passsword
        get_service = input("Enter service (ex: amazon)\n:")
        if not in_vault(get_service, db_path):
            print("Error, service not in vault")
        else:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            for get_info in c.execute("SELECT user, password, salt, iv FROM vault WHERE service=?", (get_service,)):
                print("user/email: " + get_info[0])
                print("password: " + dec(get_info[1], get_info[2], get_info[3]))
            conn.close()

    elif menu_choice == 'up': # update info
        update_service = input("Enter service to update (ex: amazon)\n:")
        if not in_vault(update_service, db_path):
            print("Error, service not in vault")
        else:
            update_user = input("Enter updated user/email or leave blank to keep current\n:")
            if update_user != '':
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("UPDATE vault SET user=? WHERE service=?", (update_user, update_service))
                conn.commit()
                conn.close()
            update_pass = input("Enter updated password or leave blank to keep current\n:")
            if update_pass != '':
                update_salt = secrets.token_bytes(16)
                update_info_enc = enc(update_pass, update_salt) 
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("UPDATE vault SET password=?, salt=?, iv=? WHERE service=?", (update_info_enc[0], update_salt, update_info_enc[1], update_service))
                conn.commit()
                conn.close()

    elif menu_choice == 'ls': # list services
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        for service in c.execute("SELECT service FROM vault"):
            print("*"+service[0])
        conn.close()

    elif menu_choice == 'ds': # delete service
        del_service = input("Enter service to delete (ex: amazon)\n:")
        if not in_vault(del_service, db_path):
            print("Error, service not in vault")
        else:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("DELETE FROM vault WHERE service=?", (del_service,))
            conn.commit()
            print(del_service+" deleted")
            conn.close()

    elif menu_choice == 'ev': # erase vault
        confirm_ev = input("Enter 'CONFIRM' to erase vault\n:")
        if confirm_ev == 'CONFIRM':
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("DELETE FROM vault")
            conn.commit()
            conn.close()
            print("Vault erased")
        else:
            print("Aborted, vault not erased")

    elif menu_choice == 'qp': # quit pypass
        quit()

    else:
        print("Invalid menu option")
