from django import forms
from .models import UserProfile
from .models import AddExpense_info
from django.utils import timezone
from django.contrib.auth.forms import UserChangeForm


PROFESSION_CHOICES = [
    ('Employee', 'Employee'),
    ('Business', 'Business'),
    ('Student', 'Student'),
    ('Others', 'Others'),
]
SELECT_CATEGORY_CHOICES = [
    ("Rent", "Rent"),
    ("Electricity", "Electricity"),
    ("Groceries", "Groceries"),
    ("TV", "TV"),
    ("Data", "Data"),
    ("Bolt", "Bolt"),
    ("Other", "Other"),
]


class UserProfileForm(UserChangeForm):
    profession = forms.ChoiceField(choices=PROFESSION_CHOICES)
    income = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profession', 'income']
    # fname = forms.CharField(label='First Name', max_length=100)
    # lname = forms.CharField(label='Last Name', max_length=100)
    # profession = forms.ChoiceField(
    #    label='Profession', choices=PROFESSION_CHOICES)
    # income = forms.IntegerField(label='Income')


class AddExpenseForm(forms.ModelForm):
    category = forms.ChoiceField(choices=SELECT_CATEGORY_CHOICES)

    class Meta:
        model = AddExpense_info
        fields = ['add_expense', 'amount', 'due_date', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        # Add expense_number as a hidden input field
        widgets.update({
            'expense_number': forms.HiddenInput()})
        labels = {
            'add_expense': 'Expense Name',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Set the 'date' field to the current date
        instance.date = timezone.now().date()
        if commit:
            instance.save()
        return instance
    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
    """
