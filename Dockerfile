FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port the app runs on (Cloud Run requires 8080 by default)
EXPOSE 8080

# Command to run the application (assuming the root directory is used to serve the agent)
CMD ["sh", "-c", "adk web --host 0.0.0.0 --port ${PORT:-8080} ./"]
