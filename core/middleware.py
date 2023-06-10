from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin


class ProcessRequestMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if "insights" in request.path:
            user = request.user
            if not user.is_authenticated:
                messages.error(request, "Your need to log in to access this page!")
                return redirect("home")