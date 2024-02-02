from simple_term_menu import TerminalMenu
import subprocess
import csv

# Define Mode(s)
sim_off = True
prod_off = True

# Dummy 'ls /' Command Return
sim_command = ('''bin
                  boot
                  var''')

# I/O Operations
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

# Rudimentary User Inputs During Development Mode
class Debug:
    def __init__(self):
        self.hostname = input('Hostname: ')
        self.username = input('Username: ')
        self.command = input('Command: ')

# Production Mode - Empty
class Production:
    def __init__(self):
        self.hostname = input('Hostname-P: ')
        self.username = input('Username-P: ')
        self.command = input('Command-P: ')       

# Define Developer || Production Modes
def Dev_Mode():
    return Debug()
def Prod_Mode():
    return Production()

def execute_ssh_command(hostname, username, command):
    # Sim-Specific Vars & Override PIPE
    stdoutSim = (f"ssh: connect to host {hostname} port 22: Connection Established")
    stderrSim = (f"{command}\n")

    try:
        # Construct the SSH command
        ssh_command = f"ssh {username}@{hostname} '{command}'"

        # Execute the SSH command
        # Use Simulation_Off Mode Switch - ( True || False )
        # Use a ternary expression to switch between two variables
        result = subprocess.run(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True) if sim_off else (subprocess.run(print(ssh_command), print(stdoutSim), print(stderrSim), text=True, check=True))

        # Return the command's standard output
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing SSH command: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # I/O Controls:
    file_name = 'data.csv'
    data = read_data(file_name)

    stream_file_name = 'data_stream.csv'
    data_stream = read_data(file_name)

    # Simulation Status Prompt
    mode = ("Simulation Mode Deactivated") if sim_off else ("Simulation Mode Activated")
    print(mode)

    # Prod-Off
    process = "Off"

    # Switch: Developer & Production Modes(s)
    m = Dev_Mode() if prod_off else Prod_Mode()
    print(m.hostname)
    print(m.username)
    print(m.command)

    # Define menu options with associated SSH commands
    options = [
        {"name": "List files in home directory", "command": "ls ~"},
        {"name": "Display system uptime", "command": "uptime"},
        {"name": "Show disk usage", "command": "df -h"},
    ]

    # Create a menu
    menu = TerminalMenu([option["name"] for option in options])

    # Show the menu and get the selected option index
    menu_entry_index = menu.show()

    # Process the selected option
    if menu_entry_index is not None:
        selected_option = options[menu_entry_index]
        print(f"Selected option: {selected_option['name']}")
        
        # Execute the associated SSH command
        try:
            ssh_output = subprocess.check_output(["ssh", f'{m.username}@{m.hostname}' , selected_option['command']], text=True)
            print(f"SSH command output:\n{ssh_output}")

            # Add the SSH command output to the data
            command_0 = selected_option['command']
            new_data = {'username': m.username, 'hostname': m.hostname, 'command': command_0, 'process': process} if prod_off else {'username': m.username, 'hostname': m.hostname, 'command': command_0}
            stream_data = {'ssh_output': ssh_output}

            # Append the new data to the existing data
            data.append(new_data)
            data_stream.append(stream_data)

            # Write the updated data back to the CSV file
            write_data(file_name, data)
            write_stream_data(stream_file_name, data_stream)

        except subprocess.CalledProcessError as e:
            print(f"Error executing SSH command: {e}")
    else:
        print("You didn't select any option.")