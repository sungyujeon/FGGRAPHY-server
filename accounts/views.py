from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import UserSerializer, UserListSerializer
from .modules import UserSupport

User = get_user_model()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
	#1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	#1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	#2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	#3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()

        # user_genre create
        # 추후 커뮤니티 활동 시 genre별 point도 증가시키기 위함
        user_support = UserSupport()
        user_support.set_genre_user(user)

        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다.
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_top_ranked_users(request):
    user_num = int(request.GET.get('user_num'))

    users = User.objects.all().order_by('ranking')[:user_num]
    serializer = UserListSerializer(list(users), many=True)

    return Response(serializer.data)





# admin ================================================================================================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def calc_ranking(request):
    user_support = UserSupport()
    users = user_support.set_ranking()
    # serializers = UserListSerializer(list(users), many=True)
    
    data = {
        'success': True
    }
    return JsonResponse(data)
    # return Response(serializers.data)
