from main.serializers import UserSerializer, ActivitySerializer, ReviewSerializer

#토큰 검사가 이루어지는 시리얼라이저들 등록 하는듯
def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
        'activity': ActivitySerializer(user, context={'request': request}).data,
        'review': ReviewSerializer(user, context={'request': request}).data,
    }