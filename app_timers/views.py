# app_timers/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Label, TimerBlock
from .serializers import LabelSerializer, TimerBlockSerializer
from django.utils import timezone

class LabelCreateView(generics.CreateAPIView):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user to the active user
        serializer.save(user=self.request.user)

class LabelUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter labels for the active user
        return Label.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the active user
        serializer.save(user=self.request.user)

class UserLabelListView(generics.ListAPIView):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # List labels for the active user
        return Label.objects.filter(user=self.request.user)

class TimerBlockCreateView(generics.CreateAPIView):
    serializer_class = TimerBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user to the active user
        serializer.save(user=self.request.user)

class TimerBlockListView(generics.ListAPIView):
    serializer_class = TimerBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # List all TimerBlocks for the active user
        return TimerBlock.objects.filter(user=self.request.user).order_by('-created_at')

class TimerBlockStartView(generics.UpdateAPIView):
    serializer_class = TimerBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        timer_block = serializer.instance
        timer_block.is_started = True
        timer_block.started_at = timezone.now()
        timer_block.save()

class TimerBlockStopView(generics.UpdateAPIView):
    serializer_class = TimerBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        timer_block = serializer.instance
        timer_block.is_started = False
        timer_block.is_completed = True
        timer_block.completed_at = timezone.now()
        timer_block.save()

class TimerBlockPauseView(generics.UpdateAPIView):
    serializer_class = TimerBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        timer_block = serializer.instance
        timer_block.is_started = False
        timer_block.save()

class TimerSessionCreateView(generics.CreateAPIView):
    serializer_class = TimerBlockSerializer  # Use TimerSessionSerializer when defined
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Save the TimerSession with the active user
        serializer.save(user=self.request.user)

class TimerSessionAnalyzeView(generics.RetrieveAPIView):
    serializer_class = TimerBlockSerializer  # Use TimerSessionSerializer when defined
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        session = self.get_object()
        timer_blocks = session.timer_blocks.split(',')  # Assume timer_blocks is a CSV of TimerBlock IDs
        return Response(timer_blocks)

class TimerSessionAddTimerBlockView(generics.UpdateAPIView):
    serializer_class = TimerBlockSerializer  # Use TimerSessionSerializer when defined
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TimerBlock.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        session = serializer.instance
        new_timer_block_id = self.request.data.get('timer_block_id')
        if new_timer_block_id:
            session.timer_blocks += f',{new_timer_block_id}'  # Append new TimerBlock ID
            session.save()
