from .redis import is_rate_limited
from django.http import JsonResponse

class RedisRateLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = (
            request.user.id
            if request.user.is_authenticated
            else request.META["REMOTE_ADDR"]
        )

        if is_rate_limited(user):
            return JsonResponse(
                {"detail": "Rate limit exceeded"},
                status=429
            )

        return self.get_response(request)