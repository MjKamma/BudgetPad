from django.contrib.sessions.models import Session
from django.contrib import admin

from .models import UserProfile, AddExpense_info


class AddExpense_infoAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "due_date", "category", "add_expense")


admin.site.register(AddExpense_info, AddExpense_infoAdmin)

admin.site.register(Session)

admin.site.register(UserProfile)
