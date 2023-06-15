from django.contrib import admin
from django.urls import path, include
from budgetpad import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # added this as entry point for routes to be created later
    path('budgetpad/', include('budgetpad.urls')),
    path('budgetpad/dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.handleSignup, name='register'),
    path('login/', views.handleLogin, name='login'),
    path('handleLogout/', views.handleLogout, name='handleLogout'),
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('expenses/', views.expenses, name='expenses'),
    path('addexpense/', views.addExpense, name='addexpense'),
    path('add_expense_submission/', views.addExpense_submission,
         name='add_expense_submission'),
    path('expense_edit/<int:expense_id>',
         views.expense_edit, name='expense_edit'),
    path('expense_delete/<int:expense_id>',
         views.expense_delete, name='expense_delete'),
    path('stats/', views.stats, name='stats'),
    path('calculator/', views.calculator, name='calculator'),
    path('info/', views.info, name="info"),
]
