# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y libvirt-dev

# Set environment variable
ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the common utility wheel file into the container
COPY utils/common/dist/common-0.1.0-py3-none-any.whl /app/utils/common/dist/

# Install Poetry and project dependencies in rancher_api and vm_api
RUN pip install --upgrade pip \
    && pip install poetry \
    && cd /app/application/micro_services/rancher_api && poetry add /app/utils/common/dist/common-0.1.0-py3-none-any.whl \
    && cd /app/application/micro_services/vm_api && poetry add /root/hexav2/application/micro_services/configs/vm_api/dist/vm_api-0.1.0-py3-none-any.whl \
    && cd /app/application/micro_services/vm_api && poetry add /root/hexav2/application/micro_services/configs/rancher_api/dist/rancher_api-0.1.0-py3-none-any.whl \
    && poetry install --no-dev

# Run Alembic migrations in vm_api
RUN cd /app/application/micro_services/vm_api/alembic \
    && alembic revision --autogenerate -m "first migration" \
    && alembic upgrade head

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME SkyCloud

# Run uvicorn in the app directory when the container launches
CMD ["sh", "-c", "cd app/application/app && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]
