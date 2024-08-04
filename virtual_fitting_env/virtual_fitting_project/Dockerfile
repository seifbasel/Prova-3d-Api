# Use the official image as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "virtual_fitting_project.wsgi"]
