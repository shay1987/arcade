# Use a Python base image
FROM python:3.9-alpine3.15

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install dependencies, including mariadb-dev for mysqlclient if needed,
# and then install Flask-SQLAlchemy and PyMySQL
RUN apk add --no-cache gcc musl-dev mariadb-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install Flask-SQLAlchemy PyMySQL

# Copy the Flask application files into the container
COPY app/ .

# Expose the port your Flask app runs on
EXPOSE 5000

# Set environment variables (if not already set in Kubernetes deployment)
ENV MYSQL_ROOT_USER=root
ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_ROOT_HOST=mysql-service.default.svc.cluster.local
ENV MYSQL_ROOT_PORT=3306
ENV MYSQL_ROOT_DB=mydb
ENV FLASK_APP_PORT=5000

# Command to run the Flask application
CMD ["python", "login.py"]