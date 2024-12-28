FROM python:3.12.1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the data directory
RUN mkdir -p /app/data

# Set correct permissions for the data directory
RUN chmod -R 755 /app/data

# Copy the rest of the application code into the container
COPY . .

# Set the default command to run your app
CMD ["python", "check_ip.py"]
