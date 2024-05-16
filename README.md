## Prerequisites

Make sure you have Docker installed on your system. You can download and install Docker from [here](https://www.docker.com/get-started).

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mtauha/Scrapy-Book-Scraping
   cd Scrapy-Book-Scraping
   ```
2. **Build the Docker Image**

   Build the Docker image using the provided `Dockerfile`:

   ```bash
   docker build -t scrapy-bookscraper .
   ```
3. **Run the Docker Container**

   Run the Docker container to execute the Scrapy spider:

   ```bash
   docker run --rm -v $(pwd)/env/Bookscraper:/app scrapy-bookscraper
   ```

   This command will:

   - Run the Scrapy spider defined in `temporary_scaper_spider/spiders/bookspider.py`.
   - Output the scraped data to `books_data.csv` in the `env/Bookscraper` directory.

## Dockerfile Explanation

- **Base Image**: Uses `python:3.11.3-slim` as the base image.
- **Environment Variables**:
  - `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from writing `.pyc` files.
  - `PYTHONUNBUFFERED=1`: Ensures Python output is not buffered.
- **Working Directory**: Sets `/app` as the working directory in the container.
- **Copy Files**:
  - Copies `requirements.txt` into the container and installs the dependencies.
  - Copies the entire Scrapy project into the container.
- **Entry Point**: Runs the Scrapy spider and outputs the data to `books_data.csv`.

## Additional Notes

- Ensure that your `requirements.txt` is up-to-date with all the necessary dependencies for your Scrapy project.
- You can modify the Scrapy command in the `ENTRYPOINT` instruction of the Dockerfile if you need to run a different spider or change output formats.

## Contact

If you have any questions or issues, please open an issue in the repository or contact the maintainer.
