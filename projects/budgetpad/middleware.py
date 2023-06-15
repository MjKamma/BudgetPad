from django.shortcuts import redirect, render
from django.urls import reverse
from .models import UserProfile


"""class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.userprofile.profile_completed:
                # Redirect the user to the profile update page if their profile is not completed
                if request.path != reverse('profile_edit'):
                    return render(request, 'budgetpad/profile_update.html')
            # else:
                # Redirect the user to the profile page if their profile is completed
                # if request.path != reverse(''):
                    # return redirect('')
            return render(request, '')
        response = self.get_response(request)
        return response"""
