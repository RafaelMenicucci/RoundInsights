from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ProcessRequestMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if "insights" in request.path:
            user = request.user
            if not user.is_authenticated:
                return HttpResponse('Unauthorized', status=401)