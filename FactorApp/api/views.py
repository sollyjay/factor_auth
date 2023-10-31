from rest_framework.views import APIView
from FactorApp.api.permissions import IsOwnerOrReadOnly
from FactorApp.api.serializers import (ChangePasswordSerializer, FollowSerializer, FollowingSerializer, LikePostSerializer, LoginSerializer, PostSerializer, ProfileUpdateSerializer, RegistrationSerializer, UnLikePostSerializer, UserAvatarSerializer,)
from FactorApp.models import Follow, Following, User, Post
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status, authentication
from django.contrib import messages
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from FactorApp.video_capture import face_capture
from FactorApp.recognizer import Recognizer
from rest_framework.permissions import IsAuthenticated

class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class RegistrationView(CreateAPIView):
    """
    This API EndPoint Register a new User
    """
    serializer_class = RegistrationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            face_capture(serializer.validated_data['email'], 'register')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            messages.error(request, serializer.errors)      
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    """
    This API EndPoint Login User
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        detail = {'email': serializer.validated_data['email']}
        
        user = User.objects.get(email__iexact=serializer.data['email'])
        
        auth_user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
        print("Is User Authenticated?****", auth_user)
        
        if auth_user:
            face_capture(serializer.validated_data['email'], 'login')
            recognized = Recognizer(detail)
            print("Recognized********", recognized)

            if recognized:
                login(request, user)
                response = {
                    'success' : 'True',
                    'status code' : status.HTTP_200_OK,
                    'message': 'User logged in  successfully',
                    'user' : serializer.data['email']
                }
                messages.success(request, 'Login Successfully')
                return Response(response, status=status.HTTP_200_OK)
            else:
                messages.error(request, 'Face Not Recognized')
                return Response({'message': 'Face Not Recognized', 'status': 'False'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            messages.error(request, 'Invalid Login Details!')
            return Response({'message': 'Invalid Login Details!', 'status': 'False'}, status=status.HTTP_400_BAD_REQUEST)

    """
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        detail = {'email': serializer.validated_data['email']}
        names = Recognizer(detail)
        user = User.objects.get(email__iexact=serializer.data['email'])        
        if str(user.email) in names:
            login(request, user)
            response = {
                'success' : 'True',
                'status code' : status.HTTP_200_OK,
                'message': 'User logged in  successfully',
                'user' : serializer.data['email']
            }
            messages.success(request, 'Login Successfully')
            return Response(response, status=status.HTTP_200_OK)
        else:
            messages.error(request, 'Face Not Recognized')
            return Response({'message': 'Face Not Recognized', 'status': 'False'}, status=status.HTTP_200_OK)
    """


class LogoutView(APIView):
    """
    This API EndPoint Logout a User
    """
    def post(self, request):
        logout(request)
        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'User Successfully Logout!'
        }
        return response


class UserAvatarUpload(CreateAPIView):
    queryset = User.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj

    def post(self, request, format=None):
        instance = self.get_object()
        serializer = UserAvatarSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Profile Updated Succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Updated Succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# POST
class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'Message': 'Posted Succesfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePostCreateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = LikePostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, post_id):
        queryset = self.get_queryset()      
        obj = get_object_or_404(queryset, id=int(post_id))
        return obj
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object(request.data['post_id'])
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnLikePostCreateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = UnLikePostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, post_id):
        queryset = self.get_queryset()      
        obj = get_object_or_404(queryset, id=int(post_id))
        return obj
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object(request.data['post_id'])
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserAPIView(UpdateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, user_id):
        queryset = self.get_queryset()    
        obj = get_object_or_404(queryset, id=int(user_id))
        return obj
    
    def get_following_serializer(self, request, *args, **kwargs):
        instance = Following.objects.get(id=request.data['id_'])
        return FollowingSerializer(instance = instance, 
                                    data = request.data, 
                                    context = {'request': request,
                                    'user_id': request.data['user_id']})
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object(request.data['user_id'])
        follow_serializer = self.get_serializer(instance, data=request.data, context={'request': request})
        following_serializer = self.get_following_serializer(request)
        if follow_serializer.is_valid() and following_serializer.is_valid():
            follow_serializer.save()
            following_serializer.save()
            return Response({'follower': follow_serializer.data, 'following': following_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'follower': follow_serializer.errors, 'following': following_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FollowingUserAPIView(UpdateAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, id_):
        queryset = self.get_queryset()    
        obj = get_object_or_404(queryset, id=int(id_))
        return obj
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object(request.data['id_'])
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

