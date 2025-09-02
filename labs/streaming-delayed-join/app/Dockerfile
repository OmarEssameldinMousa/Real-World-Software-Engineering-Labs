# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command can be overridden in docker-compose.yml
CMD ["python"]