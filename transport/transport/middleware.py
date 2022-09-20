from django.http import HttpResponse

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["mydata"] = ""
        response = self.get_response(request)
        return response
