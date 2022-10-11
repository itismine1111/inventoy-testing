from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import SandwichSerializer, SauceSerializer
from rest_framework.response import Response



# Create your views here.

class TempCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SandwichSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Product created",
                    "data": {},
                },
                status=201,
            )
