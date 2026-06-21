from django.http import JsonResponse

    

class AdminAccessMiddleware:
    def __init__(self, get_response):
        print("AdminAccessMiddleware initialized")
        self.get_response = get_response

    def __call__(self, request):
        print("AdminAccessMiddleware called")
        print("request.path:", request.path)
        print("request.user:", request.method)

        if not request.method == "POST" and not request.method == "GET":
            return JsonResponse(
                {"error": "Invalid request method"},
                status=405
            )

        # ✅ ONLY allowed base paths
        if request.path.startswith("/accounts/") or request.path.startswith("/admin/"):
            return self.get_response(request)

        return JsonResponse(
            {"error": "Invalid request path"},
            status=403
        )