# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y libvirt-dev

# Set environment variables
ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate a virtual environment
RUN python3 -m venv /app/application/app/myenv \
    && . /app/application/app/myenv/bin/activate

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Install project dependencies in the virtual environment using Poetry
RUN . /app/application/app/myenv/bin/activate \
    && cd /app/application/app \
    && poetry add /app/utils/common/dist/common-0.1.0-py3-none-any.whl \
    && poetry add /app/application/micro_services/configs/vm_api/dist/vm_api-0.1.0-py3-none-any.whl \
    && poetry add /app/application/micro_services/configs/rancher_api/dist/rancher_api-0.1.0-py3-none-any.whl \
    && poetry install --only main

# Install Alembic in the Poetry environment
RUN . /app/application/app/myenv/bin/activate \
    && pip install alembic

# Run Alembic migrations in vm_api
RUN . /app/application/app/myenv/bin/activate \
    && cd /app/application/micro_services/vm_api/alembic \
    && alembic revision --autogenerate -m "first migration" \
    && alembic upgrade head

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME=SkyCloud

# Run uvicorn in the app directory when the container launches
CMD ["sh", "-c", ". /app/application/app/myenv/bin/activate && cd /app/application/app && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]
