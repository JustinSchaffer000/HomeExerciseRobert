from django.db import models

# Create your models here.


class Business(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Invoice(models.Model):
    PAID = 'paid'
    UNPAID = 'unpaid'
    DRAFT = 'draft'

    STATUS_CHOICES = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid'),
        (DRAFT, 'Draft'),
    ]

    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    number = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    business = models.ForeignKey('Business', on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LineItem(models.Model):
    job = models.ForeignKey('Job', on_delete=models.RESTRICT, null=True)
    invoice = models.ForeignKey(
        'Invoice', on_delete=models.RESTRICT, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.RESTRICT, null=True)
    self_item = models.ForeignKey('self', on_delete=models.RESTRICT, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    CHECK = 'check'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'

    TYPES = [
        (CHECK, 'Check'),
        (CREDIT_CARD, 'Credit Card'),
        (DEBIT_CARD, 'Debit Card'),
    ]

    payer = models.ForeignKey(
        'Business', related_name='payments_sent', on_delete=models.RESTRICT)
    payee = models.ForeignKey(
        'Business', related_name='payments_received', on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    reference = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    initiated_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
