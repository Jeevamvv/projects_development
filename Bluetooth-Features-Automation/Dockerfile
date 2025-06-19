# Use Ubuntu base image
FROM ubuntu:20.04

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    bluez bluetooth bluez-tools \
    pulseaudio pulseaudio-utils \
    playerctl \
    mpv \
    dbus udev \
    sudo \
    git vim nano \
    libbluetooth-dev build-essential \
    && apt-get clean

# Set the working directory
WORKDIR /docker_bluetooth_app

# Copy the project files into the container
COPY . /docker_bluetooth_app

# Upgrade pip and install Python requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Set up PulseAudio environment variable
ENV PULSE_SERVER=unix:/run/user/1000/pulse/native

# Default command to run the app
CMD ["python3", "trigger.py"]
