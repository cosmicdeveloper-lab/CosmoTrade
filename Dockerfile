# Use the latest Ubuntu base image
FROM ubuntu:latest
LABEL authors="benyamin"

# Set the ENTRYPOINT for the Ubuntu image
ENTRYPOINT ["top", "-b"]

# Use the Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /home/benyamin/PycharmProjects/CosmoTrade

# Copy Python scripts into the container
COPY . /cosmotrade/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Command to run the bot script
CMD ["python3", "main.py"]
