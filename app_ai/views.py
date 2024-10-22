# app_ai/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .app_operations_ai import AIOperations
from rest_framework.permissions import AllowAny  # Tüm kullanıcılara izin vermek için


class AIPromptView(APIView):
    permission_classes = [AllowAny]  # İsterseniz burada yetkilendirme ekleyebilirsiniz

    def post(self, request):
        prompt = request.data.get('prompt')
        api_key = 'YOUR_OPENAI_API_KEY'  # Buraya kendi OpenAI API anahtarınızı yerleştirin

        if not prompt:
            return Response({'error': 'Prompt is required.'}, status=status.HTTP_400_BAD_REQUEST)

        ai_response = AIOperations.get_ai_response(prompt, api_key)
        return Response({'ai_response': ai_response}, status=status.HTTP_200_OK)
