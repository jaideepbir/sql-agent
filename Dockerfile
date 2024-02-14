# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install git if your project needs to install dependencies from git repositories
RUN apt-get update && apt-get install -y git

# Copy the current directory contents and the requirements file into the container at /app
COPY . /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 to 8004 available to the world outside this container
EXPOSE 8000 8001 8002 8003 8004

# Define environment variable
ENV NAME World

# Command to run the Chainlit application
CMD ["chainlit", "run", "app_csv.py", "--port", "8002", "-w"]
