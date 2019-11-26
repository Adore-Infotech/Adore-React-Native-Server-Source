import phonenumbers
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')

class UserProfileSerializer(serializers.ModelSerializer):
    User = UserSerializer(read_only=True)
    ProfileImg = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        
    def get_ProfileImg(self, obj):
        return self.context['request'].build_absolute_uri(obj.ProfileImg)

class TokenAuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserProfileSerializer(UserProfile.objects.get(User=request.user),context={'request': request})
        return Response(serializer.data)

def is_email(string):
    from django.core.exceptions import ValidationError
    from django.core.validators import EmailValidator

    validator = EmailValidator()
    try:
        validator(string)
    except ValidationError:
        return False

    return True 

def RegisterUser(Email,ISDCode,PhoneNo,FirstName,LastName):
    status=False
    msg=''
    Email = str(Email).lower()
    PhoneNo = ISDCode+PhoneNo
    if carrier._is_mobile(number_type(phonenumbers.parse("+"+PhoneNo))):
        try:
            user = User.objects.get(username=PhoneNo,)
            msg='Phone number already exits.'
        except User.DoesNotExist:
            try:
                password=User.objects.make_random_password(length=6)
                new_user = User.objects.create_user(PhoneNo, Email, password)
                new_user.first_name = FirstName
                new_user.last_name = LastName
                new_user.save()
                
                
                userProfile = UserProfile()
                userProfile.User=new_user
                userProfile.save()
                status=True
                
                msg='Sign Up Success. Please check your email for login credentials.'
            except Exception as e:
                print(e)
                msg='An error occured. Please try later.'
                
    else:
        msg='Please use a valid Phone number.'
    
    
    return {'isSuccess':status,'msg':msg}



class SignUpView(APIView):
        
    def post(self,request):
        
        FirstName = request.POST['firstname']
        LastName = request.POST['lastname']
        Email = request.POST['email']
        ISDCode = request.POST['isdcode']
        PhoneNo = request.POST['phoneno']
        
        result=RegisterUser(Email,ISDCode,PhoneNo,FirstName,LastName)
        return Response(result)        