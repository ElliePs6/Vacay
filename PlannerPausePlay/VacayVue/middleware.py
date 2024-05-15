from django.shortcuts import redirect
from django.urls import reverse

class LogoutOnLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is accessing the login page
        if request.path == reverse('login'):
            # If the user is authenticated, log them out
            if request.user.is_authenticated:
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')

        response = self.get_response(request)
        return response
