# Use a lightweight Python image
FROM python:3.12-slim

# Set a working directory inside the container
WORKDIR /app

# Copy your code into the container
COPY . .

# Install dependencies (if requirements.txt exists)
RUN pip install --no-cache-dir -r requirements.txt || true

# Command to run your script
CMD ["bash", "-c", "while true; do python3 main.py; sleep 21600; done"]