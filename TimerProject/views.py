# TimerProject/views.py
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# TimerProject/views.py

from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'CustomUser Operations': {
            'Register': reverse('register', request=request, format=format),  # User registration
            'Login-With-Token': reverse('login-with-token', request=request, format=format),        # User login
            'Login-With-Session': reverse('login-with-session', request=request, format=format),  # User login
            'Logout': reverse('logout', request=request, format=format),      # User logout
            'Send Email Verification Code': reverse('send-email-verify-code', request=request, format=format),  # Send verification code
            'Confirm Email Verification Code': reverse('confirm-email-verify-code', request=request, format=format),  # Confirm verification code
            'Make Payment': reverse('make_payment', request=request, format=format),  # Make payment
        },
        'Timer Operations': {
            'Create Label': reverse('create_label', request=request, format=format),  # Create a TimerBlock
            'Label Detail': reverse('label_detail', args=[0], request=request, format=format),  # Create or update a label
            'List User Labels': reverse('user_labels', request=request, format=format),  # List all labels for the user
            'Create Timer Block': reverse('create_timer_block', request=request, format=format),  # Create a TimerBlock
            'List Timer Blocks': reverse('timer_block_list', request=request, format=format),  # List all TimerBlocks
            'Start Timer Block': reverse('start_timer_block', args=[0], request=request, format=format),  # Start TimerBlock
            'Stop Timer Block': reverse('stop_timer_block', args=[0], request=request, format=format),  # Stop TimerBlock
            'Pause Timer Block': reverse('pause_timer_block', args=[0], request=request, format=format),  # Pause TimerBlock
            'Create Timer Session': reverse('create_timer_session', request=request, format=format),  # Create TimerSession
            'Analyze Timer Session': reverse('analyze_timer_session', args=[0], request=request, format=format),  # Analyze TimerSession
            'Add Timer Block to Session': reverse('add_timer_block_to_session', args=[0], request=request, format=format),  # Add TimerBlock to TimerSession
        }
    })

def redirect_api_root(request):
    return redirect("api-root")

