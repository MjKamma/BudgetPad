from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'budgetpad'

urlpatterns = [
    path('', views.home, name='home'),
    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    path('register/', views.handleSignup, name='register'),
    path('login/', views.handleLogin, name='login'),
    # path('budgetpad/', include('budgetpadi.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('handleLogout/', views.handleLogout, name='handleLogout'),
    path('addexpense/', views.addExpense, name='addexpense'),
    path('addexpense_submission/', views.addExpense_submission,
         name='addexpense_submission'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="home/reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="home/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="home/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetView.as_view(
        template_name="home/password_reset_done.html"), name='password_reset_complete'),
    path('expense_edit/<int:id>', views.expense_edit, name='expense_edit'),
    path('<int:id>/addmoney_update/',
         views.addExpense_update, name="addexpense_update"),
    path('expense_delete/<int:id>', views.expense_delete, name='expense_delete'),

    path('expense_month/', views.expense_month, name='expense_month'),
    path('stats/', views.stats, name='stats'),
    path('expense_week/', views.expense_week, name='expense_week'),
    path('weekly/', views.weekly, name='weekly'),
    path('check/', views.check, name="check"),
    path('<int:id>/profile_edit/', views.profile_edit, name="profile_edit"),
    path('<int:id>/profile_update/', views.profile_update, name="profile_update"),
    path('info/', views.info, name="info"),
    path('info_year/', views.info_year, name="info_year"),
    path('calculator/', views.calculator, name='calculator'),
]
