from .serializers import ProfileSerializer, SignupSerializer
from rest_framework.views import APIView
from ..models import Profile
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from ..forms import SignUpForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class SignupApiView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            form = SignUpForm(data=serializer.validated_data)
            if form.is_valid():
                user = form.save()
                return Response(
                    {
                        'username': user.username,
                        'id': user.id,
                        # 'first_name': user.first_name,
                        # 'last_name': user.last_name,
                        # 'email': user.email
                    }, status=HTTP_201_CREATED
                )
            else:
                return Response(form.errors, status=HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileCreateApiView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        mobile = request.data.get('mobile')
        # checks if user_id  provided in the request data
        if not user_id:
            message = {'error': "user_id required"}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        # checks if a user with the given user_id exists in the database.
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            message = {'error': "No such user exist"}
            return Response(message, status=HTTP_400_BAD_REQUEST)

        # checks if a profile already exists for the retrieved user
        if Profile.objects.filter(user=user).exists():
            message = {'error': "Profile already exist"}
            return Response(message, status=HTTP_400_BAD_REQUEST)

            # update the provided user details
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        # create profile with associated user
        profile = Profile.objects.create(user=user, mobile=mobile)
        # serialize the profile data
        serializer = ProfileSerializer(profile)
        response = {'message': "profile created successfully", 'status': "success", 'data': serializer.data}
        return Response(response, status=HTTP_201_CREATED)


class ProfileUpdateApiView(APIView):
    def put(self, request):
        user_id = request.data.get('user_id')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        email = request.data.get('email', '')
        mobile = request.data.get('mobile', '')
        # checks if user_id is provided or not
        if not user_id:
            message = {'error': "valid user_id required"}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        # checks if user id is present in database
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            message = {'error': "User does not exist"}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            message = {'error': f"profile does not exist for user_id {user_id}"}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        #  so if the profile exist with provided user id then update given fields

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()

        if mobile:
            profile.mobile = mobile
            profile.save()
        serializer = ProfileSerializer(profile)
        response = {'message': "profile updated successfully", 'status': "success", 'data': serializer.data}
        return Response(response, status=HTTP_200_OK)


class ProfileDeleteApiView(APIView):
    def delete(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            message = {'error': "valid user_id required"}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            message = {'error': "user does not exist"}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            message = {'error': "Profile does not exist"}
            return Response(message, status=HTTP_400_BAD_REQUEST)

        profile.delete()
        response = {'message': "Profile deleted successfully", 'status': "success"}
        return Response(response, status=HTTP_200_OK)


class ProfileDetailApiView(APIView):
    def get(self, request, user_id=None):

        if user_id is not None:
            if Profile.objects.filter(user_id=user_id).exists():
                profile = Profile.objects.get(user_id=user_id)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response({'error': "profile not found"}, status=HTTP_400_BAD_REQUEST)
        else:
            profiles = Profile.objects.all()
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
