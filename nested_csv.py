from simple_term_menu import TerminalMenu
import csv
import subprocess
import os

# Function to read data from CSV file
def read_data(file_name):
    data = []
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to write data to CSV file
def write_data(file_name, data):
    with open(file_name, mode='w', newline='') as file:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)

# Function to write data to CSV file
def write_stream_data(file_name, data):
    with open(file_name, mode='w', newline='') as file:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)

# Data Functions
# Read CSV:
file_name = 'data.csv'
data = read_data(file_name)

stream_file_name = 'data_stream.csv'
data_stream = read_data(stream_file_name)

# Menu Functions
def populate_menu():
    username_populated = data[0]['username']
    hostname_populated = data[0]['hostname']
    server_populated = (f"{username_populated}@{hostname_populated}")
    return server_populated

def populate_menu_username():
    username_populated = data[0]['username']
    return username_populated

def populate_menu_hostname():
    hostname_populated = data[0]['hostname']
    return hostname_populated

def ssh_control():
    # Execute the SSH command
    try:
        ssh_output = subprocess.check_output(ssh_command, shell=True, text=True)
        
        # Add the SSH command output to the data
        new_data = {'username': username, 'hostname': hostname, 'process': process}
        stream_data = {'ssh_output': ssh_output}

        # Append the new data to the existing data
        data.append(new_data)
        data_stream.append(stream_data)
        
        # Write the updated data back to the CSV file
        write_data(file_name, data)
        write_stream_data(stream_file_name, data_stream)
        
        print(f"SSH command output:\n{ssh_output}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing SSH command: {e}")

def stream_control():
    while True:
        # Display a menu or prompt
        print("1. [ ONE ] | 2. [ Two ] | 3. [ CLS ] | 4. [ Q ]")
        choice = input("$i: ")

        if choice == '1':
            # Handle option 1
            print("You selected Option 1")
        elif choice == '2':
            # Handle option 2
            print("You selected Option 2")
        elif choice == '3':
            # Clear the terminal screen
            os.system('clear')  # On Windows, you can use 'cls' instead of 'clear'
            break
        elif choice == '4':
            # Quit the program
            os.system('clear')
            break
        else:
            print("Invalid choice. Please try again.")

# Text Vars
username = "xxx"
hostname = "rpibolt.local"
process = "ufw.service"

# Construct the SSH command
ssh_command = f"ssh {username}@{hostname} 'systemctl status {process}'"

# Define submenus
submenu1 = TerminalMenu([f"Submenu 1 {populate_menu_hostname()}", "Submenu 1 Option 2", "Submenu 1 Option 3"])
submenu2 = TerminalMenu(["Submenu 2 Option 1", "Submenu 2 Option 2", "Submenu 2 Option 3"])

# Define the main menu with submenus
main_menu = TerminalMenu(["Serverz", "Processez", "Controlz", "Exit"])

while True:
    # Show the main menu and get the selected option index
    main_menu_entry_index = main_menu.show()

    if main_menu_entry_index is None or main_menu_entry_index == 3:
        # Exit the program
        break
    elif main_menu_entry_index == 0:
        # User selected Option 1, show submenu 1
        submenu1_entry_index = submenu1.show()
        if submenu1_entry_index == 0:
            ssh_control()
            stream_control()
        elif submenu1_entry_index is not None:
            print(f"Selected submenu 1 option: {submenu1_entry_index + 1}")
            print(populate_menu())
            
    elif main_menu_entry_index == 1:
        # User selected Option 2, show submenu 2
        submenu2_entry_index = submenu2.show()
        if submenu2_entry_index is not None:
            print(f"Selected submenu 2 option: {submenu2_entry_index + 1}")
