# ============================================================
# File: models/catalogue.py
# Classes: ContentCatalogue, StreamingService
# ============================================================

from models.content  import Content                         # Import Content class
from models.user     import RegularUser, ViewingRecord, Notification  # Import user-related classes
from models.payment  import Payment, Invoice, PaymentMethod # Import payment-related classes


class ContentCatalogue:
    """Stores and manages all video content."""  # Class description

    def __init__(self):
        self.__catalogue = {}   # Dictionary to store content (key: content_id, value: Content object)

    def get_all_content(self):
        return list(self.__catalogue.values())  # Return all content as a list

    def get_content_by_id(self, content_id):
        if content_id not in self.__catalogue:  # Check if content exists
            raise KeyError("Content '" + content_id + "' not found.")  # Raise error if not found
        return self.__catalogue[content_id]  # Return the content object

    def add_content(self, content):
        if content.get_content_id() in self.__catalogue:  # Check duplicate ID
            raise ValueError("Content ID '" + content.get_content_id() + "' already exists.")  # Error if duplicate
        self.__catalogue[content.get_content_id()] = content  # Add content to dictionary
        print("  [Catalogue] Added: '" + content.get_title() + "'")  # Print confirmation

    def remove_content(self, content_id):
        if content_id not in self.__catalogue:  # Check if exists
            raise KeyError("Content '" + content_id + "' not found.")  # Error if missing
        title = self.__catalogue[content_id].get_title()  # Get title before deletion
        del self.__catalogue[content_id]  # Remove content
        print("  [Catalogue] Removed: '" + title + "'")  # Print confirmation

    def update_availability(self, content_id, available):
        c = self.get_content_by_id(content_id)  # Fetch content
        c.set_is_available(available)  # Update availability status
        state = "available" if available else "unavailable"  # Determine state text
        print("  [Catalogue] '" + c.get_title() + "' marked " + state + ".")  # Print update

    def search_by_title(self, keyword):
        kw = keyword.lower()  # Convert keyword to lowercase
        return [c for c in self.__catalogue.values()  # Loop through all content
                if kw in c.get_title().lower()]  # Match keyword in title

    def filter_by_genre(self, genre):
        return [c for c in self.__catalogue.values()  # Loop through content
                if c.get_genre().lower() == genre.lower()]  # Match genre

    def filter_available(self):
        return [c for c in self.__catalogue.values()  # Loop through content
                if c.get_is_available()]  # Return only available content

    def display_catalogue(self):
        if not self.__catalogue:  # Check if empty
            return "Catalogue is empty."  # Return message
        return "\n\n".join(str(c) for c in self.__catalogue.values())  # Join all content strings

    def __len__(self):
        return len(self.__catalogue)  # Return number of content items


class StreamingService:
    """Handles streaming, purchases, and subscription billing."""  # Class description

    def __init__(self, catalogue):
        self.__catalogue       = catalogue  # Store catalogue reference
        self.__payment_counter = 1000       # Counter for payment IDs
        self.__invoice_counter = 2000       # Counter for invoice IDs
        self.__record_counter  = 3000       # Counter for viewing records

    def get_catalogue(self):
        return self.__catalogue  # Return catalogue

    def set_catalogue(self, c):
        self.__catalogue = c  # Set/replace catalogue

    def stream_content(self, user, content_id):
        """Stream content for a user if eligible."""  # Method description
        content = self.__catalogue.get_content_by_id(content_id)  # Fetch content

        if not user.can_stream(content):  # Check permission
            if not content.get_is_available():  # If content unavailable
                raise PermissionError("'" + content.get_title() + "' is currently unavailable.")  # Error
            raise PermissionError("Access denied. Upgrade plan or purchase '" + content.get_title() + "' to stream.")  # Error

        self.__record_counter += 1  # Increment record counter
        record = ViewingRecord(  # Create viewing record
            "rec-" + str(self.__record_counter),  # Record ID
            content_id,  # Content ID
            content.get_title()  # Content title
        )
        user.add_viewing_record(record)  # Add record to user history

        return "Now streaming: '" + content.get_title() + "' (" + content.get_content_type() + ") for " + user.get_name()  # Return message

    def purchase_content(self, user, content_id, method, discount=0.0):
        """Buy premium content. Returns an Invoice."""  # Method description
        content = self.__catalogue.get_content_by_id(content_id)  # Fetch content

        if not content.get_is_premium():  # Check if premium
            raise ValueError("'" + content.get_title() + "' is not premium content.")  # Error

        if content_id in user.get_purchased_content():  # Check if already purchased
            raise ValueError("You already purchased '" + content.get_title() + "'.")  # Error

        self.__payment_counter += 1  # Increment payment counter
        payment = Payment(  # Create payment
            "pay-" + str(self.__payment_counter),  # Payment ID
            user.get_user_id(),  # User ID
            content.get_price(),  # Content price
            method,  # Payment method
            "Purchase: " + content.get_title()  # Description
        )
        payment.process()  # Process payment

        self.__invoice_counter += 1  # Increment invoice counter
        invoice = Invoice(  # Create invoice
            "inv-" + str(self.__invoice_counter),  # Invoice ID
            content.get_price(),  # Subtotal
            discount,  # Discount
            payment_id=payment.get_payment_id(),  # Link payment
            description="Purchase: " + content.get_title()  # Description
        )

        user.add_purchased_content(content_id)  # Add content to user's purchased list

        user.add_notification(Notification(  # Notify user
            "notif-pay-" + str(self.__payment_counter),  # Notification ID
            "Payment confirmed: $" + str(round(invoice.get_total(), 2)) + " for '" + content.get_title() + "'.",  # Message
            "payment"  # Type
        ))

        return invoice  # Return invoice

    def process_subscription_payment(self, user, method, discount=0.0):
        """Bill user for their current subscription. Returns an Invoice."""  # Method description
        if not user.has_active_subscription():  # Check active subscription
            raise RuntimeError("User has no active subscription to bill.")  # Error

        plan = user.get_subscription().get_plan()  # Get subscription plan

        self.__payment_counter += 1  # Increment payment counter
        payment = Payment(  # Create payment
            "pay-" + str(self.__payment_counter),  # Payment ID
            user.get_user_id(),  # User ID
            plan.get_monthly_price(),  # Plan price
            method,  # Payment method
            "Subscription: " + plan.get_tier().value + " Plan"  # Description
        )
        payment.process()  # Process payment

        self.__invoice_counter += 1  # Increment invoice counter
        invoice = Invoice(  # Create invoice
            "inv-" + str(self.__invoice_counter),  # Invoice ID
            plan.get_monthly_price(),  # Subtotal
            discount,  # Discount
            payment_id=payment.get_payment_id(),  # Link payment
            description="Subscription: " + plan.get_tier().value + " Plan"  # Description
        )

        user.add_notification(Notification(  # Notify user
            "notif-renewal-" + str(self.__payment_counter),  # Notification ID
            "Subscription renewed. Invoice #" + invoice.get_invoice_id() + " total: $" + str(round(invoice.get_total(), 2)) + ".",  # Message
            "payment"  # Type
        ))

        return invoice  # Return invoice
