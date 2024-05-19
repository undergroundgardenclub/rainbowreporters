FROM python:3.11.9-slim

# Root
WORKDIR /usr/src/backends-api

# Install python packages for app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy src
COPY . .

# Start
EXPOSE 3000
CMD ["python", "-u", "src/start.py"]
