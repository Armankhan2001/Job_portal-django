from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from job.serializers import UserLoginSerializer,UserRegistrationSerializer,PersonalInfo,PersonalInfoSerializer
from django.contrib.auth import authenticate
from job.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# from job.renderers import UserRenderer

#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            # token = get_tokens_for_user(user)
            return Response({'msg':'Registration Successful'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response ({'token':token,'msg':'login Success'},status=status.HTTP_200_OK)
            else:
                return Response ({'errors': {'non_field_errors':['Email or Password is not Valid']}},status=status.HTTP_404_NOT_FOUND)
            

# class UserProfileView(APIView):
#     renderer_classes = [UserRenderer] 
#     permission_classes = [IsAuthenticated]
#     def get(self,request,format=None):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK) 
    


class UserPersonalInfoView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        user = request.user
        existing_info = PersonalInfo.objects.filter(user=user).first()
        if existing_info:
            return Response({'message': 'Personal information already exists for the user'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonalInfoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response({'message': 'Personal information created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        user = PersonalInfo.objects.filter(user=id)
        serializer = PersonalInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Personal information updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id , format=None):
        user =PersonalInfo.objects.filter(user=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

            

# class PersonalInfo(APIView):
#     # permission_classes = [IsAuthenticated]
#     def post(self,request):
#         serializer = PersonalInfoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         return Response({'msg':'Profile Created Successfully'},status=status.HTTP_200_OK)
