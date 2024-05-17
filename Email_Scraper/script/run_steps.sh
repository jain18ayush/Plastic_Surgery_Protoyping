#!/bin/bash

# Check if a file is passed as an argument
if [ "$#" -eq 1 ]; then
    FILE=$1
    echo "Running step1.py with file: $FILE"

    # Run step1.py with the passed file
    python3 step1.py "$FILE"
    if [ $? -ne 0 ]; then
        echo "Error running step1.py"
        exit 1
    fi

    echo "Step1 completed successfully."
    echo "Running step2.py"
else
    echo "No file argument passed. Running step2.py directly."
fi

# Run step2.py
python3 step2.py
if [ $? -ne 0 ]; then
    echo "Error running step2.py"
    exit 1
fi

echo "Step2 completed successfully."
