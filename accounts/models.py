from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.db import transaction
from djstripe.models import Customer, Subscription

class CustomUserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fireid = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True, auto_now=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL,help_text="The user's Stripe Subscription object, if it exists")

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserCreditTransaction(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('hold', 'Hold'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        # Add more status choices as needed (e.g., 'refunded', 'canceled', etc.)
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('refund','Refund')
    ]

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_datetime = models.DateTimeField(auto_now_add=True)
    # request_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    credits_balance = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    refund_reference = models.UUIDField(null=True, blank=True)  # Reference to the original transaction for refunds
    def __str__(self):
        return f"Transaction ID: {self.transaction_id} - User: {self.user.email}"

    class Meta:
        ordering = ['-transaction_datetime']

    def add_log(self, user, transaction_amount, transaction_type, refund_reference=None):
        """
        Add a new log entry for a user's credit transaction.

        Args:
            user (User): The user involved in the transaction.
            transaction_amount (Decimal): The amount of credits involved in the transaction.
            transaction_type (str): The type of transaction (e.g., 'credit', 'debit', 'refund').
            refund_reference (UUID, optional): Reference to the original transaction for refunds.

        Returns:
            UserCreditTransaction: The created transaction log entry.
        """
        with transaction.atomic():
            # Calculate the new credits balance based on the transaction type
            last_transaction = UserCreditTransaction.objects.filter(user=user).order_by('-transaction_datetime').first()

            if last_transaction:
                credits_balance = last_transaction.credits_balance  # Start with the previous balance
                if transaction_type == 'credit':
                    credits_balance += transaction_amount
                elif transaction_type == 'debit':
                    if credits_balance - transaction_amount < 0:
                        raise ValueError("Debit transaction would result in a negative balance.")
                    credits_balance -= transaction_amount
                elif transaction_type == 'refund':
                    refunded_transaction = UserCreditTransaction.objects.filter(transaction_id=refund_reference).first()
                    if refunded_transaction:
                        credits_balance += refunded_transaction.transaction_amount
            else:
                # This is the user's first transaction log, assume the balance was zero
                if transaction_type == 'credit':
                    credits_balance = transaction_amount
                elif transaction_type == 'debit':
                    # if -transaction_amount < 0:
                    raise ValueError("Debit transaction would result in a negative balance.")
                    # credits_balance = -transaction_amount
                elif transaction_type == 'refund':
                    # Handle refunds for the first transaction (if needed)
                    credits_balance = 0

            # Create and save the transaction log entry
            new_log_entry = UserCreditTransaction(
                user=user,
                transaction_amount=transaction_amount,
                transaction_type=transaction_type,
                refund_reference=refund_reference,
                credits_balance=credits_balance
            )
            new_log_entry.save()

            return new_log_entry

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self.create_user(email, password, **extra_fields)

# class User(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     fireid = models.CharField(max_length=200, unique=True)
#     name = models.CharField(max_length=200, blank=True, null=True)
#     username = models.CharField(max_length=150, unique=True, blank=True, null=True)
#     surname = models.CharField(max_length=200, blank=True, null=True)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=20, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(blank=True, null=True, auto_now=True)
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'

#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

# class JwtCsrfTokens(models.Model):
#     jwt_token = models.CharField(max_length=5000)
#     csrf_token = models.CharField(max_length=5000)