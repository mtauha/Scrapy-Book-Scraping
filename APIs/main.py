import os, subprocess
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Bookscraper.temporary_scaper_spider.models import SessionLocal
from Bookscraper.temporary_scaper_spider.pydantic_models import Book

from crud import get_books, get_book

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = get_books(db=db, skip=skip, limit=limit)
    return books


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/scrape")
async def start_scraping():
    try:
        # Change the directory to where your Scrapy project is located
        os.chdir("../env/Bookscraper/temporary_scaper_spider")

        # Run the Scrapy command
        result = subprocess.run(
            ["scrapy", "crawl", "bookspider"],
            check=True,
            capture_output=True,
            text=True,
        )

        return {"message": "Scraping completed successfully", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
