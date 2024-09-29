# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements to the container
COPY requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the server source code to the container
COPY src /app/src

# Copy the model source code to the container
COPY scripts /app/scripts

# Copy the model weights to the container
COPY experiments /app/experiments

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Start the FastAPI application using uvicorn
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]