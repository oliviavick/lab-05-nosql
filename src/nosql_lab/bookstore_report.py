#!/usr/bin/env python3
"""Print a bookstore inventory report using MongoDB Atlas."""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Read database credentials from the environment.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def main():
    """Connect to MongoDB and print books for selected authors."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        logging.error("MongoDB Atlas credentials are not configured.")
        return

    client = None

    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000,
        )

        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas.")

        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        # Include starter authors and our newly added author.
        author_ids = ["author_002", "author_003", "author_004"]

        total = authors.count_documents({"_id": {"$in": author_ids}})
        print(f"\nAuthors: {total}")

        for author in authors.find({"_id": {"$in": author_ids}}):
            print(f"\n{author['name']}")

            # Find all books referencing this author.
            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")

    except PyMongoError as error:
        logging.error("MongoDB error: %s", error)

    finally:
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()