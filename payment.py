# ============================================================
# File: models/payment.py
# Classes: PaymentMethod, PaymentStatus, Payment, Invoice
# NOTE: Payment and Invoice are created ONLY by StreamingService
#       They have NO direct link to RegularUser
# ============================================================

from datetime import datetime      # Import datetime to track payment and invoice timestamps
from enum import Enum              # Import Enum to create fixed constant values


class PaymentMethod(Enum):         # Enum representing different payment methods
    CREDIT_CARD   = "Credit Card"  # Payment using credit card
    DEBIT_CARD    = "Debit Card"   # Payment using debit card
    PAYPAL        = "PayPal"       # Payment using PayPal
    BANK_TRANSFER = "Bank Transfer"  # Payment using bank transfer


class PaymentStatus(Enum):         # Enum representing status of a payment
    PENDING   = "Pending"          # Payment has not been processed yet
    COMPLETED = "Completed"        # Payment successfully completed
    FAILED    = "Failed"           # Payment failed during processing
    REFUNDED  = "Refunded"         # Payment was refunded


# ─────────────────────────────────────────────────────────────
class Payment:
    """Records one financial transaction on StreamFlix."""  # Class description

    def __init__(self, payment_id, user_id, amount, method, description=""):  # Constructor
        self.__payment_id  = payment_id       # Unique ID for the payment
        self.__user_id     = user_id          # ID of user who made the payment
        self.__amount      = amount           # Amount paid
        self.__method      = method           # Payment method used (Enum)
        self.__status      = PaymentStatus.PENDING  # Default status is Pending
        self.__timestamp   = datetime.now()   # Store current date & time of payment
        self.__description = description      # Optional description of payment

    # Getters
    def get_payment_id(self):   return self.__payment_id   # Return payment ID
    def get_user_id(self):      return self.__user_id      # Return user ID
    def get_amount(self):       return self.__amount       # Return payment amount
    def get_method(self):       return self.__method       # Return payment method
    def get_status(self):       return self.__status       # Return payment status
    def get_timestamp(self):    return self.__timestamp    # Return timestamp
    def get_description(self):  return self.__description  # Return description

    # Setters
    def set_amount(self, a):        # Method to update amount
        if a < 0:                  # Validate amount is not negative
            raise ValueError("Amount cannot be negative.")  # Raise error if invalid
        self.__amount = a          # Update amount

    def set_status(self, s):        self.__status = s        # Update payment status
    def set_description(self, d):   self.__description = d   # Update description

    def process(self):             # Method to process payment
        """Process the payment — marks as Completed."""  # Description
        self.__status = PaymentStatus.COMPLETED  # Mark payment as completed
        return True                # Return success

    def refund(self):              # Method to refund payment
        """Refund a completed payment."""  # Description
        if self.__status != PaymentStatus.COMPLETED:  # Only allow refund if completed
            raise RuntimeError("Only completed payments can be refunded.")  # Error if not valid
        self.__status = PaymentStatus.REFUNDED  # Update status to refunded

    def display_info(self):        # Method to display payment details
        return (
            f"Payment [{self.__payment_id}] | {self.__method.value}\n"  # Show ID and method
            f"  Amount: ${self.__amount:.2f} | Status: {self.__status.value}\n"  # Show amount and status
            f"  Time: {self.__timestamp.strftime('%Y-%m-%d %H:%M')}"  # Format timestamp
            f" | {self.__description}"  # Show description
        )

    def __str__(self): return self.display_info()  # String representation


# ─────────────────────────────────────────────────────────────
class Invoice:
    """Billing document generated after each payment."""  # Class description

    TAX_RATE_DEFAULT = 0.10   # Default tax rate (10%)

    def __init__(self, invoice_id, subtotal, discount=0.0,
                 tax_rate=None, payment_id="", description=""):  # Constructor

        self.__invoice_id  = invoice_id   # Unique invoice ID
        self.__subtotal    = subtotal     # Original price before discount/tax
        self.__discount    = discount     # Discount applied
        self.__tax_rate    = tax_rate if tax_rate is not None else self.TAX_RATE_DEFAULT  # Use given or default tax rate

        self.__tax_amount  = round((subtotal - discount) * self.__tax_rate, 2)  # Calculate tax amount
        self.__total       = round(subtotal - discount + self.__tax_amount, 2)  # Calculate final total

        self.__issued_date = datetime.now()  # Timestamp of invoice creation
        self.__payment_id  = payment_id      # Linked payment ID
        self.__description = description     # Description of invoice

    # Getters
    def get_invoice_id(self):   return self.__invoice_id   # Return invoice ID
    def get_subtotal(self):     return self.__subtotal     # Return subtotal
    def get_discount(self):     return self.__discount     # Return discount
    def get_tax_rate(self):     return self.__tax_rate     # Return tax rate
    def get_tax_amount(self):   return self.__tax_amount   # Return tax amount
    def get_total(self):        return self.__total        # Return total amount
    def get_issued_date(self):  return self.__issued_date  # Return issue date

    # Setters
    def set_discount(self, d):     # Method to update discount
        if d < 0:                 # Validate discount
            raise ValueError("Discount cannot be negative.")  # Error if invalid
        self.__discount   = d     # Update discount
        self.__tax_amount = round((self.__subtotal - d) * self.__tax_rate, 2)  # Recalculate tax
        self.__total      = round(self.__subtotal - d + self.__tax_amount, 2)  # Recalculate total

    def set_tax_rate(self, r):     # Method to update tax rate
        if not (0 <= r <= 1):     # Validate tax rate range
            raise ValueError("Tax rate must be between 0 and 1.")  # Error if invalid
        self.__tax_rate   = r     # Update tax rate
        self.__tax_amount = round((self.__subtotal - self.__discount) * r, 2)  # Recalculate tax
        self.__total      = round(self.__subtotal - self.__discount + self.__tax_amount, 2)  # Recalculate total

    def display_invoice(self):     # Method to display formatted invoice
        line = "=" * 44           # Top/bottom border line
        dash = "-" * 44           # Divider line
        return (
            f"\n{line}\n"  # Print top border
            f"   STREAMFLIX INVOICE  #{self.__invoice_id}\n"  # Invoice title with ID
            f"{line}\n"  # Border
            f"  Issued  : {self.__issued_date.strftime('%Y-%m-%d %H:%M')}\n"  # Issue date
            f"  Payment : {self.__payment_id}\n"  # Linked payment
            f"  For     : {self.__description}\n"  # Description
            f"{dash}\n"  # Divider
            f"  Subtotal : ${self.__subtotal:>8.2f}\n"  # Subtotal formatted
            f"  Discount : ${self.__discount:>8.2f}\n"  # Discount formatted
            f"  Tax({self.__tax_rate*100:.0f}%)  : ${self.__tax_amount:>8.2f}\n"  # Tax info
            f"{dash}\n"  # Divider
            f"  TOTAL    : ${self.__total:>8.2f}\n"  # Final total
            f"{line}\n"  # Bottom border
        )

    def __str__(self): return self.display_invoice()  # String representation
