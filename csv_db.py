import csv
import subprocess

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

# Example usage:
file_name = 'data.csv'
data = read_data(file_name)

stream_file_name = 'data_stream.csv'
data_stream = read_data(stream_file_name)

# Text Vars
username = "mtd"
hostname = "rpibolt.local"
process = "ufw.service"

# Construct the SSH command
ssh_command = f"ssh {username}@{hostname} 'systemctl status {process}'"

# Execute the SSH command
try:
    ssh_output = subprocess.check_output(ssh_command, shell=True, text=True)
    
    # Add the SSH command output to the data
    new_data = {'username': username, 'hostname': hostname, 'process': process, 'ssh_output': ssh_output}
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
