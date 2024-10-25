# app_user/views.py

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import update_last_login
from app_timers.models import Label, TimerSession
from . import serializers
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .app_operations_user import UserOperations
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken



class PaymentView(APIView):
    permission_classes = [AllowAny]  # Requires user authentication

    def post(self, request):
        """Handles user payment processing."""
        if request.user.is_authenticated:
            # Process payment and set user premium status
            request.user.is_premium = UserOperations.process_payment(request.payment_information, request.user)
            return Response({'message': 'Payment successful!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Payment failed!'}, status=status.HTTP_400_BAD_REQUEST)


# region LOGIN-LOGOUT-REGISTER OPERATIONS

class RegisterUserView(APIView):
    """
    ## 👤 **User Registration API**

    🔗 **API URL:** `api/user/register`

    API for user registration.

    - 📨 **HTTP Method:** POST

    - 📥 **Inputs:**
        - 📝 **username (string):** Desired username of the user.
        - 📝 **first_name (string):** User's first name.
        - 📝 **last_name (string):** User's last name.
        - 📝 **email (string):** User's email address.
        - 🔐 **password (string):** User's account password.
        - 🔐 **confirm_password (string):** Confirmation of the account password.

        - 📄 Example JSON Input:
        ```json
        {
            "username": "john_doe",
            "first_name": "john",
            "last_name": "doe",
            "email": "john@example.com",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        ```

    - 📤 **Outputs:**
        - ✅ **Successful Registration:**
            - If inputs are valid and registration is successful:
                - ✅ Status: 201 Created
                - 📄 Response JSON:
                ```json
                {
                    "username": "john_doe",
                    "first_name": "john",
                    "last_name": "doe",
                    "email": "john@example.com"
                }
                ```
        - ❌ **Errors:**
            - If passwords do not match:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"error": "Passwords must match!"}`
            - If email is already taken:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"error": "Email is already taken!"}`
            - If username is already taken:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"error": "Username is already taken!"}`
            - If password length is invalid:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"error": "Password length must be between 5-20 characters!"}`
            - If username length is invalid:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"error": "Username length must be between 5-20 characters!"}`
    """

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        error_message = ""

        # Extract user input data
        username = request.data.get('username')
        if not username:
            error_message = "Username cannot be empty!"
        first_name = request.data.get('first_name')
        if not first_name:
            error_message = "First name cannot be empty!"
        last_name = request.data.get('last_name')
        if not last_name:
            error_message = "Last name cannot be empty!"
        email = request.data.get('email')
        if not email:
            error_message = "Email cannot be empty!"
        password = request.data.get('password')
        if not password:
            error_message = "Password cannot be empty!"
        confirm_password = request.data.get('confirm_password')
        if not confirm_password:
            error_message = "Confirmation password cannot be empty!"

        # Return error message if any validation fails
        if error_message:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username or email already exists
        is_exist_username = CustomUser.objects.filter(username=username).exists()
        is_exist_email = CustomUser.objects.filter(email=email).exists()

        # Set appropriate error messages based on validation
        if password != confirm_password:
            error_message = "Passwords must match!"
        elif is_exist_email:
            error_message = "Email is already taken!"
        elif is_exist_username:
            error_message = "Username is already taken!"
        elif len(password) < 5 or len(password) > 20:
            error_message = "Password length must be between 5-20 characters!"
        elif len(username) < 5 or len(username) > 20:
            error_message = "Username length must be between 5-20 characters!"

        # Return error message if any validation fails
        if error_message:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Hash the password before saving
            hashed_password = make_password(password)
            user = serializer.save(password=hashed_password, first_name=first_name, last_name=last_name)
            # Create default Label and Session
            try:
                Label.objects.create(user=user, title="Default Label")
                TimerSession.objects.create(user=user)
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    ## 🔑 **User Login API** (JWT ile)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Email ile kullanıcıyı bul
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Kullanıcıyı doğrula
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            if user.is_mail_verified:
                # JWT RefreshToken ve AccessToken oluşturma
                refresh = RefreshToken.for_user(user)

                # Son giriş zamanını güncelle
                update_last_login(None, user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_info': {
                        'username': user.username,
                        'email': user.email,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email not verified.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    🚪 **Logout API**

    🔗 **API URL:** `api/user/logout/`

    API to securely log out a user.

    - 🔑 **HTTP Method:** GET

    - 📤 Outputs:
        - ✅ **Successful Logout:**
            - If the user is logged in:
                - ✅ Status: 200 OK
                - 📄 Response JSON: `{"detail": "Logged out successfully."}`
            - If the user is not logged in:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"detail": "Authentication credentials were not provided."}`

    - 🔏 **Permissions:**
    - Only authenticated users can use this API (🔒 IsAuthenticated).
    """
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """Logs out the authenticated user."""
        logout(request)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class SendVerifyCodeView(APIView):
    """
    ## ✉️ **Verification Code Sender API**

    🔗 **API URL:** `api/user/email/verification/send-code`

    API that sends a verification code to the user's email.

    - 📨 **HTTP Method:** POST

    - 📥 **Input:**
        - ✉️ **email (string):** User's email address where the verification code will be sent.

        - 📄 Example JSON Input:
        ```json
        {
            "email": "example@example.com"
        }
        ```

    - 📤 **Outputs:**
        - ✅ **Successful Code Sending:**
            - If no issues occur:
                - ✅ Status: 200 OK
                - 📄 Response JSON: `{"message": "Verification code sent to your email."}`
            - If the user does not have the email address:
                - ❌ Status: 404 Not Found
                - 📄 Response JSON: `{"error": "No user with this email."}`

        - ❌ **Failed Code Sending:**
            - If email does not belong to the institution:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"error": "Email must be from the institution!"}`
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        # Check if the email belongs to a user
        user = CustomUser.objects.filter(email=email).first()

        if user:
            verification_code = get_random_string(length=8)  # Generate a random verification code
            send_mail(
                'Your Verification Code',  # Subject
                f'Your verification code is: {verification_code}',  # Message
                'noreply@yourapp.com',  # From email
                [email],  # To email
                fail_silently=False,
            )
            return Response({'message': 'Verification code sent to your email.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No user with this email.'}, status=status.HTTP_404_NOT_FOUND)


