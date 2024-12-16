#!/bin/bash

read -p "Enter the directory where your main.py file is located (e.g., /download/HIDS): " script_directory

read -p "Enter the username to run the service: " username

echo "Checking for virtual environment..."
if [ ! -d "$script_directory/.venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv "$script_directory/.venv"
else
    echo "Virtual environment found."
fi

echo "Activating virtual environment and installing dependencies..."
source "$script_directory/.venv/bin/activate"
pip install --upgrade pip
pip install plyer
if [ -f "$script_directory/requirements.txt" ]; then
    pip install -r "$script_directory/requirements.txt"
else
    echo "Error: requirements.txt not found in $script_directory!"
    deactivate
    exit 1
fi

service_content="[Unit]
Description=HIDS Monitoring Service
After=network.target

[Service]
WorkingDirectory=$script_directory
ExecStart=/bin/bash -c 'source $script_directory/.venv/bin/activate && python $script_directory/main.py'
Restart=always
User=$username

[Install]
WantedBy=multi-user.target"

echo "Creating the service file..."
echo "$service_content" | sudo tee /etc/systemd/system/hids.service > /dev/null

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling the service to start on boot..."
sudo systemctl enable hids.service

echo "Starting the HIDS service..."
sudo systemctl start hids.service

echo "Service status:"
sudo systemctl status hids.service
