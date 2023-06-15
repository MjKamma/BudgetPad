from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

SELECT_CATEGORY_CHOICES = [
    ("Rent", "Rent"),
    ("Electricity", "Electricity"),
    ("Groceries", "Groceries"),
    ("TV", "TV"),
    ("Data", "Data"),
    ("Bolt", "Bolt"),
    ("Other", "Other"),
]
"""ADD_EXPENSE_CHOICES = [
    ("Expense", "Expense"),
    ("Income", "Income"),
]"""
PROFESSION_CHOICES = [
    ('employee', 'Employee'),
    ('business', 'Business'),
    ('student', 'Student'),
    ('others', 'Others'),
]


class AddExpense_info(models.Model):
    user = models.ForeignKey(User,
                             default=1, on_delete=models.CASCADE)
    expense_number = models.PositiveIntegerField(default=0)
    add_expense = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=now)
    due_date = models.DateField(default=now)
    category = models.CharField(max_length=20,
                                choices=SELECT_CATEGORY_CHOICES, default='Rent')

    class Meta:
        db_table: 'addExpense'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=10,
                                  choices=PROFESSION_CHOICES)
    income = models.BigIntegerField(null=True, blank=True)
    profile_completed = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='profile_image', blank=True)
    first_name = models.CharField(max_length=30)  # Add first_name field
    last_name = models.CharField(max_length=30)   # Add last_name field

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
