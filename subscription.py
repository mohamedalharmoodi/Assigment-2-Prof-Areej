# ============================================================
# File: models/subscription.py
# Classes: PlanTier, SubscriptionStatus, SubscriptionPlan,
#          Subscription
# ============================================================

# Importing date utilities for handling subscription dates
from datetime import date, timedelta

# Importing Enum to define fixed constant values
from enum import Enum


# ─────────────────────────────────────────────────────────────
# Enum class representing different subscription tiers
class PlanTier(Enum):
    """Enumeration for subscription plan types."""

    BASIC    = "Basic"      # Basic plan with limited features
    STANDARD = "Standard"   # Standard plan with moderate features
    PREMIUM  = "Premium"    # Premium plan with full features


# ─────────────────────────────────────────────────────────────
# Enum class representing subscription status
class SubscriptionStatus(Enum):
    """Enumeration for tracking subscription lifecycle status."""

    ACTIVE    = "Active"      # Subscription is currently valid
    EXPIRED   = "Expired"     # Subscription has passed end date
    CANCELLED = "Cancelled"   # Subscription manually cancelled


# ─────────────────────────────────────────────────────────────
# Class representing a reusable subscription plan template
class SubscriptionPlan:
    """
    Represents a subscription plan (e.g., Basic, Standard, Premium).

    This class acts as a blueprint for plans that users can subscribe to.
    It defines pricing, streaming limits, and quality features.
    """

    # Constructor to initialize plan attributes
    def __init__(self, plan_id, tier, monthly_price, max_streams,
                 hd_available, ultra_hd_available, description=""):

        # Unique ID for the plan
        self.__plan_id             = plan_id

        # Plan tier (Basic / Standard / Premium)
        self.__tier                = tier

        # Monthly subscription cost
        self.__monthly_price       = monthly_price

        # Maximum simultaneous streams allowed
        self.__max_streams         = max_streams

        # Whether HD streaming is available
        self.__hd_available        = hd_available

        # Whether Ultra HD (4K) is available
        self.__ultra_hd_available  = ultra_hd_available

        # Additional description of plan features
        self.__description         = description

    # ── Getters (Encapsulation: read-only access) ─────────────

    def get_plan_id(self):             return self.__plan_id
    def get_tier(self):                return self.__tier
    def get_monthly_price(self):       return self.__monthly_price
    def get_max_streams(self):         return self.__max_streams
    def get_hd_available(self):        return self.__hd_available
    def get_ultra_hd_available(self):  return self.__ultra_hd_available
    def get_description(self):         return self.__description

    # ── Setters (Controlled modification) ─────────────────────

    # Update price with validation
    def set_monthly_price(self, p):
        if p < 0:
            raise ValueError("Price cannot be negative.")
        self.__monthly_price = p

    # Update max streams allowed
    def set_max_streams(self, n):          self.__max_streams = n

    # Enable/disable HD streaming
    def set_hd_available(self, b):         self.__hd_available = b

    # Enable/disable Ultra HD streaming
    def set_ultra_hd_available(self, b):   self.__ultra_hd_available = b

    # Update plan description
    def set_description(self, d):          self.__description = d

    # Display formatted plan details
    def display_plan(self):

        # Default streaming quality
        quality = "SD"

        # Determine highest available quality
        if self.__ultra_hd_available:
            quality = "4K"
        elif self.__hd_available:
            quality = "HD"

        # Return formatted string
        return (
            f"Plan: {self.__tier.value} | ${self.__monthly_price:.2f}/mo"
            f" | Streams: {self.__max_streams} | Quality: {quality}"
            f"\n  {self.__description}"
        )

    # String representation of plan
    def __str__(self): 
        return self.display_plan()


# ─────────────────────────────────────────────────────────────
# Class representing an individual user's subscription
class Subscription:
    """
    Represents a user's subscription instance.

    This class links a user to a SubscriptionPlan and manages
    lifecycle operations like upgrade, cancel, renew, and validation.
    """

    # Constructor to initialize subscription
    def __init__(self, subscription_id, plan,
                 start_date=None, duration_days=30, auto_renew=True):

        # Unique subscription ID
        self.__subscription_id = subscription_id

        # Reference to SubscriptionPlan (Aggregation relationship)
        self.__plan            = plan

        # Start date (defaults to today)
        self.__start_date      = start_date or date.today()

        # End date calculated using duration
        self.__end_date        = self.__start_date + timedelta(days=duration_days)

        # Initial status is ACTIVE
        self.__status          = SubscriptionStatus.ACTIVE

        # Whether subscription auto-renews
        self.__auto_renew      = auto_renew

    # ── Getters ──────────────────────────────────────────────

    def get_subscription_id(self):  return self.__subscription_id
    def get_plan(self):             return self.__plan
    def get_start_date(self):       return self.__start_date
    def get_end_date(self):         return self.__end_date
    def get_status(self):           return self.__status
    def get_auto_renew(self):       return self.__auto_renew

    # ── Setters ──────────────────────────────────────────────

    # Update plan (used in upgrade/downgrade)
    def set_plan(self, p):          self.__plan = p

    # Update end date manually
    def set_end_date(self, d):      self.__end_date = d

    # Update status (ACTIVE / EXPIRED / CANCELLED)
    def set_status(self, s):        self.__status = s

    # Enable/disable auto-renew
    def set_auto_renew(self, b):    self.__auto_renew = b

    # ── Business Logic Methods ───────────────────────────────

    # Check if subscription is still valid
    def is_active(self):
        """Check if subscription is currently valid."""

        # If not active, return False
        if self.__status != SubscriptionStatus.ACTIVE:
            return False

        # If current date exceeds end date → mark expired
        if date.today() > self.__end_date:
            self.__status = SubscriptionStatus.EXPIRED
            return False

        return True

    # Upgrade to a new plan
    def upgrade(self, new_plan):
        """Switch to a different plan."""

        # Prevent upgrading to same plan
        if new_plan.get_tier() == self.__plan.get_tier():
            raise ValueError("Already on this plan.")

        self.__plan = new_plan

    # Cancel subscription
    def cancel(self):
        """Cancel this subscription."""

        # Change status and disable auto-renew
        self.__status     = SubscriptionStatus.CANCELLED
        self.__auto_renew = False

    # Renew subscription
    def renew(self, duration_days=30):
        """Renew for another period."""

        # Reset dates and status
        self.__start_date = date.today()
        self.__end_date   = self.__start_date + timedelta(days=duration_days)
        self.__status     = SubscriptionStatus.ACTIVE

    # Display formatted subscription info
    def display_info(self):
        return (
            f"Subscription [{self.__subscription_id}]\n"
            f"  Plan: {self.__plan.get_tier().value}"
            f" | Status: {self.__status.value}\n"
            f"  Valid: {self.__start_date} to {self.__end_date}"
            f" | Auto-Renew: {self.__auto_renew}"
        )

    # String representation
    def __str__(self): 
        return self.display_info()
