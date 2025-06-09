#!/bin/sh

# Make sure the script is executable
chmod +x /app/pipeline.py

# Execute the python script with all passed arguments
# "$@" expands to all arguments passed to the entrypoint.sh script
exec python /app/pipeline.py "$@"
