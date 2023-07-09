
from . import views
from django.urls import path


urlpatterns = [
    path('', views.index),
    path('personal/', views.personal,name="personal"),
    path('login/',views.AuthView.as_view(),name='login'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('room/<str:room_name>/', views.room, name='chat'),
]