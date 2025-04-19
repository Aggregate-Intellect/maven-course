# Use an official Python 3.11 slim image as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install project dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create non-root user and give them permissions
RUN useradd -m chainlituser && \
    mkdir -p /app/.files && \
    chown -R chainlituser:chainlituser /app

# Switch to non-root user
USER chainlituser

# Copy the entire project into the container
COPY . .

# Expose the port used by Chainlit
EXPOSE 7860

# The command to run the Chainlit app
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