class VerifyCodeView(APIView):
    """
    ## 🔑 **Code Verification API**

    🔗 **API URL:** `api/user/email/verification`

    API that verifies the code sent to the user's email.

    - 📨 **HTTP Method:** POST

    - 📥 **Input:**
        - ✉️ **email (string):** User's email address.
        - 🔑 **verification_code (string):** Verification code sent to the user's email.

        - 📄 Example JSON Input:
        ```json
        {
            "email": "example@example.com",
            "verification_code": "yourcode123"
        }
        ```

    - 📤 **Outputs:**
        - ✅ **Successful Code Verification:**
            - If code matches:
                - ✅ Status: 200 OK
                - 📄 Response JSON: `{"message": "Email verified successfully."}`

        - ❌ **Failed Code Verification:**
            - If code does not match:
                - ❌ Status: 401 Unauthorized
                - 📄 Response JSON: `{"error": "Verification code is incorrect."}`
            - If email does not belong to the institution:
                - ❌ Status: 400 Bad Request
                - 📄 Response JSON: `{"error": "Email must be from the institution!"}`
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')

        user = CustomUser.objects.filter(email=email).first()

        if user and verification_code == user.verification_code:  # Assuming verification_code is stored in the user model
            user.is_mail_verified = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Verification code is incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

# endregion



#login for session

# views.py

from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login_view(request):
    """
    Example Input:
            {
                "username": "john_doe",
                "password": "securepassword123"
            }
    """
    username = request.data.get('username')
    password = request.data.get('password')

    # Kullanıcıyı doğrula
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Kullanıcıyı oturum aç
        return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

