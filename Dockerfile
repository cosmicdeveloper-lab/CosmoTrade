FROM python:3.10-slim

# Set working directory
WORKDIR /cosmotrade

# Copy all contents from current directory into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]
