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
        'Label Operations': {
            'List Labels': reverse('label-list', request=request, format=format),
            'Create Label': reverse('label-create', request=request, format=format),
            'Find Label (With Title)': reverse('label-detail-of-title', request=request, format=format),
            'Detail - Update - Delete Label (with ID)': reverse('label-detail', args=[1], request=request, format=format),  # Example ID = 1
            'Detail - Update - Delete Label Notes': reverse('label-notes', args=[1], request=request, format=format),  # Example ID = 1
            'List Label Notes (Timer Blocks)': reverse('timer-block-list', request=request, format=format),
        },
        'Work Block Operations': {
            'List Work Blocks': reverse('work-block-list', request=request, format=format),
            'Filtered Work Blocks': reverse('filtered-work-block-list', request=request, format=format),
            'Create Timer Block': reverse('create-timer-block', request=request, format=format),
            'Detail Timer Block': reverse('timer-block-detail', args=[1], request=request, format=format),
            # Example ID = 1
            'Update Timer Block Notes': reverse('timer-block-notes', args=[1], request=request, format=format),
            # Example ID = 1
            'Update Work Block Statistics': reverse('work-block-stats', args=[1], request=request, format=format),
            # Example ID = 1
            'Start Work Block': reverse('start-work-block', args=[1], request=request, format=format),  # Example ID = 1
            'Pause Work Block': reverse('pause-work-block', args=[1], request=request, format=format),  # Example ID = 1
            'Continue Work Block': reverse('continue-work-block', args=[1], request=request, format=format),
            # Example ID = 1
            'Stop Work Block': reverse('stop-work-block', args=[1], request=request, format=format),  # Example ID = 1
        },
        'Session Operations': {
            'List Work Blocks in Session': reverse('list-work-blocks-in-session', request=request, format=format),
            'Reset Session': reverse('reset-session', request=request, format=format),
            'Add Work Block to Session': reverse('add-to-session', request=request, format=format),
            # Example ID = 1
            'Remove Work Block from Session': reverse('remove-from-session',request=request, format=format),
            # Example ID = 1
        }
    })

def redirect_api_root(request):
    return redirect("api-root")

