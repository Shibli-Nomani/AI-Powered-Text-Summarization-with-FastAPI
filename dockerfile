# Use an official Python 3.10 base image
FROM python:3.10.8-slim

# Set working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and directories
COPY ./main.py ./main.py
COPY ./Readme.md ./Readme.md

COPY ./agents ./agents
COPY ./endpoints ./endpoints
COPY ./schemas ./schemas
COPY ./services ./services
COPY ./utils ./utils
COPY ./web ./web
COPY ./logs ./logs   

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
