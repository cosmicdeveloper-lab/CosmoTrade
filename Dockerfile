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
COPY divergence.py fibonacci.py Ichimoku_cloud.py init.py moving_average.py rates.py telegram_bot.py ./

# Copy the symbols folder (ensure this folder exists in the build context)
COPY symbols/ ./symbols/

# Copy requirements file into the container (ensure you have a requirements.txt file)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Command to run the bot script
CMD ["python", "init.py"]
