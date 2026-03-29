# ============================================================
# File: models/user.py
# Classes: ViewingRecord, Notification, Feedback,
#          User, RegularUser, Administrator
# ============================================================

from datetime import datetime   # Import datetime to record timestamps


# ─────────────────────────────────────────────────────────────
class ViewingRecord:
    """Stores one content-watch event for a user."""  # Class description

    def __init__(self, record_id, content_id, content_title, progress_pct=100.0):  # Constructor
        self.__record_id     = record_id        # Unique ID for viewing record
        self.__content_id    = content_id       # ID of content watched
        self.__content_title = content_title    # Title of content
        self.__watched_on    = datetime.now()   # Timestamp when content was watched
        self.__progress_pct  = progress_pct     # Percentage watched (default 100%)

    def get_record_id(self):      return self.__record_id      # Return record ID
    def get_content_id(self):     return self.__content_id     # Return content ID
    def get_content_title(self):  return self.__content_title  # Return content title
    def get_watched_on(self):     return self.__watched_on     # Return watched timestamp
    def get_progress_pct(self):   return self.__progress_pct   # Return progress %

    def set_progress_pct(self, p):    # Setter for progress
        if not (0 <= p <= 100):      # Validate range
            raise ValueError("Progress must be between 0 and 100.")  # Error if invalid
        self.__progress_pct = p      # Update progress

    def __str__(self):               # String representation
        return (
            f"[{self.__watched_on.strftime('%Y-%m-%d')}]"  # Show date
            f" {self.__content_title} — {self.__progress_pct:.0f}% watched"  # Show title and progress
        )


# ─────────────────────────────────────────────────────────────
class Notification:
    """An in-app notification message."""  # Class description

    def __init__(self, notif_id, message, notif_type="general"):  # Constructor
        self.__notif_id   = notif_id        # Unique notification ID
        self.__message    = message         # Notification message
        self.__notif_type = notif_type      # Type (general, subscription, etc.)
        self.__sent_at    = datetime.now()  # Timestamp of notification
        self.__is_read    = False           # Read status (default unread)

    def get_notif_id(self):    return self.__notif_id    # Return ID
    def get_message(self):     return self.__message     # Return message
    def get_notif_type(self):  return self.__notif_type  # Return type
    def get_sent_at(self):     return self.__sent_at     # Return timestamp
    def get_is_read(self):     return self.__is_read     # Return read status

    def set_message(self, m):  self.__message = m        # Update message
    def set_is_read(self, b):  self.__is_read = b        # Update read status
    def mark_read(self):       self.__is_read = True     # Mark as read

    def __str__(self):         # String representation
        status = "Read" if self.__is_read else "Unread"  # Determine read/unread
        return (
            f"[{status}][{self.__notif_type.upper()}]"  # Show status and type
            f" {self.__sent_at.strftime('%Y-%m-%d %H:%M')} — {self.__message}"  # Show timestamp and message
        )


# ─────────────────────────────────────────────────────────────
class Feedback:
    """A user's rating and review for content."""  # Class description

    def __init__(self, feedback_id, content_id, rating, comment=""):  # Constructor
        if not (1 <= rating <= 5):     # Validate rating range
            raise ValueError("Rating must be 1 to 5.")  # Error if invalid
        self.__feedback_id  = feedback_id   # Unique feedback ID
        self.__content_id   = content_id    # Content ID
        self.__rating       = rating        # Rating value (1–5)
        self.__comment      = comment       # Optional comment
        self.__submitted_at = datetime.now()  # Timestamp

    def get_feedback_id(self):   return self.__feedback_id   # Return ID
    def get_content_id(self):    return self.__content_id    # Return content ID
    def get_rating(self):        return self.__rating        # Return rating
    def get_comment(self):       return self.__comment       # Return comment
    def get_submitted_at(self):  return self.__submitted_at  # Return timestamp

    def set_rating(self, r):        # Setter for rating
        if not (1 <= r <= 5):       # Validate rating
            raise ValueError("Rating must be 1 to 5.")  # Error if invalid
        self.__rating = r           # Update rating

    def set_comment(self, c):    self.__comment = c   # Update comment

    def __str__(self):           # String representation
        stars = "★" * self.__rating + "☆" * (5 - self.__rating)  # Create star rating
        return f"[Feedback {self.__feedback_id}] {stars} — {self.__comment}"  # Display feedback


