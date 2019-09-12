from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, ActivitySerializer
from .models import Activity


#데이터베이스로부터 데이터를 가져오고, 선언해둔 시리얼라이저를 통해 데이터를 직렬화해준다.
class activity(APIView):
    def get_object(self):
        return Activity.objects.get(pk=4)

    def get(self, request):
        data = self.get_object()
        serializer = ActivitySerializer(data)
        return Response(serializer.data)

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)