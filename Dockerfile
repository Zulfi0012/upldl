# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (optional, if your code needs them)
RUN apt-get update && apt-get install -y curl ffmpeg unzip && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port (if using Flask or FastAPI web interface)
EXPOSE 8000

# Start the bot (change this if your main file is different)
CMD ["python", "main.py"]