from django.contrib import admin
from .models import Business, Job, Invoice, Payment, LineItem
# Register your models here.
admin.site.register(Business)
admin.site.register(Job)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(LineItem)