from main.serializers import UserSerializer, ActivitySerializer, ReviewSerializer

#토큰을 보냈을때 리턴하는 것들
def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
        #'activity': ActivitySerializer(user, context={'request': request}).data,
        #'review': ReviewSerializer(user, context={'request': request}).data,
    }