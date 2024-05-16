# Use the official Python image as a base
FROM python:3.11.3-slim

# Set environment variables to prevent Python from writing .pyc files and to prevent buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY env/requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Scrapy project into the container
COPY env/Bookscraper /app

# Set the entry point to run the Scrapy spider
ENTRYPOINT ["scrapy", "crawl", "bookspider", "-o", "books_data.csv"]
