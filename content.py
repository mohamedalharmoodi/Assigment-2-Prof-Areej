# ============================================================
# File: models/content.py
# Classes: Content (abstract), Movie, TVSeries, Documentary
# ============================================================

# Importing Abstract Base Class tools from abc module
from abc import ABC, abstractmethod

# Defining an abstract base class 'Content'
class Content(ABC):
    """Abstract base class for all StreamFlix content."""

    # Constructor to initialize all common attributes for content
    def __init__(self, content_id, title, genre, release_year,
                 duration_min, rating=0.0, is_available=True,
                 is_premium=False, price=0.0):

        # Private attribute: unique ID of content
        self.__content_id   = content_id

        # Private attribute: title of the content
        self.__title        = title

        # Private attribute: genre (e.g., Action, Drama)
        self.__genre        = genre

        # Private attribute: release year of content
        self.__release_year = release_year

        # Private attribute: duration in minutes
        self.__duration_min = duration_min

        # Private attribute: rating (default 0.0)
        self.__rating       = rating

        # Private attribute: availability status (True/False)
        self.__is_available = is_available

        # Private attribute: whether content is premium
        self.__is_premium   = is_premium

        # Private attribute: price (only for premium content)
        self.__price        = price

    # ── Getters ──────────────────────────────────────────────

    # Returns content ID
    def get_content_id(self):    return self.__content_id

    # Returns title
    def get_title(self):         return self.__title

    # Returns genre
    def get_genre(self):         return self.__genre

    # Returns release year
    def get_release_year(self):  return self.__release_year

    # Returns duration
    def get_duration_min(self):  return self.__duration_min

    # Returns rating
    def get_rating(self):        return self.__rating

    # Returns availability status
    def get_is_available(self):  return self.__is_available

    # Returns premium status
    def get_is_premium(self):    return self.__is_premium

    # Returns price
    def get_price(self):         return self.__price

    # ── Setters ──────────────────────────────────────────────

    # Updates title
    def set_title(self, title):          
        self.__title = title

    # Updates genre
    def set_genre(self, genre):          
        self.__genre = genre

    # Updates release year
    def set_release_year(self, year):    
        self.__release_year = year

    # Updates availability status
    def set_is_available(self, b):       
        self.__is_available = b

    # Updates premium status
    def set_is_premium(self, b):         
        self.__is_premium = b

    # Updates price with validation
    def set_price(self, price):
        # Raise error if price is negative
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = price

    # Updates rating with validation
    def set_rating(self, rating):
        # Rating must be between 0 and 10
        if not (0.0 <= rating <= 10.0):
            raise ValueError("Rating must be between 0 and 10.")
        self.__rating = rating

    # ── Abstract method (must override in subclass) ──────────

    # Forces subclasses to define their own content type
    @abstractmethod
    def get_content_type(self):
        pass

    # ── Display ──────────────────────────────────────────────

    # Returns formatted string of content details
    def display_info(self):

        # Determine availability text
        status = "Available" if self.__is_available else "Unavailable"

        # Show price only if premium
        premium = f" | Price: ${self.__price:.2f}" if self.__is_premium else ""

        # Return formatted multi-line string
        return (
            f"[{self.get_content_type()}] {self.__title} ({self.__release_year})\n"
            f"  Genre: {self.__genre} | Duration: {self.__duration_min} min"
            f" | Rating: {self.__rating}/10 | {status}{premium}"
        )

    # String representation of object
    def __str__(self):
        return self.display_info()


# ─────────────────────────────────────────────────────────────
# Movie class inheriting from Content
class Movie(Content):
    """A feature-length film. Inherits from Content."""

    # Constructor for Movie class
    def __init__(self, content_id, title, genre, release_year,
                 duration_min, director="", cast=None,
                 rating=0.0, is_available=True, is_premium=False, price=0.0):

        # Call parent constructor
        super().__init__(content_id, title, genre, release_year,
                         duration_min, rating, is_available, is_premium, price)

        # Private attribute: director name
        self.__director = director

        # Private attribute: list of cast members
        self.__cast     = cast if cast else []

    # Getter for director
    def get_director(self): return self.__director

    # Getter for cast (returns copy to protect data)
    def get_cast(self):     return list(self.__cast)

    # Setter for director
    def set_director(self, d):   self.__director = d

    # Setter for cast
    def set_cast(self, cast):    self.__cast = cast

    # Returns content type
    def get_content_type(self):  return "Movie"

    # Overrides display method to include director
    def display_info(self):
        base = super().display_info()
        return f"{base}\n  Director: {self.__director}"


# ─────────────────────────────────────────────────────────────
# TV Series class inheriting from Content
class TVSeries(Content):
    """A TV series with seasons and episodes. Inherits from Content."""

    # Constructor
    def __init__(self, content_id, title, genre, release_year,
                 duration_min, seasons=1, episodes=1,
                 is_completed=False, rating=0.0,
                 is_available=True, is_premium=False, price=0.0):

        # Call parent constructor
        super().__init__(content_id, title, genre, release_year,
                         duration_min, rating, is_available, is_premium, price)

        # Private attributes for series details
        self.__seasons      = seasons
        self.__episodes     = episodes
        self.__is_completed = is_completed

    # Getters
    def get_seasons(self):      return self.__seasons
    def get_episodes(self):     return self.__episodes
    def get_is_completed(self): return self.__is_completed

    # Setters
    def set_seasons(self, n):        self.__seasons = n
    def set_episodes(self, n):       self.__episodes = n
    def set_is_completed(self, b):   self.__is_completed = b

    # Returns content type
    def get_content_type(self): return "TV Series"

    # Display additional info
    def display_info(self):
        base   = super().display_info()

        # Determine completion status
        status = "Completed" if self.__is_completed else "Ongoing"

        return f"{base}\n  Seasons: {self.__seasons} | Episodes: {self.__episodes} | {status}"


# ─────────────────────────────────────────────────────────────
# Documentary class inheriting from Content
class Documentary(Content):
    """A documentary film. Inherits from Content."""

    # Constructor
    def __init__(self, content_id, title, genre, release_year,
                 duration_min, subject="", narrator="",
                 rating=0.0, is_available=True, is_premium=False, price=0.0):

        # Call parent constructor
        super().__init__(content_id, title, genre, release_year,
                         duration_min, rating, is_available, is_premium, price)

        # Private attributes
        self.__subject  = subject
        self.__narrator = narrator

    # Getters
    def get_subject(self):   return self.__subject
    def get_narrator(self):  return self.__narrator

    # Setters
    def set_subject(self, s):    self.__subject = s
    def set_narrator(self, n):   self.__narrator = n

    # Returns content type
    def get_content_type(self):  return "Documentary"

    # Display additional info
    def display_info(self):
        base = super().display_info()
        return f"{base}\n  Subject: {self.__subject} | Narrator: {self.__narrator}"
