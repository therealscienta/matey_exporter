#!/bin/bash

# Check if version is provided
if [ ! $1 ]; then
    echo "Usage: ./install.sh <version>"
    exit 1
fi

CONFIG_DIR=/etc/matey_exporter
CONFIG_FILE=$CONFIG_DIR/config.yaml
BINARY=dist/matey_exporter-$1
BINARY_DIR=/usr/bin/matey_exporter

#  Create directories
dir_exist () {
    if [ ! -d $1 ]; then
    mkdir $1
    fi
}
echo "Creating directories..."
dir_exist $CONFIG_DIR

# Copy config file
echo "Copying config file..."
cp config.yaml $CONFIG_FILE

# Copy binary
echo "Copying binary..."
cp $BINARY $BINARY_DIR

# TODO: Make better service file
# Create service file
echo "Creating service file..."
cat <<EOF > /etc/systemd/system/matey_exporter.service
[Unit]
Description=Matey Exporter

[Service]
ExecStart=/usr/bin/matey_exporter --config /etc/matey_exporter/config.yaml

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

echo "Installation complete."
echo "Edit configuration file /etc/matey_exporter/config.yaml and then run 'systemctl start matey_exporter' to start the service."