# app_timers/urls.py

from django.urls import path
from .views import (
    UserLabelListView,
    TimerBlockCreateView,
    TimerBlockListView,
    TimerBlockStartView,
    TimerBlockStopView,
    TimerBlockPauseView,
    TimerSessionCreateView,
    TimerSessionAnalyzeView,
    TimerSessionAddTimerBlockView, LabelCreateView, LabelUpdateDeleteView,
)





urlpatterns = [
    # Label operations
    path('label/create/', LabelCreateView.as_view(), name='create_label'),
    # Create, update, delete a label

    path('label/<int:pk>/', LabelUpdateDeleteView.as_view(), name='label_detail'),  # Create, update, delete a label
    path('labels/', UserLabelListView.as_view(), name='user_labels'),  # List all labels for the user

    # TimerBlock operations
    path('timerblock/create/', TimerBlockCreateView.as_view(), name='create_timer_block'),  # Create TimerBlock
    path('timerblocks/', TimerBlockListView.as_view(), name='timer_block_list'),  # List all TimerBlocks
    path('timerblock/<int:pk>/start/', TimerBlockStartView.as_view(), name='start_timer_block'),  # Start TimerBlock
    path('timerblock/<int:pk>/stop/', TimerBlockStopView.as_view(), name='stop_timer_block'),  # Stop TimerBlock
    path('timerblock/<int:pk>/pause/', TimerBlockPauseView.as_view(), name='pause_timer_block'),  # Pause TimerBlock

    # TimerSession operations
    path('timersession/', TimerSessionCreateView.as_view(), name='create_timer_session'),  # Create TimerSession
    path('timersession/<int:pk>/analyze/', TimerSessionAnalyzeView.as_view(), name='analyze_timer_session'),  # Analyze TimerSession
    path('timersession/<int:pk>/add_timerblock/', TimerSessionAddTimerBlockView.as_view(), name='add_timer_block_to_session'),  # Add TimerBlock to TimerSession
]
