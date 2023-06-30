import os
import requests

# Prompt the user to enter the URL
url = input("Enter the URL to download the latest file: ")
tar_file = url.split("/")[-1]

# Define the path for extracting the tar file
extract_path = "./snmp_exporter"

# Define the service file contents
service_contents = """
[Unit]
Description=Prometheus SNMP Exporter Service
After=network.target

[Service]
Type=simple
User=prometheus
ExecStart=/usr/local/bin/snmp_exporter --config.file="/usr/local/bin/snmp.yml"

[Install]
WantedBy=multi-user.target
"""

# Download the tar file
response = requests.get(url)
with open(tar_file, "wb") as file:
    file.write(response.content)

# Extract the contents of the tar file
os.system(f"sudo tar xzf {tar_file}")

# Copy the files to the /usr/local/bin/ folder
os.system(f"sudo cp ./{extract_path}/snmp_exporter /usr/local/bin/snmp_exporter")
os.system(f"sudo cp ./{extract_path}/snmp.yml /usr/local/bin/snmp.yml")

# Create the service file
with open("snmp-exporter.service", "w") as file:
    file.write(service_contents)

# Move the service file to the appropriate location
os.system("sudo mv snmp-exporter.service /etc/systemd/system/")

# Create the prometheus user
os.system("sudo useradd --system prometheus")

# Reload systemd to pick up the new service file
os.system("sudo systemctl daemon-reload")

# Enable and start the service
os.system("sudo systemctl enable snmp-exporter.service")
os.system("sudo systemctl start snmp-exporter.service")
