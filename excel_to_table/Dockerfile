# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE main.settings

# Create and set the working directory
WORKDIR /app

# COPY requirement.txt /app/requirement.txt
# RUN pip install -r requirement.txt
RUN apt update && apt install -y libzbar0
RUN apt install -y libgl1-mesa-glx
RUN apt install libdmtx0b
RUN pip install --upgrade pip
RUN pip install Django pandas numpy opencv-python grpcio-tools grpcio djangorestframework django-crispy-forms daphne mysqlclient pyzbar crispy-bootstrap4 pylibdmtx pytesseract qrcode openpyxl
COPY . /app/