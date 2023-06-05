from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import random
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from .models import OTP , OTP_temp
#region UserSignUp    
class UserSignup(APIView):
    def post(self, request):
        serializer = userserilizer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Wrong input error'})
        phone_number = serializer.validated_data['username']
        otp = request.data.get('otp', None)
        
        if not otp:
            return Response({'status': 400, 'message': 'OTP not provided'})
        
        otp_obj = OTP_temp.objects.filter(phone_number=phone_number, otp=str(otp)).first()
        if not otp_obj:
            return Response({'status': 403, 'message': 'Invalid OTP'})
        
        user = serializer.save()
        token_obj, _ = Token.objects.get_or_create(user=user)
        
        otp_obj.delete()  # Delete the OTP object after successful signup
        
        return Response({'status': 200, 'payload': serializer.data, 'message': 'User created successfully', 'token': str(token_obj)})
    
    
    
    
    
    
    
    
    
    
    
    
#endregion


#region CheckPhone

class CheckUsername(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        
        if username:
            existing_users = User.objects.filter(username=username)
            if existing_users.exists():
                return Response({'status': 400, 'message': 'Username exists'})
            else:
                
                otp = generate_otp()
                OTP_temp.objects.create(phone_number=username, otp=str(otp))
                print(otp)
                ## sending otp code goes here 
                
                return Response({'status': 200, 'message': 'Username does not exist ready to go'})
        else:
            return Response({'status': 403, 'message': 'Username not provided'})
#endregion





def generate_otp():
    return random.randint(100000, 999999)





#region forgot_password
class ForgotPassword(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                otp = generate_otp()
                print(otp)
                OTP.objects.create(user=user, otp=str(otp))
                return Response({'status': 200, 'message': 'OTP sent successfully'})
            else:
                return Response({'status': 404, 'message': 'User not found'})
        else:
            return Response({'status': 400, 'message': 'Username not provided'})

#endregion



#region reset_password
class ResetPassword(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        otp = request.data.get('otp', None)
        new_password = request.data.get('new_password', None)
        if username and otp and new_password:
            user = User.objects.filter(username=username).first()
            if user:
                otp_obj = OTP.objects.filter(user=user, otp=str(otp)).first()
                if otp_obj:
                    user.set_password(new_password)
                    user.save()
                    otp_obj.delete() 
                    token_obj, _ = Token.objects.get_or_create(user=user)
                    # Delete the OTP object after password reset
                    return Response({'status': 200, 'message': 'Password reset successful','Token':str(token_obj)})
                else:
                    return Response({'status': 400, 'message': 'Invalid OTP'})
            else:
                return Response({'status': 404, 'message': 'User not found'})
        else:
            return Response({'status': 400, 'message': 'Missing parameters'})
        
        
#endregion










