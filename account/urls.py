from django.urls import path
from .views import *

urlpatterns=[
    path('reg',RegView.as_view(),name="reg"),
    # path('home',HomeView.as_view(),name="home"),
    path('logout',LogoutView.as_view(),name="logout")
]