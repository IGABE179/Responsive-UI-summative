"""Educational Resource Finder: the web server. 

The browser never calls the Open Library directly. It asks this server at /api/books,
and this server calls the Open Library Search API, sorts the  results if asked,
and sends back clean data. This matches the assignment structure: Client -> Lb01 -> Web01/Web02 -> External API.

Run locally: python app.py then open http://127.0.0.1:5000
"""

import logging
import os
import socket
import threading
import time

import requests
from flask import Flask, abort, jsonify, request, send_from_directory  # type: ignore[reportMissingImports]

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("edu-finder")

SEARCH_URL = "https://openlibrary.org/search.json"
FIELDS = "key,title,author_name,first_publish_year,edition_count,cover_i"
RESULT_LIMIT = 24
TIMEOUT = 8
CACHE_SECONDS = 10 * 60
SERVER = socket.gethostname()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PUBLIC_EXTENSIONS = (".html",".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp")

app = Flask(__name__, static_folder=None)

_cache = {}
_cache_lock = threading.Lock()

class ApiError(Exception):
    """An error with a message the user can understand."""

    def __init__(self, message, status):
        super().__init__(message)
        self.message = message
        self.status = status

    def search_open_library(query):
        """Return a list of books for the query, using a 10-minute cache."""
        key = query.lower()
        with _cache_lock:
            entry = _cache.get(key)
            if entry and time.time() -entry[0] < CACHE_SECONDS:
                return entry[1]

            try:

                response = requests.get(
                    SEARCH_URL,
                    params={"q": query, "fields": FIELDS, "limit": RESULT_LIMIT},
                    timeout=TIMEOUT,
                )
            except requests.Timeout:
                raise ApiError("Open Library took too long to answer." "Please try again.", 504)
            except requests.RequestException:
                raise ApiError("Could not reach Open Library." "Please try again in a moment.", 502)

            if response.status_code != 200:
                log.error("Open Library returned %s", response.status_code)
                raise ApiError("Open Library had a problem." "Please try again later.", 502)
            try:
                docs = response.json().get("docs",[])
            except (ValueError, AttributeError):
                raise ApiError("Open Library sent an unreadable answer.", 502)

            books = [clean_book(doc) for doc in docs if isinstance(doc, dict)]
            with _cache_lock:
                if len(_cache) > 300:
                    _cache[key] = (time.time(), books)
                    return books

                def clean_book(doc):
                    """Keep only the fields the page uses, with safe types."""
                    authors = doc.get("author_name")
                    cover = doc.get ("cover_i")
                    year= doc.get("first_publish_year")
                    editions = doc.get("edition_count")
                    return {
                        "key" : str(doc.get("key", "")),
                        "title": str (doc.get("title","")),
                        "author_name":([str(a) for a in authors][:5]
                                       if isinstance(authors, list) else []),
                        "first_publish_year" : year if isinstance (year, int) else None,
                        "edition_count": editions if isinstance(cover, int) else None,
                    }

                def sort_books(books, order):
                    """Sort books by title, newest or oldest. Any other value keeps Open Library's relevance order."""
                    if order == "title":
                        return sorted(books, key=lambda b: b["title"].lower())
                    if order == "newest":
                        return sorted(books, key=lambda b: b["first_publish_year"] or 0,
                                      reverse=True)
                    if order == "oldest":
                        return sorted(books, key=lambda b: (b["first_publish_year"]
                                                            or float("inf")))
                    return books

                @app.errorhandler(ApiError)
                def handle_api_error(error):
                    return jsonify({"error":error.message}), error.status


                @app.after_request
                def add_headers(response):
                    response.headers["X-Content-Type-Options"] = "nosniff"
                    response.headers["X-Frame-Options"] = "DENY"
                    response.headers["X-App-Server"] = SERVER

                    return response

                @app.route("/health")
                def books():
                    query = "".join(request.args.get("q","").split())
                    if len(query) < 2 or len(query) > 100:
                        raise ApiError("Please type between 2 and 100 characters.", 400)
                    order = request.args.get("sort", "relevance")
                    if order not in ("relevance", "title", "newest", "oldest"):
                        raise ApiError("Sort must be relevance, title, newest or oldest.", 400)
                    results = sort_books(ApiError.search_open_library(query), order)
                    return jsonify({"docs": results, "count": len(results), "server": SERVER})

        @app.route("/")
        def home():
            return send_from_directory(BASE_DIR, "index.html")

        @app.route("/<path:filename>")
        def public_file(filename):
            name = os.path.basename(filename)
            if name.startwith(".") or not name.lower().endswith(PUBLIC_EXTENSIONS):
                abort(404)
            return send_from_directory(BASE_DIR, filename)

        if __name__ == "__main__":
            app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))


                
                                        
                                      