# ─────────────────────────────────────────────────────────────
class User:
    """Base class for all StreamFlix users."""  # Parent class

    def __init__(self, user_id, name, email, password_hash=""):  # Constructor
        if "@" not in email:   # Validate email format
            raise ValueError(f"Invalid email: {email}")  # Error if invalid
        self.__user_id       = user_id        # Unique user ID
        self.__name          = name           # User name
        self.__email         = email          # Email
        self.__password_hash = password_hash  # Password (hashed)
        self.__is_active     = True           # Account active status
        self.__created_at    = datetime.now() # Account creation timestamp
        self.__notifications = []             # List of notifications

    def get_user_id(self):        return self.__user_id
    def get_name(self):           return self.__name
    def get_email(self):          return self.__email
    def get_password_hash(self):  return self.__password_hash
    def get_is_active(self):      return self.__is_active
    def get_notifications(self):  return list(self.__notifications)  # Return copy

    def set_name(self, n):           self.__name = n
    def set_email(self, e):
        if "@" not in e:  # Validate email
            raise ValueError(f"Invalid email: {e}")
        self.__email = e
    def set_password_hash(self, h):  self.__password_hash = h
    def set_is_active(self, b):      self.__is_active = b

    def add_notification(self, n):   # Add notification
        self.__notifications.append(n)

    def get_unread_notifications(self):  # Filter unread notifications
        return [n for n in self.__notifications if not n.get_is_read()]

    def mark_all_notifications_read(self):  # Mark all as read
        for n in self.__notifications:
            n.mark_read()

    def get_role(self):   return "User"  # Base role

    def display_info(self):  # Display user info
        status = "Active" if self.__is_active else "Inactive"
        return (
            f"[{self.get_role()}] {self.__name} <{self.__email}>\n"
            f"  ID: {self.__user_id} | Status: {status}"
            f" | Joined: {self.__created_at.strftime('%Y-%m-%d')}"
        )

    def __str__(self): return self.display_info()  # String representation


# ─────────────────────────────────────────────────────────────
class RegularUser(User):
    """Standard subscriber. Inherits from User."""  # Child class

    def __init__(self, user_id, name, email, password_hash=""):
        super().__init__(user_id, name, email, password_hash)  # Call parent constructor
        self.__subscription      = None   # Subscription object
        self.__viewing_history   = []     # List of viewing records
        self.__feedback_list     = []     # List of feedback
        self.__purchased_content = []     # List of purchased content IDs

    def get_subscription(self):       return self.__subscription
    def get_viewing_history(self):    return list(self.__viewing_history)
    def get_feedback_list(self):      return list(self.__feedback_list)
    def get_purchased_content(self):  return list(self.__purchased_content)
    def set_subscription(self, s):    self.__subscription = s

    def subscribe(self, sub):  # Subscribe to a plan
        self.__subscription = sub
        self.add_notification(Notification(
            f"notif-sub-{self.get_user_id()}",
            f"You subscribed to the {sub.get_plan().get_tier().value} plan.",
            "subscription"
        ))

    def cancel_subscription(self):  # Cancel subscription
        if not self.__subscription:
            raise RuntimeError("No subscription to cancel.")
        self.__subscription.cancel()
        self.add_notification(Notification(
            f"notif-cancel-{self.get_user_id()}",
            "Your subscription has been cancelled.",
            "subscription"
        ))

    def has_active_subscription(self):  # Check if active
        return (self.__subscription is not None
                and self.__subscription.is_active())

    def can_stream(self, content):  # Check streaming permission
        if not content.get_is_available():
            return False
        if not content.get_is_premium():
            return self.has_active_subscription()
        if content.get_content_id() in self.__purchased_content:
            return True
        if self.has_active_subscription():
            from models.subscription import PlanTier
            return self.__subscription.get_plan().get_tier() == PlanTier.PREMIUM
        return False

    def add_viewing_record(self, record):  # Add viewing history
        self.__viewing_history.append(record)

    def add_purchased_content(self, content_id):  # Add purchased content
        if content_id not in self.__purchased_content:
            self.__purchased_content.append(content_id)

    def submit_feedback(self, feedback):  # Submit feedback
        self.__feedback_list.append(feedback)

    def get_role(self):  return "RegularUser"  # Override role

    def display_info(self):  # Extended display
        base    = super().display_info()
        sub_str = (self.__subscription.get_plan().get_tier().value
                   if self.__subscription else "None")
        return (
            f"{base}\n  Subscription: {sub_str}"
            f" | History: {len(self.__viewing_history)} items"
        )

    def display_viewing_history(self):  # Show history
        if not self.__viewing_history:
            return "No viewing history yet."
        lines = [str(r) for r in self.__viewing_history]
        return "Viewing History:\n" + "\n".join(f"  {l}" for l in lines)


# ─────────────────────────────────────────────────────────────
class Administrator(User):
    """Admin account with elevated privileges. Inherits from User."""  # Admin class

    def __init__(self, user_id, name, email, password_hash="",
                 admin_level=1, department="General"):
        super().__init__(user_id, name, email, password_hash)
        self.__admin_level = admin_level   # Admin level (1–3)
        self.__department  = department    # Department name

    def get_admin_level(self):   return self.__admin_level
    def get_department(self):    return self.__department

    def set_admin_level(self, l):
        if l not in (1, 2, 3):  # Validate level
            raise ValueError("Admin level must be 1, 2, or 3.")
        self.__admin_level = l

    def set_department(self, d): self.__department = d

    def reset_user_password(self, user, new_hash):  # Reset password
        user.set_password_hash(new_hash)

    def deactivate_user(self, user):  # Deactivate account
        user.set_is_active(False)

    def toggle_content_availability(self, content):  # Toggle availability
        content.set_is_available(not content.get_is_available())

    def get_role(self):  return "Administrator"  # Override role

    def display_info(self):  # Extended display
        base = super().display_info()
        return (
            f"{base}\n  Admin Level: {self.__admin_level}"
            f" | Department: {self.__department}"
        )
