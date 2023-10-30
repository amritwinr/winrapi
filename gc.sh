#!/bin/bash

# Define the Gunicorn command and application directory
GUNICORN_CMD="gunicorn"
APP_DIR="."

# Function to start Gunicorn
start_gunicorn() {
    if pgrep -f "$GUNICORN_CMD" > /dev/null; then
        echo "Gunicorn is already running."
    else
        "$GUNICORN_CMD" --bind 0.0.0.0:8000 WINR.wsgi & # Adjust the number of workers and bind address/port as needed
        echo "Gunicorn started."
    fi
}

# Function to restart
restart_gunicorn() {
    if pgrep -f "$GUNICORN_CMD" > /dev/null; then
        kill -9 $(lsof -t -i:8000 -sTCP:LISTEN)
        echo "Stopping Gunicorn..."
        sleep 5  # Wait for old processes to exit gracefully
    fi
    start_gunicorn
}
# Check for the action and call the appropriate function
if [ "$1" == "start" ]; then
    start_gunicorn
elif [ "$1" == "restart" ]; then
    restart_gunicorn
else
    echo "Usage: $0 [start|restart]"
fi
