from django.urls import path
from . import views
from django.urls import path
from .views import (
    CreateTimerBlockView,
    TimerBlockDetailView,
    TimerBlockNoteView,
    AddToSessionView,
    RemoveFromSessionView,
    WorkBlockStatsView,
    StartWorkBlockView,
    PauseWorkBlockView,
    ContinueWorkBlockView,
    StopWorkBlockView,
    ListWorkBlocksInSessionView,
    ResetSessionView, LabelDetailOfTitleView, TimerBlockListView
)



urlpatterns = [

    # Label APIs
    path('api/labels/', views.LabelListAPIView.as_view(), name='label-list'),
    path('api/labels/detail-of-title/', LabelDetailOfTitleView.as_view(), name='label-detail-of-title'),

    path('api/labels/create/', views.LabelCreateAPIView.as_view(), name='label-create'),
    path('api/labels/<int:pk>/', views.LabelDetailAPIView.as_view(), name='label-detail'),
    path('api/labels/<int:pk>/notes/', views.LabelNoteUpdateAPIView.as_view(), name='label-notes'),

    # Work Block APIs
    path('api/work-blocks/', views.WorkBlockListAPIView.as_view(), name='work-block-list'),
    path('api/work-blocks/filtered/', views.FilteredWorkBlockAPIView.as_view(), name='filtered-work-block-list'),
    path('api/timer-blocks/', CreateTimerBlockView.as_view(), name='create-timer-block'),
    path('api/list-timer-blocks/', TimerBlockListView.as_view(), name='timer-block-list'),

    path('api/timer-blocks/<int:pk>/', TimerBlockDetailView.as_view(), name='timer-block-detail'),
    path('api/timer-blocks/<int:pk>/notes/', TimerBlockNoteView.as_view(), name='timer-block-notes'),
    path('api/timer-blocks/<int:pk>/stats/', WorkBlockStatsView.as_view(), name='work-block-stats'),
    path('api/timer-blocks/<int:pk>/start/', StartWorkBlockView.as_view(), name='start-work-block'),
    path('api/timer-blocks/<int:pk>/pause/', PauseWorkBlockView.as_view(), name='pause-work-block'),
    path('api/timer-blocks/<int:pk>/continue/', ContinueWorkBlockView.as_view(), name='continue-work-block'),
    path('api/timer-blocks/<int:pk>/stop/', StopWorkBlockView.as_view(), name='stop-work-block'),

    #Session APIs
    path('api/session/work-blocks/', ListWorkBlocksInSessionView.as_view(), name='list-work-blocks-in-session'),
    path('api/session/reset/', ResetSessionView.as_view(), name='reset-session'),
    path('api/timer-blocks/add-to-session/', AddToSessionView.as_view(), name='add-to-session'),
    path('api/timer-blocks/remove-from-session/', RemoveFromSessionView.as_view(), name='remove-from-session'),

]
