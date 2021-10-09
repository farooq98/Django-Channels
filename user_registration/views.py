from .models import UserModel
from core_files.authentication import PublicAPI, PrivateAPI
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class CreateUser(PublicAPI):

    @classmethod
    def validate_email(cls, value):
        try:
            UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            return True
        else:
            return False

    @classmethod
    def validate_password(cls, value):
        passwd = len(value)
        if passwd and passwd < 8:
            return False
        return True
    
    def post(self, request):

        data = request.data
        email = data.get("email") if self.validate_email(data.get("email")) else False
        password = data.get("password") if self.validate_password(data.get("password")) else False

        if not email or not password:
            if not email:
                message = "Email is already taken"
            elif not password:
                message = "Password must be greater than 8 characters"

            return Response({
                "created": False,
                "message": message,
            }, status=status.HTTP_400_BAD_REQUEST)
        

        user = UserModel.objects.create_user(
            email=data.get("email"), 
            password=data.get("password")
        )    

        if user:
            user.image_url = data.get("image_url")
            user.user_type = data.get("user_type")
            user.name = data.get("name")
            user.save()

            resp = {
                "created": True,
                "message": "User Created"
            }
            if settings.DEBUG:
                resp.update({"verification_code": user.verification_code})

            return Response(resp, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "created": False,
                "message": "something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

class ActivateUser(PublicAPI):

    def post(self, request):
        stat = None
        message = None
        success = None

        try:
            user = UserModel.objects.get(email=request.data.get('email'))
            user.is_active = user.validate_timeout(str(request.data.get('verification_code')))
            if user.is_active:
                user.save()
                login(request,user)
                success, message, stat = True, "email has been verified", status.HTTP_200_OK
            else:
                success, message, stat = False, "verification code has expired", status.HTTP_400_BAD_REQUEST
        
        except UserModel.DoesNotExist:
            success, message, stat = False, "No such user exists", status.HTTP_400_BAD_REQUEST

        resp = {
            "status": success,
            "message": message
        }

        if success:
            resp.update({"name": user.name, "designation": user.designation})

        return Response(resp, status=stat)

class RequestForgetPassword(PublicAPI):

    def post(self, request):
        email = request.data.get('email')
        stat = None
        message = None
        success = None

        try:
            user = UserModel.objects.get(email=email)
            user.change_password()

            success, message, stat = True, "an email with otp code is sent", status.HTTP_200_OK
        
        except UserModel.DoesNotExist:
            success, message, stat = False, "No such user exists", status.HTTP_400_BAD_REQUEST

        link = f"HappySpace://forgot/{email}/{user.verification_code}/"
        
        resp = {
            "status": success,
            "message": message,
        }

        if success and settings.DEBUG:
            resp.update({"otp_code": user.verification_code, 'link': link})

        return Response(resp, status=stat)


class ForgetPassword(PublicAPI):
    
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        code = request.data.get('verification_code')
        stat = None
        message = None
        success = None

        try:
            user = UserModel.objects.get(email=email)
            timeout_check = user.validate_timeout(code)
            
            if timeout_check:
                user.set_password(password)
                user.save()
                success, message, stat = True, "password has been changed", status.HTTP_200_OK
            else:
                success, message, stat = False, "verification code has expired", status.HTTP_400_BAD_REQUEST
        
        except UserModel.DoesNotExist:
            success, message, stat = False, "No such user exists", status.HTTP_400_BAD_REQUEST

        return Response({
            "status": success,
            "message": message
        }, status=stat)

class LoginUser(PublicAPI):

    def post(self, request):

        eamil = request.data.get('email')
        password = request.data.get('password')

        try:
            user = UserModel.objects.get(email=eamil)
        except UserModel.DoesNotExist:
            return Response({
                "status": False,
                "isActive": False
            }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            auth_user = user.check_password(password)

            if auth_user:
                resp = {
                    "status": True,
                    "isActive": user.is_active,
                    "name": user.name,
                    "user_type": user.user_type,
                    "image_url": user.image_url,
                }
                if user.is_active:
                    login(request, user)
                    return Response(resp, status=status.HTTP_200_OK)
                else:
                    user.send_email()
                    resp.update({"activation_code": user.code})
                    return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "isActive": user.is_active
                }, status=status.HTTP_400_BAD_REQUEST)
    
class ResendVerificationCode(PublicAPI):

    def post(self, request):

        email = request.data.get('email')
        try:
            user = UserModel.objects.get(email=email)
            if not user.is_active:
                user.send_email()

                resp = {
                    'status': True,
                    'message': 'verification code sent'
                }
                if settings.DEBUG:
                    resp.update({'verfication_code': user.verification_code})

                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'message': 'user already verified'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except UserModel.DoesNotExist:
            return Response({
                'status': False,
                'message': "so such user with email exists"
            }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(PublicAPI):

    def post(self, request):
        logout(request)
        return Response({'success':True, 'message': "Logout successfull."}, status=status.HTTP_200_OK)

class CheckAuth(PrivateAPI):

    def get(self, request):

        return Response({'status': True, 'email': request.user.username}, status=status.HTTP_200_OK)

class UpdateUserDetails(PrivateAPI):

    def post(self, request):
        
        name = request.data.get('name')
        designation = request.data.get('designation')
        image_url = request.data.get('image_url')

        if name:
            request.user.name = name
        if designation:
            request.user.designation = designation
        if image_url:
            request.user.image_url = image_url


        request.user.save()

        return Response({
            "status": True,
            "message": "user info updated",
        }, status = status.HTTP_200_OK)

class ChangePassword(PrivateAPI):

    def post(self, request):

        password = request.data.get('password')

        if CreateUser.validate_password(password):

            request.user.set_password(str(password))
            request.user.save()

            return Response({
                'status': True,
                'message': 'success'
            }, status = status.HTTP_200_OK)
        
        else:
            return Response({
                'status': False,
                'message': 'password must be grater than 8 characters'
            }, status = status.HTTP_400_BAD_REQUEST)