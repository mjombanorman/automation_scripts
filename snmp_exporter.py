import os
import requests
import getpass

# Define the URL and file name of the tar file
url = "https://github.com/prometheus/snmp_exporter/releases/download/v0.22.0/snmp_exporter-0.22.0.linux-amd64.tar.gz"
tar_file = "snmp_exporter-0.22.0.linux-amd64.tar.gz"
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

# Check if the 'prometheus' user already exists, and create it if not
username = "prometheus"
try:
    result = getpass.getuser()
    if result != username:
        os.system(f"useradd --system {username}")
except Exception:
    os.system(f"useradd --system {username}")

# Download the tar file
response = requests.get(url)
with open(tar_file, "wb") as file:
    file.write(response.content)

# Extract the contents of the tar file
os.system(f"tar xzf {tar_file}")

# Copy the files to the /usr/local/bin/ folder
os.system(f"cp ./{extract_path}/snmp_exporter /usr/local/bin/snmp_exporter")
os.system(f"cp ./{extract_path}/snmp.yml /usr/local/bin/snmp.yml")

# Create the service file
with open("snmp-exporter.service", "w") as file:
    file.write(service_contents)

# Move the service file to the appropriate location
os.system("mv snmp-exporter.service /etc/systemd/system/")

# Reload systemd to pick up the new service file
os.system("systemctl daemon-reload")

# Enable and start the service
os.system("systemctl enable snmp-exporter.service")
os.system("systemctl start snmp-exporter.service")
