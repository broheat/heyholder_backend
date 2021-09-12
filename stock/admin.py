from django.contrib import admin

# Register your models here.
from .models import Stock, Research, Account

admin.site.register(Stock)
admin.site.register(Research)
admin.site.register(Account)
