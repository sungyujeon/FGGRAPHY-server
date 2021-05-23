from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserSerializer, UserDataSerializer
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


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_or_update_or_delete_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        serializer = UserDataSerializer(user)
        return Response(serializer.data)
    elif request.user == user:  # 로그인한 사용자와 수정/삭제하려는 사용자가 일치할 때
        if request.method == 'PUT':
            print('???????? 왜 회원정보 수정이 안되는거야...')
            
            # serializer = UserSerializer(user, data=request.data)
            # print(serializer)
            # if serializer.is_valid(raise_exception=True):
            #     serializer.save()
            #     user.set_password(request.data.get('password'))
            #     user.save()
            #     return Response(serializer.data)
            data = {
                'success': False,
                'status': 'updated',
            }
            return JsonResponse(data)
        elif request.method == 'DELETE':
            user.delete()
            data = {
                'success': True,
                'status': 'deleted',
            }
            return JsonResponse(data)
    else:
        data = {
            'success': False,
            'message': '사용자가 일치하지 않습니다.',
        }
        return JsonResponse(data)

# ranking
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_top_ranked_users(request):
    user_num = int(request.GET.get('user_num'))

    users = User.objects.all().order_by('ranking')[:user_num]
    serializer = UserDataSerializer(list(users), many=True)

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