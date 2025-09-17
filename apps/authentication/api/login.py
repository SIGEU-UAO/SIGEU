from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views import View
import json

class inicio_sesionAPI(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido."}, status=400)

        email = data.get("email")
        password = data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user) 
            return JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)

        return JsonResponse({"error": "No se encontró ningun usuario."}, status=401)