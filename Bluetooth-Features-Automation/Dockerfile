
# Use Ubuntu as base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /bluetooth_app

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    bluez bluez-tools bluetooth \
    libglib2.0-dev libbluetooth-dev \
    libgirepository1.0-dev gir1.2-glib-2.0 \
    python3-gi python3-gi-cairo \
    dbus libdbus-1-dev libdbus-glib-1-dev \
    build-essential pkg-config cmake \
    sudo vim \
    && apt-get clean

# Copy all project files into the container
COPY . /bluetooth_app

# Install Python dependencies
RUN pip3 install --default-timeout=200 --no-cache-dir -r requirements.txt

# Create and configure user
RUN adduser --disabled-password --gecos '' btuser && \
    adduser btuser sudo && \
    usermod -a -G bluetooth btuser

# Set permissions
RUN chown -R btuser:btuser /bluetooth_app

# Switch to non-root user
USER btuser
ENV PYTHONPATH=/bluetooth_app

# Default command
CMD ["python3", "run.py"]
